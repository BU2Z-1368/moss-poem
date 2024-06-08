import pygame
import sys
from typing import Any
from openai import OpenAI

# Initialize the OpenAI client
client = OpenAI(
    base_url="https://gtapi.xiaoerchaoren.com:8932/v1",
    api_key="sk-B3Y7GWocZpSn6Vux45296358Bd4642BcAd61Cd5419E1F0Df",
)

def generate_poem(prompt: str) -> str:
    """
    Generates text based on the given prompt using the GPT-3.5 model.

    Args:
        prompt (str): The input prompt for text generation.

    Returns:
        str: The generated text.
    """
    response: Any = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": "You are a poet. Create a short poem based on the following prompt.",
            },
            {"role": "user", "content": prompt},
        ],
    )
    return response.choices[0].message.content.strip()

def render_poem(
    screen: pygame.Surface,
    poem_text: str,
    font: pygame.font.Font,
    text_color: tuple,
    background_image: pygame.Surface,
    scroll_x: int
) -> None:
    """
    Render the poem on the screen with horizontal scrolling from right to left.

    Args:
        screen (pygame.Surface): The pygame surface to render on.
        poem_text (str): The text of the poem.
        font (pygame.font.Font): The font to use for rendering.
        text_color (tuple): The color of the text.
        background_image (pygame.Surface): The background image to display.
        scroll_x (int): The x-coordinate for scrolling.
    """
    screen.blit(background_image, (0, 0))

    # Split the poem into lines and render each line vertically rotated
    poem_lines = poem_text.split("\n")
    screen_height = screen.get_height()
    for i, line in enumerate(poem_lines):
        text_surface = font.render(line, True, text_color)
        text_surface = pygame.transform.rotate(text_surface, 90)  # Rotate the text surface by 90 degrees clockwise
        text_height = text_surface.get_height()
        y = (screen_height - text_height) // 2  # Center the text vertically
        screen.blit(text_surface, (scroll_x + i * 50, y))

    pygame.display.flip()

def main():
    pygame.init()
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    width = screen.get_width()
    height = screen.get_height()
    pygame.display.set_caption("AI Generated Poem")

    font = pygame.font.Font(None, 40)
    text_color = (255, 255, 255)

    # Load and rotate the background image
    background_image = pygame.image.load("D:/VSCODE/文件保存/moss background.webp").convert()
    background_image = pygame.transform.rotate(background_image, 90)  # Rotate the background image by 90 degrees clockwise
    background_image = pygame.transform.scale(background_image, (width, height))  # Scale the rotated image to fit the screen

    prompt = "Write a poem from the perspective of a moss plant."
    poem_text = generate_poem(prompt)

    scroll_x = width  # Start position at the right edge of the screen

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    screen.blit(background_image, (0, 0))
                    pygame.display.flip()
                    poem_text = generate_poem(prompt)
                    scroll_x = width

                elif event.key is pygame.K_ESCAPE:
                    running = False

        scroll_x -= 2  # Adjust scrolling speed
        if scroll_x < -len(poem_text.split("\n")) * 50:
            scroll_x = width  # Reset scroll position

        render_poem(screen, poem_text, font, text_color, background_image, scroll_x)

        pygame.time.delay(50)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
