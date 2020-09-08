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
background = pygame.image.load("C:/Users/이승연/Desktop/PyGames/backgound.png")

# ----------- 캐릭터 불러오기 --------------
character = pygame.image.load("C:/Users/이승연/Desktop/PyGames/char.png")
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

# ---------이벤트 루프-------------
running = True  # 게임이 진행중인지 판단 여부
while running:
    # FPS 추가부분
    dt = clock.tick(30)  # 게임화면의 초당 프레임 수를 설정 ( tick 메서드 사용)
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

    # screen.fill((0, 0, 255)) # fill 메서드로 rgb 표현식으로도 가능
    screen.blit(background, (0, 0))  # 이벤트루프 밖에서 배경 지정 튜플형식으로(x,y)축

    screen.blit(character, (character_x, character_y))  # 캐릭터 그리기

    pygame.display.update()  # 게임화면 다시 그리기(매번 매 프레임시 화면을 그려줘야 함)

# 게임 종료
pygame.quit()
