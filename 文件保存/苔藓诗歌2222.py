import pygame
import sys

def render_poem(
    screen: pygame.Surface,
    poem_text: str,
    font: pygame.font.Font,
    text_color: tuple,
    background_image: pygame.Surface,
    scroll_y: int,
) -> None:
    """
    Render the poem on the screen with a background image.

    Args:
        screen (pygame.Surface): The pygame surface to render on.
        poem_text (str): The text of the poem.
        font (pygame.font.Font): The font to use for rendering.
        text_color (tuple): The color of the text.
        background_image (pygame.Surface): The background image surface.
        scroll_y (int): The y-coordinate for scrolling.
    """
    # Blit the background image
    screen.blit(background_image, (0, 0))

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
    pygame.init()
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    height = screen.get_height()
    pygame.display.set_caption("AI Generated Poem")

    # Load the background image
    background_image = pygame.image.load('background.jpg')
    background_image = pygame.transform.scale(background_image, (screen.get_width(), screen.get_height()))

    font = pygame.font.Font(None, 40)
    text_color = (255, 255, 255)

    prompt = "Write a poem from the perspective of a moss plant."
    poem_text = generate_poem(prompt)

    scroll_y = height
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    poem_text = generate_poem(prompt)
                    scroll_y = height
                elif event.key == pygame.K_ESCAPE:
                    running = False

        scroll_y -= 2
        if scroll_y < -len(poem_text.split("\n")) * 50:
            scroll_y = height

        render_poem(screen, poem_text, font, text_color, background_image, scroll_y)
        pygame.time.delay(50)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
