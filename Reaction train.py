import pygame
import random
import time
import sys

pygame.init()

WHITE = (255, 255, 255)
DARK_YELLOW = (218, 132, 16)
DARK_PURPLE = (128, 0, 128)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
DARK_GRAY = (54, 54, 54)
LIGHT_GRAY = (120, 120, 120)

font = pygame.font.Font(None, 60)
button_font = pygame.font.Font(None, 40)
input_font = pygame.font.Font(None, 60)

screen_info = pygame.display.Info()
screen_width = screen_info.current_w
screen_height = screen_info.current_h

screen = pygame.display.set_mode((screen_width, screen_height), pygame.FULLSCREEN)
pygame.display.set_caption("Treinamento de Reação")

is_light_theme = True
background_color = WHITE
text_color = BLACK

def draw_text(text, font, color, surface, x, y, align="center"):
    textobj = font.render(text, True, color)
    textrect = textobj.get_rect()
    if align == "center":
        textrect.center = (x, y)
    elif align == "left":
        textrect.midleft = (x, y)
    elif align == "top":
        textrect.midtop = (x, y)
    surface.blit(textobj, textrect)

def reaction_test(reaction_time, target_color, use_circle, random_position):
    running = True
    while running:
        screen.fill(background_color)
        draw_text(f'Tempo de Reação:', font, text_color, screen, screen_width // 2, 100)
        draw_text(f'{reaction_time} ms', font, text_color, screen, screen_width // 2, 140)

        back_button_rect = pygame.Rect(screen_width - 150, screen_height - 100, 140, 60)
        pygame.draw.rect(screen, text_color, back_button_rect, 2)
        draw_text('Voltar', button_font, text_color, screen, back_button_rect.centerx, back_button_rect.centery)

        pygame.display.update()

        clicked_early = False
        start_time = pygame.time.get_ticks()
        random_delay = random.uniform(1, 5) * 1000

        while pygame.time.get_ticks() - start_time < random_delay:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if back_button_rect.collidepoint(event.pos):
                        return True
                    clicked_early = True
                    break

            if clicked_early:
                break

        if clicked_early:
            screen.fill(background_color)
            draw_text('Você clicou cedo demais!', font, RED, screen, screen_width // 2, screen_height // 2)
            pygame.display.update()
            time.sleep(0.5)
            continue

        if use_circle:
            screen.fill(background_color)
            if random_position:
                circle_x = random.randint(50, screen_width - 50)
                circle_y = random.randint(50, screen_height - 50)
            else:
                circle_x = screen_width // 2
                circle_y = screen_height // 2
            pygame.draw.circle(screen, target_color, (circle_x, circle_y), 25)
        else:
            screen.fill(target_color)
        
        pygame.display.update()
        start_time = pygame.time.get_ticks()
        clicked = False

        while pygame.time.get_ticks() - start_time < reaction_time:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if back_button_rect.collidepoint(event.pos):
                        return True
                    clicked = True
                    break

        screen.fill(background_color)
        pygame.display.update()

        if clicked:
            draw_text('Você acertou!', font, GREEN, screen, screen_width // 2, screen_height // 2)
        else:
            draw_text('Você errou!', font, RED, screen, screen_width // 2, screen_height // 2)

        pygame.display.update()
        time.sleep(0.7)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

def draw_start_screen(input_rect, user_text, cursor_visible, play_button_rect):
    screen.fill(background_color)
    global color_buttons, theme_button_rect, use_circle_checkbox_rect, random_position_checkbox_rect

    color_buttons = []

    draw_text('@Lakevlr', button_font, text_color, screen, 100, 150, align="left")
    draw_text('@lenhartt1', button_font, text_color, screen, 100, 200, align="left")

    pygame.draw.rect(screen, LIGHT_GRAY, input_rect, 2)
    text_surface = input_font.render(user_text, True, text_color)
    screen.blit(text_surface, (input_rect.x + 10, input_rect.y + input_rect.height // 2 - text_surface.get_height() // 2))

    if cursor_visible:
        cursor_x = input_rect.x + 10 + input_font.size(user_text)[0]
        cursor_y = input_rect.centery
        pygame.draw.line(screen, text_color, (cursor_x, cursor_y - 25), (cursor_x, cursor_y + 25), 2)

    pygame.draw.rect(screen, LIGHT_GRAY, play_button_rect, 2)
    draw_text('Jogar!', button_font, text_color, screen, play_button_rect.centerx, play_button_rect.centery)

    color_button_width = 220
    color_button_height = 60

    start_x = screen_width - 400
    start_y = screen_height // 2 + 50

    color_options = [
        ("Amarelo", DARK_YELLOW),
        ("Roxo", DARK_PURPLE),
        ("Vermelho", RED)
    ]

    for i, (text, color) in enumerate(color_options):
        button_x = start_x - color_button_width // 2
        button_y = start_y + i * 100

        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect(midleft=(button_x + 10, button_y + color_button_height // 2))
        button_rect = pygame.Rect(button_x, button_y, color_button_width, color_button_height)
        color_buttons.append((button_rect, color))
        pygame.draw.rect(screen, text_color, button_rect, 2)
        screen.blit(text_surface, text_rect)

    theme_button_rect = pygame.Rect(screen_width - 250, 50, 150, 60)
    pygame.draw.rect(screen, text_color, theme_button_rect, 2)
    draw_text('Light' if is_light_theme else 'Dark', button_font, text_color, screen, theme_button_rect.centerx, theme_button_rect.centery)

    use_circle_checkbox_rect = pygame.Rect(screen_width // 2 - 100, screen_height // 2 + 200, 20, 20)
    pygame.draw.rect(screen, text_color, use_circle_checkbox_rect, 2)
    draw_text('Usar Esfera', button_font, text_color, screen, screen_width // 2 - 100 + 30, screen_height // 2 + 210, align="left")

    random_position_checkbox_rect = pygame.Rect(screen_width // 2 - 100, screen_height // 2 + 250, 20, 20)
    pygame.draw.rect(screen, LIGHT_GRAY if use_circle else DARK_GRAY, random_position_checkbox_rect, 2)
    draw_text('Esfera Aleatória', button_font, text_color, screen, screen_width // 2 - 100 + 30, screen_height // 2 + 260, align="left")

    if selected_color is None:
        draw_text('Escolha uma cor antes de jogar!', font, RED, screen, screen_width // 2, 100, align="center")

    if use_circle:
        pygame.draw.rect(screen, text_color, use_circle_checkbox_rect)

    if use_circle and random_position:
        pygame.draw.rect(screen, text_color, random_position_checkbox_rect)
    
    pygame.display.flip()

def toggle_theme():
    global is_light_theme, background_color, text_color
    is_light_theme = not is_light_theme
    if is_light_theme:
        background_color = WHITE
        text_color = BLACK
    else:
        background_color = DARK_GRAY
        text_color = WHITE

running = True
selected_color = None
message_displayed = True
user_text = ''
input_rect = pygame.Rect(screen_width // 2 - 150, screen_height // 4 - 150, 300, 60)
cursor_visible = False
cursor_timer = 0
use_circle = False
random_position = False

play_button_rect = pygame.Rect(screen_width // 2 - 100, screen_height // 2, 200, 60)

while running:
    draw_start_screen(input_rect, user_text, cursor_visible, play_button_rect)
    cursor_timer += pygame.time.Clock().tick(30)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if theme_button_rect.collidepoint(event.pos):
                toggle_theme()
            for button_rect, color in color_buttons:
                if button_rect.collidepoint(event.pos):
                    selected_color = color
                    message_displayed = False
            if play_button_rect.collidepoint(event.pos):
                try:
                    reaction_time = int(user_text)
                    if selected_color is not None:
                        if reaction_test(reaction_time, selected_color, use_circle, random_position):
                            running = True
                        else:
                            running = False
                except ValueError:
                    pass
            elif input_rect.collidepoint(event.pos):
                cursor_visible = True
            elif use_circle_checkbox_rect.collidepoint(event.pos):
                use_circle = not use_circle
                if not use_circle:
                    random_position = False
            elif random_position_checkbox_rect.collidepoint(event.pos):
                if use_circle:
                    random_position = not random_position
            else:
                cursor_visible = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
            if event.key == pygame.K_BACKSPACE:
                user_text = user_text[:-1]
            elif event.key == pygame.K_RETURN:
                try:
                    reaction_time = int(user_text)
                    if selected_color is not None:
                        if reaction_test(reaction_time, selected_color, use_circle, random_position):
                            running = True
                        else:
                            running = False
                except ValueError:
                    pass
            else:
                user_text += event.unicode

    if cursor_timer >= 500:
        cursor_visible = not cursor_visible
        cursor_timer = 0

pygame.quit()
