

import pygame
import os
################################################
# 기본 초기화
pygame.init()

# 화면 크기 설정
screen_width = 640  # 가로
screen_height = 480  # 세로
screen = pygame.display.set_mode((screen_width, screen_height))

# 화면 타이틀 설정
pygame.display.set_caption("Minigame_PANG_Game")

# FPS
clock = pygame.time.Clock()

################################################
# 1. 사용자 게임 초기화 ( 배경화면, 이미지, 좌표,속도, 폰트)
current_path = os.path.dirname(__file__)  # os 모듈을 이용해 현재 파일의 위치 반환
image_path = os.path.join(current_path, 'images')  # images 폴더 위치 반환

# background setting
background = pygame.image.load(os.path.join(image_path, 'background.png'))

# stage setting (배경 위에 스테이지가 있고 그 안에서 캐릭터가 움직이게 됨)
stage = pygame.image.load(os.path.join(image_path, 'stage.png'))
stage_size = stage.get_rect().size
stage_height = stage_size[1]  # 스테이지 높이 위에 캐릭터를 두기 위해 사용함
# character setting
character = pygame.image.load(os.path.join(image_path, 'character.png'))
character_size = character.get_rect().size
character_width = character_size[0]
character_height = character_size[1]
character_x = (screen_width / 2) - (character_width / 2)
character_y = (screen_height) - (stage_height+character_height)

# -- character move, speed
char_move_x = 0
char_speed = 3

# -- weapon setting --
weapon = pygame.image.load(os.path.join(image_path, 'weapon.png'))
weapon_size = weapon.get_rect().size
weapon_width = weapon_size[0]

# -- 무기는 여러발 동시에 타격이 가능 함 --(리스트로 관리)
weapons = []

# 무기 발사 속도
weapon_speed = 5

#  -- game ball setting ---
# ball은 총 4개  160 / 80 / 40 / 20
ball_images = [
    pygame.image.load(os.path.join(image_path, 'ball1.png')),
    pygame.image.load(os.path.join(image_path, 'ball2.png')),
    pygame.image.load(os.path.join(image_path, 'ball3.png')),
    pygame.image.load(os.path.join(image_path, 'ball4.png'))
]

# 공 크기에 따른 최초 스피드 처리
ball_speed_y = [-18, -15, -12, -9]

# balls 점점 쪼개짐
balls = []

# 최초 발생하는 큰 공 추가
balls.append({
    "x": 50,  # 공 x 좌표  , 딕셔너리로 처리
    "y": 50,
    "img_idx": 0,  # 공 이미지의 index
    "to_x": 3,  # 공의 x축 이동 방향,  -3이면 lf , 3이면 rf
    "to_y": -6,  # 공의 y축 이동 방향
    "init_speed_y": ball_speed_y[0]  # y 최초 속도
})

running = True
while running:
    dt = clock.tick(60)

    # 2. 이벤트 처리 ( 키보드, 마우스 등)
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            running = False
        if e.type == pygame.KEYDOWN:
            if e.key == pygame.K_LEFT:
                char_move_x -= char_speed
            elif e.key == pygame.K_RIGHT:
                char_move_x += char_speed
            elif e.key == pygame.K_SPACE:
                weapon_x = character_x + \
                    (character_width / 2) - (weapon_width / 2)
                # 무기는 캐릭터의 x 좌표 중앙에서 발사 해야하므로 위치정의
                weapon_y = character_y  # 캐릭터의 y축으로 무기 y축 정의
                weapons.append([weapon_x, weapon_y])  # 리스트에 무기의 x,y를 추가

        if e.type == pygame.KEYUP:
            if e.key == pygame.K_LEFT or e.key == pygame.K_RIGHT:
                char_move_x = 0

# 3. 게임 캐릭터 위치 정의
    character_x += char_move_x

    if character_x < 0:
        character_x = 0
    elif character_x > screen_width - character_width:
        character_x = screen_width - character_width

# 무기 위치 조정
# ex) x = 100, y= 200 => x는 그대로, y는 점점 줄어듬
# 즉 x는 그대로 이고 y 좌표만 스피드만큼 뺴주는 것
    weapons = [[w[0], w[1] - weapon_speed] for w in weapons]  # 무기 위치를 위로

    weapons = [[w[0], w[1]] for w in weapons if w[1] > 0]
    # y가 천장에 닿지 않은 것만 리스트로

    # 공 위치 정의----
    for ball_idx, ball_val in enumerate(balls):  # enu = index가 필요할 떄
        ball_pos_x = ball_val["x"]
        ball_pos_y = ball_val["y"]
        ball_img_idx = ball_val["img_idx"]

        ball_size = ball_images[ball_img_idx].get_rect().size
        ball_width = ball_size[0]
        ball_height = ball_size[1]

    # 공의 경계값 처리
        # 가로 벽에 맞았다면 반대 방향으로 공 튀기
        if ball_pos_x < 0 or ball_pos_x > screen_width - ball_width:
            # -3이었다면 3 , 3 이었다면 - 3 -*- = + +*+ = *
            ball_val["to_x"] = ball_val["to_x"] * -1
            # 세로 위치 처리
            # 스테이지에 닿으면 튕겨서 올라가는 처리
        if ball_pos_y >= screen_height - stage_height - ball_height:  # stage에 닿았다면
            # 최초 튕기는 값 (딕셔너리에 정의한 것)
            ball_val["to_y"] = ball_val["init_speed_y"]
        else:  # 그 외에는 속도를 증가(시작값은 마이너스이므로 올라가다 정수로 넘어오면 내려옴)
            ball_val["to_y"] += 0.5  # 처음에 -6이라면 0.5씩 더함 0, 0.5 .. 빠르게 내려오는 효과

        ball_val["x"] += ball_val["to_x"]
        ball_val["y"] += ball_val["to_y"]

        # 4. 충돌 처리

        # 5. 화면에 그리기

    screen.blit(background, (0, 0))

    # weapon 리스트안에있는 모든 것을 그려야 하기떄문 for문 사용
    # 순서대로 그리기 때문에 stage 위에 재 정의
    for x, y in weapons:
        screen.blit(weapon, (x, y))

    for idx, val in enumerate(balls):
        print_ball_x = val["x"]
        print_ball_y = val["y"]
        print_ball_idx = val["img_idx"]
        screen.blit(ball_images[print_ball_idx], (print_ball_x, print_ball_y))

    screen.blit(stage, (0, (screen_height - stage_height)))
    screen.blit(character, (character_x, character_y))

    pygame.display.update()

pygame.quit()
