import pygame
import sys
from transformers import pipeline

# 初始化pygame
pygame.init()

# 设置窗口
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('AI Generated Poem')

# 设置字体和颜色
font = pygame.font.Font(None, 40)  # 可以选择更好看的字体
text_color = (255, 255, 255)  # 白色字体
background_color = (0, 0, 0)  # 黑色背景

# 加载GPT-2模型
generator = pipeline('text-generation', model='gpt2')

# 生成诗歌
def generate_poem(prompt: str, max_length: int = 100) -> str:
    """Generate a poem using the GPT-2 model."""
    poems = generator(prompt, max_length=max_length, num_return_sequences=1)
    return poems[0]['generated_text']

# 生成诗歌文本
poem_text = generate_poem("Ode to the night,", max_length=150)
poem_lines = poem_text.split('\n')
rendered_text = [font.render(line, True, text_color) for line in poem_lines]

# 滚动设置
scroll_y = height  # 开始位置在屏幕底部

# 游戏主循环
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # 填充背景
    screen.fill(background_color)
    
    # 更新文本位置
    scroll_y -= 2  # 调整滚动速度
    if scroll_y < -len(rendered_text) * 50:
        scroll_y = height  # 重置滚动位置
    
    # 渲染文本
    for i, text_surface in enumerate(rendered_text):
        screen.blit(text_surface, (50, scroll_y + i * 50))  # 调整行间距
    
    # 更新屏幕显示
    pygame.display.flip()
    pygame.time.delay(50)  # 调整更新频率以控制滚动的平滑性

# 退出pygame
pygame.quit()
sys.exit()
