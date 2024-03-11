import os
import sys

import pygame
import requests

# spn = 30
spn_x = 30
spn_y = 30
x, y = 100, -30
pygame.init()
screen = pygame.display.set_mode((600, 450))
count = 0
sp = ['sat', 'map', 'sat,skl']

def reserch_button():
    screen = pygame.display.set_mode((600, 450))
    font = pygame.font.Font(None, 32)
    clock = pygame.time.Clock()
    input_box = pygame.Rect(100, 100, 140, 32)
    color_inactive = pygame.Color('lightskyblue3')
    color_active = pygame.Color('dodgerblue2')
    color = color_inactive
    active = False
    text = ''
    done = False

    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                # If the user clicked on the input_box rect.
                if input_box.collidepoint(event.pos):
                    # Toggle the active variable.
                    active = not active
                else:
                    active = False
                # Change the current color of the input box.
                color = color_active if active else color_inactive
            if event.type == pygame.KEYDOWN:
                if active:
                    if event.key == pygame.K_RETURN:
                        print(text)
                        text = ''
                        done = True
                    elif event.key == pygame.K_BACKSPACE:
                        text = text[:-1]
                    else:
                        text += event.unicode

        screen.fill((30, 30, 30))
        # Render the current text.
        txt_surface = font.render(text, True, color)
        # Resize the box if the text is too long.
        width = max(200, txt_surface.get_width() + 10)
        input_box.w = width
        # Blit the text.
        screen.blit(txt_surface, (input_box.x + 5, input_box.y + 5))
        # Blit the input_box rect.
        pygame.draw.rect(screen, color, input_box, 2)

        pygame.display.flip()
        clock.tick(30)


def zapros(x, y, spn_x, spn_y, kind):
    map_request = f"http://static-maps.yandex.ru/1.x/?ll={x},{y}&spn={spn_x},{spn_y}&l={kind}"
    response = requests.get(map_request)

    if not response:
        print("Ошибка выполнения запроса:")
        print(map_request)
        print("Http статус:", response.status_code, "(", response.reason, ")")
        sys.exit(1)

    # Запишем полученное изображение в файл.
    map_file = "map.png"
    with open(map_file, "wb") as file:
        file.write(response.content)

    # Рисуем картинку, загружаемую из только что созданного файла.
    screen.blit(pygame.image.load(map_file), (0, 0))
    # Переключаем экран и ждем закрытия окна.
    pygame.display.flip()
    # Удаляем за собой файл с изображением.
    os.remove(map_file)


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            break
        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_PAGEUP:
                spn_x, spn_y = spn_x - 10, spn_y - 10

            if event.key == pygame.K_PAGEDOWN:
                spn_x, spn_y = spn_x + 10, spn_y + 10

            if event.key == pygame.K_UP:
                if not y == 80:
                    y += 10

            if event.key == pygame.K_DOWN:
                if not y == -80:
                    y -= 10
            if event.key == pygame.K_LEFT:
                if not x == -180:
                    x -= 10
            if event.key == pygame.K_RIGHT:
                if not x == 170:
                    x += 10
            if event.key == pygame.K_4:
                if count >= 2:
                    count = 0
                else:
                    count += 1
            if event.key == pygame.K_5:
                reserch_button()

    zapros(x, y, spn_x, spn_y, sp[count])

    pygame.display.flip()





# zapros(116.164042,-35.237191, 30, 32)
