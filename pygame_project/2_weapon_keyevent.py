

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


running = True
while running:

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
    # 천장에 닿으면 사라지게 하기
    weapons = [[w[0], w[1]]
               for w in weapons if w[1] > 0]  # y가 천장에 닿지 않은 것만 리스트로


# 4. 충돌 처리

# 5. 화면에 그리기
    screen.blit(background, (0, 0))

    # weapon 리스트안에있는 모든 것을 그려야 하기떄문 for문 사용
    # 순서대로 그리기 때문에 stage 위에 재 정의
    for x, y in weapons:
        screen.blit(weapon, (x, y))

    screen.blit(stage, (0, (screen_height - stage_height)))
    screen.blit(character, (character_x, character_y))

    pygame.display.update()

pygame.quit()


# 무기설정, 키이벤트 space 무기 설정, 무기 x,y축 리스트를 이용하여 저장 후
# 화면 그려주기 작업
