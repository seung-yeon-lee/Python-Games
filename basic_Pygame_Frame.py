import pygame
##############################
# 기본 초기화
pygame.init()

# 화면 크기 설정


# 화면 타이틀 설정


# FPS


# 1. 사용자 게임 초기화 ( 배경화면, 이미지, 좌표,속도, 폰트)

# 배경화면

# 캐릭터 등 이미지

# 좌표

# 속도

# 폰트

running = True
while running:

    # 2. 이벤트 처리 ( 키보드, 마우스 등)
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            running = False

# 3. 게임 캐릭터 위치 정의

# 4. 충돌 처리

# 5. 화면에 그리기

    pygame.display.update()

pygame.quit()
