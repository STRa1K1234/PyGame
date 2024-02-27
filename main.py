import random
import sys

import pygame

check_list = []


def normalize_city_name(name):
    return name.strip().lower().replace('ё', 'е')

cache = set()
cities = {normalize_city_name(x) for x in open("cities.txt", encoding="utf-8").readlines() if x.strip()}

def find_city(last_letter):
    for city in cities:
        if city[0].lower() == last_letter:
            return city
    return None

def get_last_letter(city):
    if city[-1].lower() in ["ъ", "ь", "й", "ц", "ы"]:
        return city[-2].lower()
    else:
        return city[-1].lower()

pygame.init()

# Устанавливаем размеры окна
WINDOW_SIZE = (800, 600)
screen = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption("Города")
font = pygame.font.SysFont("Arial", 24)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

with open('cities.txt', encoding='utf8') as file:
    city_random = file.readlines()

computer_text = random.choice(city_random).strip()
used_cities = [computer_text.lower()]


def load_cities(filename='cities.txt'):
    with open(filename, encoding='utf-8') as file:
        cities = [city.strip().lower() for city in file]
    return cities


cities = load_cities()


def get_next_city(letter):
    possible_cities = [city for city in cities if city[0] == letter]
    for city in possible_cities:
        if city not in used_cities:
            return city
    return None


running = True
input_text = ""

# Создание стартового окна
start_screen = True

while start_screen:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                start_screen = False
                last_letter = computer_text[-1].lower() if computer_text[-1].lower() not in ["ъ", "ь", "й", "ц", "ы"] else computer_text[-2].lower()
            elif event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()

    screen.fill(BLACK)

    city_text = font.render("Города", True, (WHITE))
    city_text_rect = city_text.get_rect(center=(WINDOW_SIZE[0] // 2, (WINDOW_SIZE[1] // 2) - 100))
    screen.blit(city_text, city_text_rect)

    start_text = font.render("Нажмите Пробел, чтобы начать игру", True, (WHITE))
    start_text_rect = start_text.get_rect(center=(WINDOW_SIZE[0] // 2, WINDOW_SIZE[1] // 2))
    screen.blit(start_text, start_text_rect)

    pygame.display.flip()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:  # Пользователь нажал "Enter"
                user_city = input_text.lower()
                if user_city and user_city[0] == computer_text[
                    -1] and user_city in cities and user_city not in used_cities:
                    used_cities.append(user_city)
                    computer_text = get_next_city(user_city[-1])
                    if computer_text is None:
                        print("Компьютер не смог найти город. Вы выиграли!")
                        running = False
                else:
                    print("Введите корректный город, начинающийся на букву", computer_text[-1].upper())

                input_text = ""

            elif event.key == pygame.K_BACKSPACE:
                input_text = input_text[:-1]

            else:
                input_text += event.unicode

    screen.fill((0, 0, 0))

    # Отображение вводного поля для города пользователя
    player_input_text = font.render("Введите город:", True, WHITE)
    player_input_rect = player_input_text.get_rect(center=(WINDOW_SIZE[0] // 2, WINDOW_SIZE[1] // 2 - 50))
    screen.blit(player_input_text, player_input_rect)

    text_surface = font.render(input_text, True, WHITE)
    text_rect = text_surface.get_rect(center=(WINDOW_SIZE[0] // 2, WINDOW_SIZE[1] // 2 + 20))
    screen.blit(text_surface, text_rect)

    # Отображение буквы, с которой должен начаться город пользователя
    start_letter = font.render(computer_text[-1].upper(), True, WHITE)
    start_letter_rect = start_letter.get_rect(center=(WINDOW_SIZE[0] // 4, WINDOW_SIZE[1] // 2))
    screen.blit(start_letter, start_letter_rect)

    chosen_city_text = font.render(computer_text, True, WHITE)
    chosen_city_rect = chosen_city_text.get_rect(center=(WINDOW_SIZE[0] // 2, (WINDOW_SIZE[1] // 2 - 150)))
    screen.blit(chosen_city_text, chosen_city_rect)

    pygame.display.flip()

# Выход из Pygame
pygame.quit()
sys.exit()


# TODO несуществующие букву в конце слов заменить на предпоследнюю