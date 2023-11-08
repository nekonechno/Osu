import pygame
import random
import time




pygame.init()
pygame.mixer.init()

pygame.mixer.music.load('01_-_vivid.mp3')
pygame.mixer.music.set_volume(0.1)
pygame.mixer.music.play()


SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Define the original and current resolutions
original_resolution = (512, 384)
current_resolution = (SCREEN_WIDTH, SCREEN_HEIGHT)

def scale_coordinates(coords, original_resolution, current_resolution):
    scale_x = current_resolution[0] / original_resolution[0]
    scale_y = current_resolution[1] / original_resolution[1]
    scaled_coords = [(int(x * scale_x), int(y * scale_y), time_ms) for x, y, time_ms in coords]
    return scaled_coords

def load_osu_data(file_path, current_resolution):
    read_hit_objects = False
    read_sliders = False
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    hit_objects = []
    sliders = []
    for line in lines:
        if line.startswith("[HitObjects]"):
            read_hit_objects = True
        elif line.startswith("[SliderPoints]"):
            read_sliders = True
            read_hit_objects = False
        elif read_hit_objects:
            parts = line.strip().split(",")
            x = int(parts[0])
            y = int(parts[1])
            time_ms = int(parts[2])
            hit_objects.append((x, y, time_ms))
        elif read_sliders:
            parts = line.strip().split(",")
            x = int(parts[0])
            y = int(parts[1])
            time_ms = int(parts[2])
            sliders.append((x, y, time_ms))

    original_resolution = (512, 384)

    scaled_hit_objects = scale_coordinates(hit_objects, original_resolution, current_resolution)
    scaled_sliders = scale_coordinates(sliders, original_resolution, current_resolution)

    return scaled_hit_objects, scaled_sliders


osu_data, sliders = load_osu_data("FAIRY FORE - Vivid (Hitoshirenu Shourai) [Normal].osu",current_resolution)





circle_color = (255, 255, 255)
score = 0

time_circle_radius = 10
time_circle_color = (148, 255, 225)

HP = 100
hp_bar_width = 200
hp_bar_height = 20
hp_bar_x = 10
hp_bar_y = 10

misses = 0
hits_50 = 0
hits_100 = 0
hits_300 = 0

background_image = pygame.image.load('Chocobos.jpg')
background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
def draw_circle(position):
    pygame.draw.circle(screen, (10,10,10), position, circle_radius)
    pygame.draw.circle(screen, circle_color, position, circle_radius, width=2)

def draw_slider(positions):
    pygame.draw.lines(screen, circle_color, False, positions, width=2)





def draw_time_circle(position, radius):
    pygame.draw.circle(screen, time_circle_color, position, radius, width=2)

def draw_hp_bar():
    border_radius = 10  # Радиус скругления углов
    pygame.draw.rect(screen, (255, 0, 0), (hp_bar_x, hp_bar_y, hp_bar_width, hp_bar_height), border_radius=border_radius)
    fill_width = int((HP / 100) * hp_bar_width)
    pygame.draw.rect(screen, (0, 255, 0), (hp_bar_x, hp_bar_y, fill_width, hp_bar_height), border_radius=border_radius)

running = True
time_last_change = pygame.time.get_ticks()  # Время последней смены круга


combo = 0
combo_font = pygame.font.Font(None, 36)
score_multiplier = 1


scaled_osu_data = scale_coordinates(osu_data, original_resolution, (SCREEN_WIDTH, SCREEN_HEIGHT))


current_object_index = 0

def get_approach_rate(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
        for line in lines:
            if line.startswith("ApproachRate"):
                return float(line.split(":")[1].strip())
    return 5.0


circle_display_time = int(1200 + (600 * (5 - get_approach_rate("FAIRY FORE - Vivid (Hitoshirenu Shourai) [Normal].osu"))/5))

def get_CS(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
        for line in lines:
            if line.startswith("CircleSize"):
                return float(line.split(":")[1].strip())
circle_radius = int(54.4 - 4.48 * get_CS("FAIRY FORE - Vivid (Hitoshirenu Shourai) [Normal].osu"))


while running:

    screen.fill((0, 0, 0))
    screen.blit(background_image, (0,0))
    draw_hp_bar()

    for slider in sliders:
        slider_positions = [(slider[0], slider[1])]
        object_x, object_y = sliders
        for _ in range(5):
            new_x = object_x + random.randint(-50, 50)
            new_y = object_y + random.randint(-50, 50)
            slider_positions.append((new_x, new_y))
            object_x, object_y = new_x, new_y
        draw_slider(slider_positions)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN and (event.button == 1 or event.button == 3):
            mouse_x, mouse_y = pygame.mouse.get_pos()
            if current_object_index < len(osu_data):
                object_x, object_y, _ = osu_data[current_object_index]
                distance = ((mouse_x - object_x) ** 2 + (mouse_y - object_y) ** 2) ** 0.5
                if distance <= circle_radius:
                    current_object_index += 1
                    click_duration = pygame.time.get_ticks() - time_last_change  # Продолжительность нажатия

                    if click_duration < circle_display_time/1.5:
                        HP += 5
                        combo += 1
                        if combo >= 1:
                            score += int(50 * score_multiplier)
                            score_multiplier += 0.0001
                        else:
                            score += 50

                        hits_50 += 1
                    elif circle_display_time/1.5 < circle_display_time/2.5:
                        HP += 3
                        combo += 1
                        if combo >= 1:
                            score += int(100 * score_multiplier)
                            score_multiplier += 0.0001
                        else:
                            score += 100

                        hits_100 += 1
                    else:
                        HP += 1
                        combo +=1
                        if combo >= 1:
                            score += int(300 * score_multiplier)
                            score_multiplier += 0.0001
                        else:
                            score += 300

                        hits_300 += 1
                    if HP > 100:
                        HP = 100
                    time_last_change = pygame.time.get_ticks()
                else:
                    combo = 0
                    HP -= 10
                    misses+=1



    if current_object_index < len(osu_data):
        object_x, object_y, _ = osu_data[current_object_index]
        draw_circle((object_x, object_y))

    # Рисуем time_circle с уменьшающимся радиусом
    time_elapsed = pygame.time.get_ticks() - time_last_change
    if 0 <= time_elapsed < circle_display_time:
        time_circle_radius = 60 - int(30 * (time_elapsed / circle_display_time))
        draw_time_circle((object_x, object_y), time_circle_radius)

    # Отображаем комбо
    if combo > 0:
        combo_text = combo_font.render(f'X{combo}', True, (255, 255, 255))
        screen.blit(combo_text, (10, SCREEN_HEIGHT - 40))




    font = pygame.font.Font(None, 72)
    font_accuracy = pygame.font.Font(None, 36)
    score_text = font.render(f'{str(score).zfill(6)}', True, (255, 255, 255))
    screen.blit(score_text, (SCREEN_WIDTH - 190, SCREEN_HEIGHT - (SCREEN_HEIGHT - 10)))

    if pygame.time.get_ticks() - time_last_change > circle_display_time:
        combo = 0
        HP = HP - 10
        current_object_index += 1
        if current_object_index < len(osu_data):
            object_x, object_y, _ = osu_data[current_object_index]
        time_last_change = pygame.time.get_ticks()  # Обновляем время последней смены круга
    total_hits = misses + hits_50 + hits_100 + hits_300
    total_score = hits_50 * 50 + hits_100 * 100 + hits_300 * 300

    if total_hits > 0:
        accuracy = (total_score / (total_hits * 300)) * 100
        accuracy_text = font_accuracy.render(f'{accuracy:.2f}%', True, (255, 255, 255))
        screen.blit(accuracy_text, (SCREEN_WIDTH - 80, SCREEN_HEIGHT - (SCREEN_HEIGHT - 60)))

    pygame.display.flip()
    pygame.time.Clock().tick(60)

    if HP <= 0 or (len(osu_data) == total_hits):
        pygame.mixer.music.stop()
        pygame.quit()

pygame.quit()