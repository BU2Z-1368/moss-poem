from typing import Any
import pygame
import sys
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
    background_color: tuple,
    scroll_y: int,
) -> None:
    """
    Render the poem on the screen.

    Args:
        screen (pygame.Surface): The pygame surface to render on.
        poem_text (str): The text of the poem.
        font (pygame.font.Font): The font to use for rendering.
        text_color (tuple): The color of the text.
        background_image (tuple): The color of the background.
        scroll_y (int): The y-coordinate for scrolling.
    """
    screen.fill(background_color)
    screen.fill(background_image)

    # Split the poem into lines and render each line
    poem_lines = poem_text.split("\n")
    screen_width = screen.get_width()
    for i, line in enumerate(poem_lines):
        text_surface = font.render(line, True, text_color)
        text_width = text_surface.get_width()
        x = (screen_width - text_width) // 2  # Center the text horizontally
        screen.blit(text_surface, (x, scroll_y + i * 50))

    pygame.display.flip()


def main():
    # Initialize PyGame
    pygame.init()

    # Set up the display window
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    height = screen.get_height()
    pygame.display.set_caption("AI Generated Poem")

    # Set font and colors
    font = pygame.font.Font(None, 40)  # Choose a nicer font if desired
    text_color = (255, 255, 255)  # White text
    background_image = pygame.image.load('background.jpg')
    background_image = pygame.transform.scale(background_image, (screen.get_width(), screen.get_height()))

    # Generate poem text
    prompt = "Write a poem from the perspective of a moss plant."
    poem_text = generate_poem(prompt)

    # Scrolling setup
    scroll_y = height  # Start position at bottom of screen

    # Main game loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    # Clear the screen
                    screen.fill(background_image)
                    pygame.display.flip()
                    # Generate a new poem when Enter key is pressed
                    poem_text = generate_poem(prompt)
                    # Reset scroll position
                    scroll_y = height

                # press key to exit
                elif event.key == pygame.K_ESCAPE:
                    running = False

        # Update text position
        scroll_y -= 2  # Adjust scrolling speed
        if scroll_y < -len(poem_text.split("\n")) * 50:
            scroll_y = height  # Reset scroll position

        # Render the poem
        render_poem(screen, poem_text, font, text_color, background_image, scroll_y)

        # Adjust update frequency for smooth scrolling
        pygame.time.delay(50)

    # Quit PyGame
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
