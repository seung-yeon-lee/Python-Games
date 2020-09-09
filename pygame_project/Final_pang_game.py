import pygame
import os

# 게임 초기화
pygame.init()

# 화면 설정------------------------------------------------------------------------
screen_width = 640  # 가로크기 설정
screen_height = 480  # 세로크기 설정
screen = pygame.display.set_mode((screen_width, screen_height))

# 화면 타이틀 설정
pygame.display.set_caption('Minigames in pygame')

# FPS 설정
clock = pygame.time.Clock()

########################################################################
# 1.사용자 게임 초기화 ( 배경화면, 이미지, 좌표, 속도, 폰트 ) 설정 부분
current_path = os.path.dirname(__file__)  # os모듈을 이용해 현재 파일 위치 반환
image_path = os.path.join(current_path, 'images')  # image 폴더 위치 반환

# 배경화면 설정--------------------------------------------------------------------------------
background = pygame.image.load(os.path.join(image_path, 'background.png'))

# 스테이지 설정---------------------------------------------------------------------------------
stage = pygame.image.load(os.path.join(image_path, 'stage.png'))
stage_size = stage.get_rect().size
stage_height = stage_size[1]  # 스테이지는 높이만 필요(스테이지 위에 캐릭터)


# 게임 캐릭터 설정-------------------------------------------------------------------------------
character = pygame.image.load(os.path.join(image_path, 'character.png'))
character_size = character.get_rect().size
character_width = character_size[0]
character_height = character_size[1]
character_x = (screen_width / 2) - (character_width / 2)  # 캐릭터는 화면 중앙에 위치
# y축은 스테이지 위에
character_y = (screen_height) - (stage_height + character_height)


# 캐릭터 이동
character_move_x = 0

# 캐릭터 스피드
character_speed = 0.3

# 무기(총) 설정---------------------------------------------------------------------------------------
weapon = pygame.image.load(os.path.join(image_path, 'weapon.png'))
weapon_size = weapon.get_rect().size
weapon_width = weapon_size[0]  # 높이는 캐릭터 y축으로 설정하기 때문에 너비만 필요

# 무기 발사 속도 설정
weapon_speed = 10

# 무기는 클릭마다 발사가 되므로 그 값을 리스트로 관리
weapons = []

# 게임 성공,실패 처리를 위한 Font 및 Time 정의--------------------------------------------------
game_font = pygame.font.Font(None, 40)
total_time = 100  # 게임 시간 제한 100초
start_time = pygame.time.get_ticks()   # 게임 시작 시간
game_result = 'Game Over!'  # 게임 종료 메시지

# 게임 볼 설정--------------------------------------------------------------------------------------
# 게임 볼 사이는 160 / 80 / 40 / 20 으로 설정
# 최초 큰 공을 맞췄다면 그 다음 사이즈의 공이 2개가 나타나야 하므로 리스트로 관리
ball_images = [
    pygame.image.load(os.path.join(image_path, 'ball1.png')),
    pygame.image.load(os.path.join(image_path, 'ball2.png')),
    pygame.image.load(os.path.join(image_path, 'ball3.png')),
    pygame.image.load(os.path.join(image_path, 'ball4.png')),
]

# 공 크기에 따른 최초 스피드 처리
ball_speed_y = [-18, -15, -12, -9]

# 공이 쪼개지는것을 리스트로 관리
balls = []

# 게임 시작 시 최초로 등장하는 큰 공 추가
balls.append({
    "x": 50,  # x축에서 50으로 초깃값 지정
    "y": 50,  # y축에서 50으로 초깃값 지정
    "img_idx": 0,  # 공 이미지의 index
    "to_x": 3,  # 공의 x 축 이동 방향
    "to_y": -10,  # 공의 y축 이동 방향
    "init_speed_y": ball_speed_y[0]  # 정의한 변수의 0번쨰 idx로 우선 지정
})

# --공을 무기로 맞췄을 시, 사라져야하는 무기, 공 정보를 저장하기 위한 변수 정의--------------------
weapon_remove = -1
ball_remove = -1

# ---------------------------------------------------------------------------------------------------------
# 2, 이벤트 처리 ( 키보드, 마우스 등)
running = True
while running:
    dt = clock.tick(30)

    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            running = False
        if e.type == pygame.KEYDOWN:
            if e.key == pygame.K_LEFT:
                character_move_x -= character_speed
            elif e.key == pygame.K_RIGHT:
                character_move_x += character_speed
            elif e.key == pygame.K_SPACE:
                # 무기는 캐릭터의 x 중앙에서 발사하므로 무기 변수 선언 및 정의
                weapon_x = character_x + \
                    (character_width / 2) - (weapon_width / 2)
                weapon_y = character_y  # 캐릭터의 y축에 무기 설정
                weapons.append([weapon_x, weapon_y])  # 선언해둔 리스트에 무기 x,y 값 저장

        # 키보드 방향키를 누르고 있지 않다면 x 좌표를 0으로 설정
        if e.type == pygame.KEYUP:
            if e.key == pygame.K_LEFT or e.key == pygame.K_RIGHT:
                character_move_x = 0

# 3. 게임 캐릭터 위치 정의 ------------------------------------------------------------------------------------
    character_x += character_move_x * dt
    if character_x < 0:  # 게임화면에서 왼쪽으로 넘어갔다면
        character_x = 0
    elif character_x > screen_width - character_width:  # 게임화면에서 오른쪽으로 넘어갔다면
        character_x = screen_width - character_width

# 무기 위치 조정---------------------------------------------------------------------------------------------------
# 리스트 표현식
# 현재 무기의 x 축은 캐릭터와 같고 y축만 처리해주면 됨(x는 그대로 y만 스피드만큼 뺴주는 것)
# 키 이벤트에서 스페이스바 누를 시 weapons에 append를 하게 구현 해 놓았음
    weapons = [[w[0], w[1] - weapon_speed] for w in weapons]
    weapons = [[w[0], w[1]] for w in weapons if w[1] > 0]
# y축이 천장에 닿지 않은 것만 리스트로 추가

# 공 위치 정의 ------------------------------------------------------------------------------------------------------
    # index 값이 필요하기 때문에 enumerate 사용
    for ball_idx, ball_val in enumerate(balls):
        ball_pos_x = ball_val['x']  # 딕셔너리 balls의 x의 값을 대입
        ball_pos_y = ball_val['y']
        ball_img_idx = ball_val['img_idx']
        ball_size = ball_images[ball_img_idx].get_rect().size
        ball_width = ball_size[0]
        ball_height = ball_size[1]

    # 공이 벽에 맞았다면 그 반대 방향으로 공 튕기게 처리
        if ball_pos_x < 0 or ball_pos_x > screen_width - ball_width:
            ball_val['to_x'] = ball_val['to_x'] * - 1
  # -3이라면 3, & 3이라면 -3 반대 방향으로 움직임

    # 공이 스테이지에 닿았다면
        if ball_pos_y >= screen_height - stage_height - ball_height:
            # 최초 정의한 값으로 닿으면 튕겨서 공이 올라가게됨
            ball_val['to_y'] = ball_val['init_speed_y']

        else:  # 그 외에는 시작값은 마이너스 이므로 올라가다가 정수로 바뀌면서 공이 내려오는 효과
            ball_val['to_y'] += 0.5

        ball_val['x'] += ball_val['to_x']
        ball_val['y'] += ball_val['to_y']

    # 4. 충돌 처리 정의-------------------------------------------------------------------------------------------
    # 캐릭터와 공이 닿았을 경우, 무기와 공이 닿았을 경우

    # 4.1 캐릭터와 공이 부딪혔다면  @@@@@@@@@@@@@@@@@@@@@@@@@@
    # 캐릭터 rect 정보 업데이트
        character_rect = character.get_rect()
        character_rect.left = character_x
        character_rect.top = character_y

        for ball_idx, ball_val in enumerate(balls):  # 공 정보를 위한 for문
            ball_pos_x = ball_val['x']
            ball_pos_y = ball_val['y']
            ball_img_idx = ball_val['img_idx']

        # 공 rect 정보 업데이트
            ball_rect = ball_images[ball_img_idx].get_rect()
            ball_rect.left = ball_pos_x
            ball_rect.top = ball_pos_y

        # 공 & 캐릭터가 충돌했다면
            if character_rect.colliderect(ball_rect):
                running = False
                break  # 충돌했다면 게임을 멈춤, (for문 탈출)

        # 4.2 무기와 공이 부딪혔다면 @@@ @@@@@@@@@@@@@@@@@@@@@
            # 무기 정보를 얻기 위한 for
            for weapon_idx, weapon_val in enumerate(weapons):
                weapon_pos_x = weapon_val[0]
                weapon_pos_y = weapon_val[1]
            # 무기 정보 업데이트 정의
                weapon_rect = weapon.get_rect()
                weapon_rect.left = weapon_pos_x
                weapon_rect.top = weapon_pos_y

            # 무기와 공의 충돌 체크
            # 2중 포문으로 바깥쪽 for에서 ball_rect 참조
                if weapon_rect.colliderect(ball_rect):
                    # 초깃값은 -1이지만 현재 무기,공의 index를 정의 (삭제를 위한 값)
                    weapon_remove = weapon_idx
                    ball_remove = ball_idx

                # 충돌을 했는데 가장 작은 볼이 아니라면 다음 단계의 크기로 나눠주는 처리
                    if ball_img_idx < 3:  # 바깥 for문 참조, 최초 공은 image의 0번째 이므로 if문에 걸림
                        # 현재 공의 크기를 가져옴
                        ball_width = ball_rect.size[0]
                        ball_height = ball_rect.size[1]
                    # 나눠진 공 정보 정의
                    # images에서 현재 idx를 +1 한 값(그다음 공)의 정보 업데이트
                        small_ball_rect = ball_images[ball_img_idx + 1].get_rect()
                    # 그 다음 공에 대한 가로,세로 정의
                        small_ball_width = small_ball_rect.size[0]
                        small_ball_height = small_ball_rect.size[1]

                    # 충돌 후 왼쪽으로 분해 되는 공@@@@@@@@@@@@@@

                    # 볼의 x축 + (현재 볼 너비 / 2) - (그 다음공 너비 /2)
                        balls.append({
                            "x": ball_pos_x + (ball_width / 2) - (small_ball_width / 2),
                            "y": ball_pos_y + (ball_height / 2) - (small_ball_height / 2),
                            # 현재 images idx에서 +1 (그 다음 거로)
                            "img_idx": ball_img_idx + 1,
                            "to_x": -3,  # 왼쪽으로 쪼개지므로 - 값 설정
                            "to_y": -6,
                            # 속도 역시 +1씩(그 다음 속도로)
                            "init_speed_y": ball_speed_y[ball_img_idx + 1]
                        })

                    # 충돌 후 오른쪽으로 분해 되는 공@@@@@@@@@@@@@
                        balls.append({
                            "x": ball_pos_x + (ball_width / 2) - (small_ball_width / 2),
                            "y": ball_pos_y + (ball_height / 2) - (small_ball_height / 2),
                            # 현재 images idx에서 +1 (그 다음 거로)
                            "img_idx": ball_img_idx + 1,
                            "to_x": 3,  # 오른쪽으로 쪼개지므로 정수로 설정
                            "to_y": -6,
                            # 속도 역시 +1씩(그 다음 속도로)
                            "init_speed_y": ball_speed_y[ball_img_idx + 1]
                        })
                    break  # 충돌해서 처리가 완료 되었다면 for문 탈출

            # 충돌된 공 & 무기 삭제 정의( 공과 충돌했다면 기존 공과 무기를 삭제하기 위함)
            # 위에서 무기와 공이 충돌할 경우에 대비해서 변수에 현재 무기 공에대한 Idx를 정의했었음
            if ball_remove > -1:  # 인덱스는 0,1,2 순서대로 가기 떄문에 True 일 시(값이 있다면)
                del balls[ball_remove]  # 딕셔너리 balls에서 현재 값 삭제
                ball_remove = -1  # 다음 프레임에서 똑같이 -1로 시작하고 업데이트 될 때 처리 위해
            if weapon_remove > -1:
                del weapons[weapon_remove]
                weapon_remove = -1

            # 모든 공을 처리 했다면 게임 종료 처리 -----------------------------------------------------------
            if len(balls) == 0:
                game_result = 'Mission Complete!'
                running = False

# --------------- 화면에 모든 요소 추가 및 그리기 -----------------------------------------------------------------

    screen.blit(background, (0, 0))  # 배경 화면 설정
# weapon 리스트안에있는 모든 것을 그려야 하므로 for문 사용
# 순서대로 그리기 떄문에 stage보다 위에 설정
    for x, y in weapons:
        screen.blit(weapon, (x, y))

    for idx, val in enumerate(balls):  # 최초 공,분해 시 작업을 미리 끝내두었기 떄문에 원하는 정보가 다 들어있음
        print_ball_x = val['x']
        print_ball_y = val['y']
        print_ball_idx = val['img_idx']
        screen.blit(ball_images[print_ball_idx], (print_ball_x, print_ball_y))

    screen.blit(stage, (0, (screen_height - stage_height)))  # 스테이지 설정
    screen.blit(character, (character_x, character_y))  # 캐릭터 설정

# 게임 시간 계산
    elapsed_time = (pygame.time.get_ticks() - start_time) / 1000  # ms 를 => s 로
    timer = game_font.render(
        f"Time:{int(total_time - elapsed_time)}", True, (255, 255, 255))
    screen.blit(timer, (10, 10))

# 시간 초과
    if total_time - elapsed_time <= 0:
        game_result = 'Game Over'
        running = False

    pygame.display.update()  # 무조건 필요 화면설정 할떄도 계속 그려줘야 함

# 게임 오버 메시지
msg = game_font.render(game_result, True, (255, 255, 0))
msg_rect = msg.get_rect(
    center=(int(screen_width / 2), int(screen_height / 2)))
screen.blit(msg, msg_rect)
pygame.display.update()
pygame.time.delay(2000)  # 바로 종료 방지용 2초 대기

pygame.quit()
