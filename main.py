# Uncharted Freefall

import pygame
import random

pygame.init()
pygame.mixer.init()
WIDTH = 500
HEIGHT = 800
fps = 60
timer = pygame.time.Clock()
huge_font = pygame.font.Font('assets/Terserah.ttf', 42)
font = pygame.font.Font('assets/Terserah.ttf', 24)
pygame.display.set_caption('Uncharted Freefall')
screen = pygame.display.set_mode([WIDTH, HEIGHT])
bg = (221, 87, 28)
game_over = False
clouds = [[200, 100, 1], [50, 330, 2], [350, 330, 3], [200, 670, 1]]
cloud_images = []
for i in range(1, 4):
    img = pygame.image.load(f'assets/clouds/cloud{i}.png')
    cloud_images.append(img)
# player variables
player_x = 240
player_y = 40
skydiver = pygame.transform.scale(pygame.image.load('assets/skydiver.png'), (100, 100))
direction = -1
y_speed = 0
gravity = 0.2
x_speed = 3
x_direction = 0
# score variables
score = 0
total_distance = 0
file = open('high_scores.txt', 'r')
read = file.readlines()
first_high = int(read[0])
high_score = first_high
# enemies
eagle = pygame.transform.scale(pygame.image.load('assets/obstacles/eagle.png'), (150, 75))
enemies = [[-234, random.randint(400, HEIGHT - 100), 1]]
# boxes
box = pygame.transform.scale(pygame.image.load('assets/obstacles/box.png'), (200, 100))
boxes = [[-234, random.randint(400, HEIGHT - 100), 1]]
# sounds and music
pygame.mixer.music.load('assets/fallbgm.mp3')
end_sound = pygame.mixer.Sound('assets/game_over.mp3')
pygame.mixer.music.play()
pygame.mixer.music.set_volume(0.4)


def draw_clouds(cloud_list, images):
    platforms = []
    for j in range(len(cloud_list)):
        image = images[cloud_list[j][2] - 1]
        platform = pygame.rect.Rect((cloud_list[j][0] + 5, cloud_list[j][1] + 40), (120, 10))
        screen.blit(image, (cloud_list[j][0], cloud_list[j][1]))
        #pygame.draw.rect(screen, 'gray', [cloud_list[j][0] + 5, cloud_list[j][1] + 40, 120, 3])
        platforms.append(platform)
    return platforms


def draw_player(x_pos, y_pos, player_img, direc):
    if direc == -1:
        player_img = pygame.transform.flip(player_img, False, True)
    screen.blit(player_img, (x_pos, y_pos))
    player_rect = pygame.rect.Rect((x_pos + 14, y_pos + 80), (72, 20))
    # pygame.draw.rect(screen, 'green', player_rect, 3)
    return player_rect


def draw_enemies(enemy_list, eagle_img):
    enemy_rects = []
    for j in range(len(enemy_list)):
        enemy_rect = pygame.rect.Rect((enemy_list[j][0] + 40, enemy_list[j][1] + 50), (100, 50))
        # pygame.draw.rect(screen, 'orange', enemy_rect, 3)
        enemy_rects.append(enemy_rect)
        if enemy_list[j][2] == 1:
            screen.blit(eagle_img, (enemy_list[j][0], enemy_list[j][1]))
        elif enemy_list[j][2] == -1:
            screen.blit(pygame.transform.flip(eagle_img, 1, 0), (enemy_list[j][0], enemy_list[j][1]))
    return enemy_rects

def draw_boxes(boxes_list, box_img):
    boxes_rects = []
    for j in range(len(boxes_list)):
        boxes_rect = pygame.rect.Rect((boxes_list[j][0] + 40, boxes_list[j][1] + 50), (175, 70))
        # pygame.draw.rect(screen, 'blue', enemy_rect, 3)
        boxes_rects.append(boxes_rect)
        if boxes_list[j][2] == 1:
            screen.blit(box_img, (boxes_list[j][0], boxes_list[j][1]))
        elif boxes_list[j][2] == -1:
            screen.blit(pygame.transform.flip(box_img, 1, 0), (boxes_list[j][0], boxes_list[j][1]))
    return boxes_rects


def move_enemies(enemy_list, current_score):
    enemy_speed = 2 + current_score//15
    for j in range(len(enemy_list)):
        if enemy_list[j][2] == 1:
            if enemy_list[j][0] < WIDTH:
                enemy_list[j][0] += enemy_speed
            else:
                enemy_list[j][2] = -1
        elif enemy_list[j][2] == -1:
            if enemy_list[j][0] > -235:
                enemy_list[j][0] -= enemy_speed
            else:
                enemy_list[j][2] = 1
        if enemy_list[j][1] < -100:
            enemy_list[j][1] = random.randint(HEIGHT, HEIGHT + 500)
    return enemy_list


def update_objects(cloud_list, play_y, enemy_list):
    lowest_cloud = 0
    update_speed = 10
    if play_y > 200:
        play_y -= update_speed
        for q in range(len(enemy_list)):
            enemy_list[q][1] -= update_speed
        for j in range(len(cloud_list)):
            cloud_list[j][1] -= update_speed
            if cloud_list[j][1] > lowest_cloud:
                lowest_cloud = cloud_list[j][1]
        if lowest_cloud < 750:
            num_clouds = random.randint(1, 2)
            if num_clouds == 1:
                x_pos = random.randint(0, WIDTH - 70)
                y_pos = random.randint(HEIGHT + 100, HEIGHT + 300)
                cloud_type = random.randint(1, 3)
                cloud_list.append([x_pos, y_pos, cloud_type])
            else:
                x_pos = random.randint(0, WIDTH / 2 - 70)
                y_pos = random.randint(HEIGHT + 100, HEIGHT + 300)
                cloud_type = random.randint(1, 3)
                x_pos2 = random.randint(WIDTH / 2 + 70, WIDTH - 70)
                y_pos2 = random.randint(HEIGHT + 100, HEIGHT + 300)
                cloud_type2 = random.randint(1, 3)
                cloud_list.append([x_pos, y_pos, cloud_type])
                cloud_list.append([x_pos2, y_pos2, cloud_type2])
    return play_y, cloud_list, enemy_list


run = True
while run:
    screen.fill(bg)
    timer.tick(fps)
    cloud_platforms = draw_clouds(clouds, cloud_images)
    player = draw_player(player_x, player_y, skydiver, direction)
    enemy_boxes = draw_enemies(enemies, eagle)
    enemies = move_enemies(enemies, score)
    player_y, clouds, enemies = update_objects(clouds, player_y, enemies)
    if game_over:
        end_text = huge_font.render('Uncharted Freefall', True, 'black')
        end_text2 = font.render('Game Over: Press Enter to fall again!', True, 'cyan')
        screen.blit(end_text, (70, 20))
        screen.blit(end_text2, (48, 80))
        player_y = - 300
        y_speed = 0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                x_direction = -1
            elif event.key == pygame.K_RIGHT:
                x_direction = 1
            if event.key == pygame.K_RETURN and game_over:
                game_over = False
                player_x = 240
                player_y = 40
                direction = -1
                y_speed = 0
                x_direction = 0
                score = 0
                total_distance = 0
                enemies = [[-234, random.randint(400, HEIGHT - 100), 1]]
                clouds = [[200, 100, 1], [50, 330, 2], [350, 330, 3], [200, 670, 1]]
                pygame.mixer.music.play()

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                x_direction = 0
            elif event.key == pygame.K_RIGHT:
                x_direction = 0

    if y_speed < 10 and not game_over:
        y_speed += gravity
    player_y += y_speed
    if y_speed < 0:
        direction = 1
    else:
        direction = -1
    player_x += x_speed * x_direction
    if player_x > WIDTH:
        player_x = -30
    elif player_x < -50:
        player_x = WIDTH - 20

    for i in range(len(enemy_boxes)):
        if player.colliderect(enemy_boxes[i]) and not game_over:
            end_sound.play()
            game_over = True
            if score > first_high:
                file = open('high_scores.txt', 'w')
                write_score = str(score)
                file.write(write_score)
                file.close()
                first_high = score

    total_distance += y_speed
    score = round(total_distance / 100)
    score_text = font.render(f'Score: {score}', True, 'black')
    screen.blit(score_text, (10, HEIGHT - 70))
    if score > high_score:
        high_score = score
    score_text2 = font.render(f'High Score: {high_score}', True, 'black')
    screen.blit(score_text2, (10, HEIGHT - 40))

    pygame.display.flip()
pygame.quit()