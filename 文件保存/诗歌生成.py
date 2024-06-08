import pygame
import sys
import openai
import time
from typing import Tuple

def fetch_poem(api_key: str) -> str:
    """Fetch a poem from OpenAI with rate limit handling."""
    client = openai.OpenAI(
        base_url="https://gtapi.xiaoerchaoren.com:8932/v1",
        api_key=api_key
    )
    attempt = 0
    while attempt < 5:
        try:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": "Generate a poem."}
                ]
            )
            poem = response.choices[0].message.content
            return poem
        except openai.RateLimitError:
            print("Rate limit reached, retrying in 30 seconds...")
            time.sleep(30)  # Wait 30 seconds before retrying
            attempt += 1
    return "Failed to fetch poem due to rate limits. Please try again later."

def main(api_key: str):
    """Main function to create the display and handle events."""
    pygame.init()
    screen = pygame.display.set_mode((800, 600), pygame.RESIZABLE)
    pygame.display.set_caption('Poem Display')
    font = pygame.font.SysFont("timesnewroman", 30)
    black = (0, 0, 0)
    white = (255, 255, 255)

    poem = ''
    text_height = font.get_linesize() + 15
    scroll_y = 600
    start_scrolling = False
    fullscreen = False

    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type is pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if not start_scrolling:
                        poem = fetch_poem(api_key)
                        scroll_y = 600
                        start_scrolling = True
                    else:
                        start_scrolling = False
                elif event.key == pygame.K_F11:
                    fullscreen = not fullscreen
                    if fullscreen:
                        screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
                    else:
                        screen = pygame.display.set_mode((800, 600), pygame.RESIZABLE)
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

        if start_scrolling:
            screen.fill(black)
            y_offset = scroll_y
            for line in poem.split('\n'):
                text_surface = font.render(line, True, white)
                text_x = (screen.get_width() - text_surface.get_width()) // 2
                screen.blit(text_surface, (text_x, y_offset))
                y_offset += text_height

            scroll_y -= 1  # Reduced speed of scrolling
            if y_offset < 0:  # Reset scroll to loop
                scroll_y = 600

        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    api_key = "sk-B3Y7GWocZpSn6Vux45296358Bd4642BcAd61Cd5419E1F0Df"
    main(api_key)
