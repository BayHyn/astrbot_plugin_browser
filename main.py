import asyncio
import re
import time
import json
from astrbot import logger
from astrbot.api.event import filter
from astrbot.api.star import Context, Star, register
from astrbot.core import AstrBotConfig
from astrbot.core.platform import AstrMessageEvent
from .core.browser import gbm
from .core.ticks_overlay import create_ticks_overlay
import astrbot.core.message.components as Comp


FAVORITE_PATH = "data/plugins/astrbot_plugin_browser/resource/favorite.json"
try:
    with open(FAVORITE_PATH, "r", encoding="utf-8") as file:
        favorite: dict[str, str] = json.load(file)
except json.JSONDecodeError as e:
    logger.error(f"JSON 文件格式错误: {e}")

favorite_set = set(favorite.keys())

@register("astrbot_plugin_browser", "Zhalslar", "浏览器交互插件", "1.0.0")
class AdminPlugin(Star):
    def __init__(self, context: Context, config: AstrBotConfig):
        super().__init__(context)
        self.viewport_width: int = config.get('viewport_width')  # 视口宽度
        self.viewport_height: int = config.get('viewport_height')  # 视口高度
        self.zoom_factor: float = config.get('zoom_factor')  # 打开新页面时的默认缩放比例
        self.full_page_zoom_factor: float = config.get('full_page_zoom_factor')  # 查看整页时的默认缩放比例, 0表示不改变原来的缩放比
        self.default_search_engine: str = config.get('default_search_engine')  # 默认使用的搜索引擎
        self.max_pages: int = config.get('max_pages') # 允许的最大标签页数量

        cat_log = config.get('cat_log')
        self.webui_url: str = cat_log.get('webui_url')
        self.token: str = cat_log.get('token')
        self.dark_themes: bool = cat_log.get('dark_themes')

        rebuild_ticks_img: bool = config.get('rebuild_ticks_img') # 启动时重新生成浏览器刻度图
        if rebuild_ticks_img:
            logger.info("正在重新生成浏览器刻度图...")
            asyncio.create_task(create_ticks_overlay())



    @filter.command('搜索', alias=favorite_set)
    async def search(self, event: AstrMessageEvent, keyword:str=None):
        """/搜索 xxx  /必应搜索 xxx（具体用什么搜索网页请看收藏夹）"""
        yield event.plain_result(f"稍等...")
        group_id = event.get_group_id()
        message_str = event.message_str
        selected_engine = next((k for k in favorite_set if k in message_str), self.default_search_engine)
        url = self.format_url(selected_engine, keyword)
        result = await gbm.search(
            group_id=group_id,
            url=url,
            zoom_factor=self.zoom_factor,
            max_pages= self.max_pages
        )
        if result:
            yield event.plain_result(result)
            return
        screenshot = await gbm.get_screenshot(
            group_id=group_id,
            viewport_width=self.viewport_width,
            viewport_height=self.viewport_height,
        )
        yield event.chain_result([Comp.Image.fromBytes(screenshot)])


    @filter.command("访问")
    async def visit(self, event: AstrMessageEvent, url:str=None):
        """/访问 xxx"""
        if not url:
            return
        group_id = event.get_group_id()
        yield event.plain_result("访问中...")
        result = await gbm.search(
            group_id=group_id,
            url=url,
            zoom_factor=self.zoom_factor,
            max_pages=self.max_pages
        )
        if result:
            yield event.plain_result(result)
            return
        screenshot = await gbm.get_screenshot(
            group_id=group_id,
            viewport_width=self.viewport_width,
            viewport_height=self.viewport_height,
        )
        yield event.chain_result([Comp.Image.fromBytes(screenshot)])


    @filter.command("点击")
    async def click(self, event: AstrMessageEvent, input_x:int=0, input_y:int=0):
        """模拟点击，如/点击 200 300"""
        group_id = event.get_group_id()
        coords = input_x, input_y
        result = await gbm.click_coord(group_id=group_id, coords=coords)
        if result:
            yield event.plain_result(result)
            return
        screenshot = await gbm.get_screenshot(
            group_id=group_id,
            viewport_width=self.viewport_width,
            viewport_height=self.viewport_height,
        )
        yield event.chain_result([Comp.Image.fromBytes(screenshot)])


    @filter.command("输入")
    async def text_input(self, event: AstrMessageEvent, text:str=None, input_x:int=None, input_y:int=None):
        """向输入框输入文本，如/输入 阿巴阿巴 /输入 阿巴阿巴 200 300"""
        group_id = event.get_group_id()
        coords = [input_x, input_y]  if (input_x and input_y) else None
        result = await gbm.text_input(group_id=group_id, text=text, coords=coords)
        if result:
            yield event.plain_result(result)
            return
        screenshot = await gbm.get_screenshot(
            group_id=group_id,
            viewport_width=self.viewport_width,
            viewport_height=self.viewport_height,
        )
        yield event.chain_result([Comp.Image.fromBytes(screenshot)])

    @filter.command("滑动")
    async def swipe(self, event: AstrMessageEvent, start_x:int=None, start_y:int=None, end_x:int=None, end_y:int=None):
        """模拟滑动，如/滑动 200 300 200 500， 即从点(200,300)滑动到点(200,500)"""
        group_id = event.get_group_id()
        coords = start_x, start_y, end_x, end_y
        if len(coords) != 4:
            yield event.plain_result("应提供4个整数：起始X，起始Y，结束X，结束Y")
            return
        result = await gbm.swipe(group_id=group_id, coords=coords)
        if result:
            yield event.plain_result(result)
            return
        screenshot = await gbm.get_screenshot(
            group_id=group_id,
            viewport_width=self.viewport_width,
            viewport_height=self.viewport_height,
        )
        yield event.chain_result([Comp.Image.fromBytes(screenshot)])


    @filter.command("缩放")
    async def zoom_to_scale(self, event: AstrMessageEvent, scale_factor:float=1.5):
        """把网页缩放，如/缩放 1.6"""
        group_id = event.get_group_id()
        result = await gbm.zoom_to_scale(group_id=group_id, scale_factor=scale_factor)
        if result:
            yield event.plain_result(result)
            return
        screenshot = await gbm.get_screenshot(
            group_id=group_id,
            viewport_width=self.viewport_width,
            viewport_height=self.viewport_height,
        )
        yield event.chain_result([Comp.Image.fromBytes(screenshot)])


    @filter.command("滚动", alias={"向下滚动", "向上滚动", "向左滚动", "向右滚动"})
    async def scroll(self, event: AstrMessageEvent, distance:int=None):
        """向某个方向滚动网页，如/滚动， /向{上下左右}滚动"""
        group_id = event.get_group_id()
        arg = event.message_str.strip().split()[0]
        distance = distance or (self.viewport_height - 100)
        if len(arg) == 2:
            direction = '向下'
        else:
            direction = arg[:2]
        result = await gbm.scroll_by(group_id=group_id, distance=distance, direction=direction)
        if result:
            yield event.plain_result(result)
            return
        screenshot = await gbm.get_screenshot(
            group_id=group_id,
            viewport_width=self.viewport_width,
            viewport_height=self.viewport_height,
        )
        yield event.chain_result([Comp.Image.fromBytes(screenshot)])


    @filter.command("当前页面", alias={"整页"})
    async def view_full_page(self, event: AstrMessageEvent, zoom_factor:float=None):
        """查看当前的标签页：/当前页面，整页显示网页：/整页"""
        group_id = event.get_group_id()
        message_str = event.get_message_str()
        full_page = "整页" in message_str

        target_zoom_factor = (zoom_factor if zoom_factor else self.full_page_zoom_factor) if full_page else None
        screenshot  = await gbm.get_screenshot(
            group_id=group_id,
            full_page=full_page,
            zoom_factor=target_zoom_factor
        )
        yield event.chain_result([Comp.Image.fromBytes(screenshot)])


    @filter.command("上一页")
    async def go_back(self, event: AstrMessageEvent):
        """跳转上一页"""
        group_id = event.get_group_id()
        result = await gbm.go_back(group_id=group_id)
        if result:
            yield event.plain_result(result)
            return
        screenshot = await gbm.get_screenshot(
            group_id=group_id,
            viewport_width=self.viewport_width,
            viewport_height=self.viewport_height,
        )
        yield event.chain_result([Comp.Image.fromBytes(screenshot)])


    @filter.command("下一页")
    async def go_forward(self, event: AstrMessageEvent):
        """跳转下一页"""
        group_id = event.get_group_id()
        result = await gbm.go_forward(group_id=group_id)
        if result:
            yield event.plain_result(result)
            return
        screenshot = await gbm.get_screenshot(
            group_id=group_id,
            viewport_width=self.viewport_width,
            viewport_height=self.viewport_height,
        )
        yield event.chain_result([Comp.Image.fromBytes(screenshot)])


    @filter.command("标签页列表")
    async def get_all_tabs_titles(self, event: AstrMessageEvent):
        """查看所有标签页的标题"""
        titles = await gbm.get_all_tabs_titles()
        titles_str = ("\n".join(f"{i + 1}. {title}" for i, title in enumerate(titles))) or "暂无打开中的标签页"
        yield event.plain_result(titles_str)


    @filter.command("标签页")
    async def switch_to_tab(self, event: AstrMessageEvent, index:int=1):
        """切换到指定序号的标签页，如/标签页 2"""
        group_id = event.get_group_id()
        result = await gbm.switch_to_tab(group_id=group_id, tab_index=index - 1)
        if result:
            yield event.plain_result(result)
            return
        screenshot = await gbm.get_screenshot(
            group_id=group_id,
            viewport_width=self.viewport_width,
            viewport_height=self.viewport_height,
        )
        yield event.chain_result([Comp.Image.fromBytes(screenshot)])


    @filter.command("关闭标签页")
    async def close_tab(self, event: AstrMessageEvent):
        """关闭指定的标签页，如/关闭标签页 1 3 4"""
        group_id = event.get_group_id()
        message_str = event.get_message_str()
        index_list = [int(num) for num in re.findall(r'\d+', message_str)]
        if not index_list:  # 如果输入为空，则默认操作为关闭最后一个标签页
            result = await gbm.close_tab(group_id=group_id)
            if result:
                yield event.plain_result(result)
                return
        else:
            try:  # 将输入的索引转换为整数，并按降序排序
                index_list = sorted(index_list, reverse=True)
            except ValueError:
                yield event.plain_result("所有输入必须是整数序号")
                return
            for index in index_list:
                result = await gbm.close_tab(tab_index=index - 1, group_id=group_id)
                if result:
                    yield event.plain_result(result)


    @filter.command("关闭浏览器")
    async def close_browser(self, event: AstrMessageEvent):
        """关闭浏览器"""
        is_closed = await gbm.close_browser()
        if is_closed:
            yield event.plain_result("浏览器已关闭")
        else:
            yield event.plain_result("没有打开中的浏览器")


    @filter.command("猫猫日志")
    async def handle_cat_log(self, event: AstrMessageEvent):
        """自动跳转到NapCat的猫猫日志"""
        group_id = event.get_group_id()
        try:
            await gbm.search(group_id=group_id, url= self.webui_url)
            await gbm.text_input(group_id=group_id, text= self.token)
            await gbm.click_button(group_id=group_id, button_text="登录")
            await gbm.click_button(group_id=group_id, button_text="猫猫日志")
            if self.dark_themes:
                await gbm.click_button(group_id=group_id, button_text="切换主题")
            screenshot_path = await gbm.get_screenshot(group_id=group_id)
            yield event.image_result(screenshot_path)
        except Exception as e:
            logger.error(f"猫猫日志打开时出错：{e}")
            yield event.plain_result("猫猫日志打不开啦~")


    @staticmethod
    def get_current_timestamps():
        """获取当前的秒级和毫秒级时间戳"""
        current_time = time.time()  # 获取当前时间戳（秒）
        timestamp_s = int(current_time)  # 秒级时间戳
        timestamp_ms = int(current_time * 1000)  # 毫秒级时间戳
        return timestamp_s, timestamp_ms


    def format_url(self, selected_engine, keyword):
        """根据选定的搜索引擎和关键词格式化URL"""
        if selected_engine in  favorite:
            url_template = favorite[selected_engine]
            timestamp_s, timestamp_ms = self.get_current_timestamps()
            params = {
                'keyword': keyword,
                'timestamp_s': timestamp_s,
                'timestamp_ms': timestamp_ms
            }
            try:
                formatted_url = url_template.format(**params)
            except KeyError as e:
                # 如果模板中有未定义的占位符，则移除相应的参数并重试
                missing_key = e.args[0]
                del params[missing_key]
                formatted_url = url_template.format(**params)

            return formatted_url
        else:
            return ""






