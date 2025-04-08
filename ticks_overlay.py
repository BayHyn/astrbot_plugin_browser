
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO

SCALE_PATH = Path("data/plugins/astrbot_plugin_browser/resource/ruler_scale.png")
SCALE_PATH.parent.mkdir(parents=True, exist_ok=True)

FONT_PATH: Path = Path("data/plugins/astrbot_plugin_browser/resource/simhei.ttf")


async def create_ticks_overlay():
    """生成刻度背景图"""
    width, height = 4000, 13000  # 图片宽高
    major_tick_length_x = 20  # X轴主刻度线长度
    minor_tick_length_x = 10  # X轴子刻度线长度
    major_tick_length_y = 30  # Y轴主刻度线长度
    minor_tick_length_y = 15  # Y轴子刻度线长度
    tick_interval = 100  # 刻度间隔
    font_size = 20  # 字体大小
    font_color = (200, 0, 0)  # 字体颜色
    line_color = (0, 0, 0)  # 线条颜色
    dot_radius = 1  # 点的半径
    dot_color = (0, 0, 0)  # 点的颜色


    # 创建具有透明背景的图像
    img = Image.new('RGBA', (width, height), color=(255, 255, 255, 0))
    draw = ImageDraw.Draw(img)

    # 绘制X轴和Y轴上的刻度
    for i in range(0, width + 1, tick_interval):
        # X轴主刻度
        draw.line([(i, major_tick_length_x), (i, 0)], fill=line_color)
        # X轴子刻度
        for j in range(1, 10):
            minor_pos = i - (j * tick_interval // 10)
            if minor_pos > 0:
                draw.line([(minor_pos, minor_tick_length_x), (minor_pos, 0)], fill=line_color)

    for i in range(0, height + 1, tick_interval):
        # Y轴主刻度
        draw.line([(0, i), (major_tick_length_y, i)], fill=line_color)
        # Y轴子刻度
        for j in range(1, 10):
            minor_pos = i + (j * tick_interval // 10)
            if minor_pos < height:
                draw.line([(minor_tick_length_y, minor_pos), (0, minor_pos)], fill=line_color)
    # 在x轴和y轴的每个主刻度交点处画点
    for x in range(0, width + 1, tick_interval):
        for y in range(0, height + 1, tick_interval):
            draw.ellipse(
                [(x - dot_radius, y - dot_radius), (x + dot_radius, y + dot_radius)],
                fill=dot_color
            )
    # 添加文字标签
    font = ImageFont.truetype(str(FONT_PATH), font_size)
    for i in range(0, width + 1, tick_interval):
        draw.text((i, major_tick_length_x), str(i), font=font, fill=font_color)
    for i in range(0, height + 1, tick_interval):
        draw.text((major_tick_length_y + 5, i), str(i), font=font, fill=font_color)

    # 保存图像
    img.save(str(SCALE_PATH), format = 'PNG')


def overlay_ticks_on_background(background_bytes) -> bytes:
    """将刻度覆盖层叠加到背景图片上"""
    background = Image.open(BytesIO(background_bytes)).convert("RGBA")
    overlay = Image.open(SCALE_PATH).convert("RGBA")

    combined = Image.new("RGBA", background.size)
    combined.paste(background, (0, 0))  # 将背景图片粘贴到新创建的图像上
    combined.paste(overlay, (0, 0), overlay)   # 将刻度覆盖层粘贴到新创建的图像的左上角

    output = BytesIO()
    combined.save(output, format="PNG")
    return output.getvalue()














