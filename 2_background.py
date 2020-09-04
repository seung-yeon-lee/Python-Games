import pygame

# 뼈대 만들기
pygame.init()  # 초기화

# 화면 크기 설정
screen_width = 480  # 가로
screen_height = 640  # 세로
screen = pygame.display.set_mode(
    (screen_width, screen_height))  # 튜플 형식으로 가로,세로 주입

# ------- 화면 제목 설정-------------
pygame.display.set_caption("Create Pygame Version 1(Prototype)")  # 게임 이름 설정
# 이벤트 루프가 실행되야지만 게임이 꺼지지 않음

# -----------Background 불러오기( 그림판 작업 후)------------------------
background = pygame.image.load("C:/Users/이승연/Desktop/PyGames/backgound.png")


# ---------이벤트 루프-------------
running = True  # 게임이 진행중인지 판단 여부
while running:
    for e in pygame.event.get():  # 어떠한 동작이 있는지 체크 반드시 필요한 부분(이벤트가 발생 시)
        if e.type == pygame.QUIT:  # 게임창에서  창이 닫히는 이벤트가 발생 한다면
            running = False  # 닫았다면 false
    # screen.fill((0, 0, 255)) # fill 메서드로 rgb 표현식으로도 가능
    screen.blit(background, (0, 0))  # 이벤트루프 밖에서 배경 지정 튜플형식으로(x,y)축
    pygame.display.update()  # 게임화면 다시 그리기(매번 매 프레임시 화면을 그려줘야 함)

# 게임 종료
pygame.quit()
