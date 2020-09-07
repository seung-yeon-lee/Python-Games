# 미니게임1

import pygame
import random


# 뼈대 만들기
pygame.init()  # 초기화

# 화면 크기 설정
screen_width = 550  # 가로
screen_height = 640  # 세로
screen = pygame.display.set_mode(
    (screen_width, screen_height))  # 튜플 형식으로 가로,세로 주입

pygame.display.set_caption("똥 피하기 게임")  # 게임 이름 설정

clock = pygame.time.Clock()

background = pygame.image.load("C:/Users/이승연/Desktop/pgame/backgound.png")

# ----------- 캐릭터 불러오기 --------------
character = pygame.image.load("C:/Users/이승연/Desktop/pgame/char.png")
character_size = character.get_rect().size  # 이미지 크기를 구해옴
character_width = character_size[0]  # 캐릭터의 가로 크기
character_height = character_size[1]  # 캐릭터의 세로 크기
character_x = (screen_width / 2) - \
    (character_width / 2)  # 화면 가로의 절반 크기에 해당하는 곳에 위치
character_y = screen_height - character_height  # 화면 세로 크기 가장 밑에 위치
# --------- 이동 할 좌표 -------------------
move_x = 0
# -------- 이동 속도 ---------------
char_speed = 0.6
# --------------- 적 캐릭터 생성 ----------------------
enemy = pygame.image.load("C:/Users/이승연/Desktop/pgame/enemy.png")
enemy_size = enemy.get_rect().size  # 이미지 크기를 구해옴
enemy_width = enemy_size[0]  # 캐릭터의 가로 크기
enemy_height = enemy_size[1]  # 캐릭터의 세로 크기
enemy_x = random.randint(0, screen_width - enemy_width)
enemy_y = 0
enemy_speed = 7

# ---------이벤트 루프-------------
running = True  # 게임이 진행중인지 판단 여부
while running:
    # FPS 추가부분
    dt = clock.tick(60)  # 게임화면의 초당 프레임 수를 설정 ( tick 메서드 사용)
    for e in pygame.event.get():  # 어떠한 동작이 있는지 체크 반드시 필요한 부분(이벤트가 발생 시)
        if e.type == pygame.QUIT:  # 게임창에서  창이 닫히는 이벤트가 발생 한다면
            running = False  # 닫았다면 false
            # 키보드 이벤트 부분
        if e.type == pygame.KEYDOWN:  # 키보드를 눌렀다면
            if e.key == pygame.K_LEFT:  # 캐릭터를 왼쪽으로
                move_x -= char_speed
            elif e.key == pygame.K_RIGHT:  # 캐릭터를 오른쪽으로
                move_x += char_speed

        if e.type == pygame.KEYUP:  # 방향키에서 손을 떼었다면 멈춤 좌표표시
            if e.key == pygame.K_LEFT or e.key == pygame.K_RIGHT:
                move_x = 0

    character_x += move_x * dt

    # 가로 경계값 처리
    if character_x < 0:  # 왼쪽 화면 밖으로 나갔다면
        character_x = 0  # 맨 왼쪽에 멈춤
    elif character_x > screen_width - character_width:
        character_x = screen_width-character_width

    # 똥 처리
    enemy_y += enemy_speed
    if enemy_y > screen_height:
        enemy_y = 0
        enemy_x = random.randint(0, screen_width - enemy_width)
    # -- 충돌 처리를 위한 rect 정보 업데이틑 부분-- ##
    char_rect = character.get_rect()  # 실제 캐릭터가 위치하고있는 곳으로 업데이트
    char_rect.left = character_x
    char_rect.top = character_y

    enemy_rect = enemy.get_rect()
    enemy_rect.left = enemy_x
    enemy_rect.top = enemy_y
    # 충돌 체크----------------
    # 사각형 기준으로 충돌이있는지 판단 # 즉, 캐릭터와 적과 충돌을 했는가?
    if char_rect.colliderect(enemy_rect):
        print('충돌')
        running = False

    # screen.fill((0, 0, 255)) # fill 메서드로 rgb 표현식으로도 가능
    screen.blit(background, (0, 0))  # 이벤트루프 밖에서 배경 지정 튜플형식으로(x,y)축
    screen.blit(character, (character_x, character_y))  # 캐릭터 그리기
    screen.blit(enemy, (enemy_x, enemy_y))  # 적 그리기

    pygame.display.update()  # 게임화면 다시 그리기(매번 매 프레임시 화면을 그려줘야 함)

# 바로 게임이 꺼지는데 2초 딜레이 후 종료되게 하기
pygame.time.delay(2000)

# 게임 종료
pygame.quit()

# 1시간 25분#
