import pygame as pg
from settings import *
from lib import MOD

class Help():
    def __init__(self):
        self.screen = MOD.get_screen()
        self.back_img = pg.image.load(HELP_BACK_BUTTON_PATH).convert_alpha()
        self.back_img = pg.transform.scale(self.back_img, (50, 50))
        self.background = pg.image.load(HELP_BACKGROUND_PATH).convert_alpha()
        self.background = pg.transform.scale(self.background, (WIDTH, HEIGTH))
        self.back_button = MOD.BUTTON(40, 20, self.back_img)
        self.max_scroll = 3500# 设定最大滚动高度
        # 文档内容（示例）
        self.doc_content = HELP_TEXTS

        self.scroll_offset = 0
        self.sidebar_width = 50
        self.sidebar_x = WIDTH - self.sidebar_width
        self.sidebar_height = HEIGTH
        self.sidebar_button_height = 60  # 拖动按钮的高度
        self.button_y = 100  # 按钮的初始Y坐标
        self.dragging_sidebar = False

        # 初始化字体
        self.FONT1 = pg.font.Font(FONT, 30)
        self.FONT2 = pg.font.Font(FONT1, 30)
        self.FONT3 = pg.font.Font(FONT2, 30)  # 提供三种字体

    def draw_document(self):
        """绘制文档内容"""
        y_pos = 50 - self.scroll_offset
        for paragraph in self.doc_content:
            lines = paragraph.split("\n")
            for line in lines:
                text = self.FONT1.render(line, True, BLACK)
                self.screen.blit(text, (100, y_pos))
                y_pos += text.get_height() + 10  # 行间距

    def draw_sidebar(self):
        """绘制侧边栏"""
        pg.draw.rect(self.screen, GRAY, (self.sidebar_x, 0, self.sidebar_width, self.sidebar_height))

        # 绘制侧边栏中的拖动按钮（黑色长方形）
        pg.draw.rect(self.screen, BLACK, (self.sidebar_x, self.button_y, self.sidebar_width, self.sidebar_button_height))

    # 处理鼠标滚轮
    def handle_scroll(self, event):
        """处理滚动事件"""
        if event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 4:  # 滚轮向上
                self.scroll_offset = max(self.scroll_offset - 20, 0)
            elif event.button == 5:  # 滚轮向下
                self.scroll_offset = min(self.scroll_offset + 20, self.max_scroll)

            # 更新按钮位置：根据scroll_offset调整按钮的Y位置
            self.update_sidebar_button_position()

    def update_sidebar_button_position(self):
        """根据scroll_offset更新按钮位置"""

        # 假设文档最大滚动偏移量为3500, 侧边栏按钮的位置也会在这个范围内变化
        self.button_y = (self.scroll_offset / self.max_scroll) * (self.sidebar_height - self.sidebar_button_height)
        self.button_y = max(0, min(self.sidebar_height - self.sidebar_button_height, self.button_y))

    # 处理鼠标拖动
    def handle_sidebar_drag(self, event):
        """处理侧边栏拖动"""
        if event.type == pg.MOUSEBUTTONDOWN:
            # 检查是否点击了拖动按钮
            if (self.sidebar_x <= event.pos[0] <= self.sidebar_x + self.sidebar_width and
                self.button_y <= event.pos[1] <= self.button_y + self.sidebar_button_height):
                self.dragging_sidebar = True
                self.mouse_y_start = event.pos[1]  # 记录开始拖动时的鼠标位置

        if event.type == pg.MOUSEBUTTONUP:
            self.dragging_sidebar = False

        if event.type == pg.MOUSEMOTION:
            if self.dragging_sidebar:
                # 更新拖动按钮的Y位置
                delta_y = event.pos[1] - self.mouse_y_start  # 鼠标移动的距离
                new_button_y = self.button_y + delta_y
                # 限制拖动按钮的范围在侧边栏内
                self.button_y = max(0, min(self.sidebar_height - self.sidebar_button_height, new_button_y))
                self.mouse_y_start = event.pos[1]  # 更新拖动起始位置

                # 更新滚动偏移量：根据按钮的位置来调整文档的滚动
                # 将按钮的Y位置映射到滚动偏移量
                self.scroll_offset = (self.button_y / (self.sidebar_height - self.sidebar_button_height)) * self.max_scroll
                self.scroll_offset = max(0, min(self.scroll_offset, self.max_scroll))  # 确保scroll_offset在合理范围内

    def run(self):
        """运行帮助文档界面"""
        running = True
        while running:
            self.screen.blit(self.background, (0, 0))  # 绘制背景图

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    running = False
                self.handle_scroll(event)  # 处理滚动事件
                self.handle_sidebar_drag(event)  # 处理侧边栏拖动
                if self.back_button.Active():
                    return

            # 绘制文档内容和侧边栏
            self.draw_document()
            self.draw_sidebar()

            self.back_button.draw()  # 绘制返回按钮

            # 更新显示
            pg.display.flip()
