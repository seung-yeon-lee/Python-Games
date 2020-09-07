# 7 텍스트 처리

import pygame


# 뼈대 만들기
pygame.init()  # 초기화

# 화면 크기 설정
screen_width = 550  # 가로
screen_height = 640  # 세로
screen = pygame.display.set_mode(
    (screen_width, screen_height))  # 튜플 형식으로 가로,세로 주입

# ------- 화면 제목 설정-------------
pygame.display.set_caption("Create Pygame Version 1(Prototype)")  # 게임 이름 설정

# FPS 처리
clock = pygame.time.Clock()

# -----------Background 불러오기( 그림판 작업 후)------------------------
background = pygame.image.load("C:/Users/이승연/Desktop/pgame/backgound.png")

# ----------- 캐릭터 불러오기 --------------
character = pygame.image.load("C:/Users/이승연/Desktop/pgame/char.png")
# 배경은 그대로 이지만 캐릭터는 움직임이 있음
character_size = character.get_rect().size  # 이미지 크기를 구해옴
# print(character_size)
character_width = character_size[0]  # 캐릭터의 가로 크기
character_height = character_size[1]  # 캐릭터의 세로 크기
character_x = (screen_width / 2) - \
    (character_width / 2)  # 화면 가로의 절반 크기에 해당하는 곳에 위치
character_y = screen_height - character_height  # 화면 세로 크기 가장 밑에 위치

# --------- 이동 할 좌표 -------------------
move_x = 0
move_y = 0

# -------- 이동 속도 ---------------
char_speed = 0.6

# --------------- 적 캐릭터 생성 ----------------------
enemy = pygame.image.load("C:/Users/이승연/Desktop/pgame/enemy.png")
# 배경은 그대로 이지만 캐릭터는 움직임이 있음
enemy_size = enemy.get_rect().size  # 이미지 크기를 구해옴
# print(character_size)
enemy_width = enemy_size[0]  # 캐릭터의 가로 크기
enemy_height = enemy_size[1]  # 캐릭터의 세로 크기
enemy_x = (screen_width / 2) - \
    (enemy_width / 2)  # 화면 가로의 절반 크기에 해당하는 곳에 위치
enemy_y = (screen_height / 2) - (enemy_height / 2)  # 화면 세로 크기 가장 밑에 위치

# 폰트 정의
game_font = pygame.font.Font(None, 40)  # 폰트 객체 생성(폰트,크기)

# 게임 총 시간
total_time = 10

# 시작한 시점 계산
start_tick = pygame.time.get_ticks()  # 시작 tick을 받아옴

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
            elif e.key == pygame.K_UP:  # 캐릭터를 위로
                move_y -= char_speed
            elif e.key == pygame.K_DOWN:  # 캐릭터를 아래로
                move_y += char_speed
        if e.type == pygame.KEYUP:  # 방향키에서 손을 떼었다면 멈춤 좌표표시
            if e.key == pygame.K_LEFT or e.key == pygame.K_RIGHT:
                move_x = 0
            elif e.key == pygame.K_UP or e.key == pygame.K_DOWN:
                move_y = 0
    # if문 탈출 후
    # 프레임이 높으면 부드러울 수 있으나 게임 속도는 낮나 높나 같아야함
    # 그렇기 떄문에 추가한 dt값을 곱함
    character_x += move_x * dt
    character_y += move_y * dt
    # 현재 캐릭터가 게임화면 밖으로 나가지는 현상이 발생, 해결하는 처리과정
    # 현재 width = 550 , height = 640

    # 가로 경계값 처리
    if character_x < 0:  # 왼쪽 화면 밖으로 나갔다면
        character_x = 0  # 맨 왼쪽에 멈춤
    elif character_x > screen_width - character_width:
        character_x = screen_width-character_width
    # 세로 경계값 처리
    if character_y < 0:
        character_y = 0
    elif character_y > screen_height - character_height:
        character_y = screen_height - character_height

    # -- 충돌 처리를 위한 rect 정보 업데이틑 부분-- ##
    char_rect = character.get_rect()  # 실제 캐릭터가 위치하고있는 곳으로 업데이트
    char_rect.left = character_x
    char_rect.top = character_y

    enemy_rect = enemy.get_rect()
    # print(enemy_rect) # 0 0 70 70 사이즈 정보
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

    # 타이머 넣기
    # 경과 시간 체크
    result_time = (pygame.time.get_ticks() - start_tick) / 1000
    # 결과시간을 초 단위로 표시하기 위해 / 1000
    title = game_font.render('TEST GAMES', True, (255, 255, 255))
    timer = game_font.render(
        str(int(total_time - result_time)), True, (255, 255, 255))
    # 출력할 글자, True, 글자 색상
    screen.blit(timer, (12, 10))
    screen.blit(title, (200, 2))

    # 만약 시간이 0 이하이면 게임 종료
    if total_time - result_time <= 0:
        running = False
    pygame.display.update()  # 게임화면 다시 그리기(매번 매 프레임시 화면을 그려줘야 함)

# 바로 게임이 꺼지는데 2초 딜레이 후 종료되게 하기
pygame.time.delay(2000)

# 게임 종료
pygame.quit()
