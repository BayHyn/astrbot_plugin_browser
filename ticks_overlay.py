
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO

class TickOverlayManager:
    def __init__(
        self,
        font_path: Path = Path(
            "data/plugins/astrbot_plugin_browser/resource/kaiti_GB2312.ttf"
        ),
        scale_path: Path = Path(
            "data/plugins/astrbot_plugin_browser/resource/ticks_overlay.png"
        ),
        width: int = 4000,
        height: int = 13000,
        tick_interval: int = 100,
        font_size: int = 20,
    ):
        self.font_path = font_path
        self.scale_path = scale_path
        self.width = width
        self.height = height
        self.tick_interval = tick_interval
        self.font_size = font_size

        # 样式设定
        self.font_color = (200, 0, 0)
        self.line_color = (0, 0, 0)
        self.dot_color = (0, 0, 0)
        self.major_tick_length_x = 20
        self.minor_tick_length_x = 10
        self.major_tick_length_y = 30
        self.minor_tick_length_y = 15
        self.dot_radius = 1

    def create_overlay(self):
        """生成刻度覆盖图并保存为PNG"""
        img = Image.new("RGBA", (self.width, self.height), color=(255, 255, 255, 0))
        draw = ImageDraw.Draw(img)

        # 画X轴刻度
        for x in range(0, self.width + 1, self.tick_interval):
            draw.line([(x, self.major_tick_length_x), (x, 0)], fill=self.line_color)
            for j in range(1, 10):
                minor_x = x - (j * self.tick_interval // 10)
                if minor_x > 0:
                    draw.line(
                        [(minor_x, self.minor_tick_length_x), (minor_x, 0)],
                        fill=self.line_color,
                    )

        # 画Y轴刻度
        for y in range(0, self.height + 1, self.tick_interval):
            draw.line([(0, y), (self.major_tick_length_y, y)], fill=self.line_color)
            for j in range(1, 10):
                minor_y = y + (j * self.tick_interval // 10)
                if minor_y < self.height:
                    draw.line(
                        [(self.minor_tick_length_y, minor_y), (0, minor_y)],
                        fill=self.line_color,
                    )

        # 主刻度交点加点
        for x in range(0, self.width + 1, self.tick_interval):
            for y in range(0, self.height + 1, self.tick_interval):
                draw.ellipse(
                    [
                        (x - self.dot_radius, y - self.dot_radius),
                        (x + self.dot_radius, y + self.dot_radius),
                    ],
                    fill=self.dot_color,
                )

        # 添加文字标签
        font = ImageFont.truetype(self.font_path, self.font_size)
        for x in range(0, self.width + 1, self.tick_interval):
            draw.text(
                (x, self.major_tick_length_x), str(x), font=font, fill=self.font_color
            )
        for y in range(0, self.height + 1, self.tick_interval):
            draw.text(
                (self.major_tick_length_y + 5, y),
                str(y),
                font=font,
                fill=self.font_color,
            )

        # 保存图片
        self.scale_path.parent.mkdir(parents=True, exist_ok=True)
        img.save(str(self.scale_path), format="PNG")

    def overlay_on_background(self, background_bytes: bytes) -> bytes:
        """将刻度覆盖层叠加到背景图上，自动检查overlay是否存在"""
        if not self.scale_path.exists():
            self.create_overlay()

        background = Image.open(BytesIO(background_bytes)).convert("RGBA")
        overlay = Image.open(self.scale_path).convert("RGBA")

        combined = Image.new("RGBA", background.size)
        combined.paste(background, (0, 0))
        combined.paste(overlay, (0, 0), overlay)

        output = BytesIO()
        combined.save(output, format="PNG")
        return output.getvalue()
