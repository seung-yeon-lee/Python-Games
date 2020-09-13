import random
from time import sleep
from pygame.sprite import Sprite
import os

import pygame
from pygame.locals import *

WINDOW_WIDTH = 480  # 가로화면
WINDOW_HEIGHT = 640  # 세로화면

# 이미지 파일
current_path = os.path.dirname(__file__)
img_path = os.path.join(current_path, 'game_source')


# 기본 색상 정의
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (250, 250, 50)
RED = (250, 50, 50)

# FPS 설정
FPS = 60

# 전투기 생성


class Fighter(Sprite):
    def __init__(self):
        super(Fighter, self).__init__()   # 상속받았기 떄문에 super 로 상위 클래스 호출
        self.image = pygame.image.load(os.path.join(img_path, 'fighter.png'))
        self.rect = self.image.get_rect()   # get_rect()로 크기를 가져옴
        self.rect.x = int(WINDOW_WIDTH / 2)
        self.rect.y = WINDOW_HEIGHT - self.rect.height  # 우주선의 높이만큼 뺴서 맨 밑에 위치 방지
        self.dx = 0  # x,y 움직임 정의할 값 선언
        self.dy = 0

    def update(self):   # 전투기가 움직일 떄 처리
        self.rect.x += self.dx
        self.rect.y += self.dy
        # 화면 왼쪽 or 오른쪽으로 벗어난다면
        if self.rect.x < 0 or self.rect.x + self.rect.width > WINDOW_WIDTH:
            self.rect.x -= self.dx

        if self.rect.y < 0 or self.rect.y + self.rect.height > WINDOW_HEIGHT:
            self.rect.y -= self.dy
        #  화면에 그리는 메서드

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def collide(self, sprites):  # 충돌 시
        for sprite in sprites:
            if pygame.sprite.collide_rect(self, sprite):  # 만약 충돌이 났다면
                return sprite  # 충돌이 발생한 것을 반환

# 미사일 class 생성


class Missile(Sprite):
    def __init__(self, xpos, ypos, speed):  # 미사일은 위치값과 속도를 가져와야 하므로
        super(Missile, self).__init__()
        self.image = pygame.image.load(os.path.join(img_path, 'missile.png'))
        self.rect = self.image.get_rect()
        self.rect.x = xpos  # 미사일은 전투기에서 발사되야 하므로 좌표를 가져옴
        self.rect.y = ypos
        self.speed = speed
        self.sound = pygame.mixer.Sound(os.path.join(img_path, 'missile.wav'))

    def launch(self):   # 미사일 발사 시 소리 재생
        self.sound.play()

    def update(self):
        self.rect.y -= self.speed
        if self.rect.y + self.rect.height < 0:  # 미사일이 화면 밖으로 나갔다면
            self.kill()  # 해당 미사일은 삭제

    def collide(self, sprites):  # 충돌 여부
        for sprite in sprites:
            if pygame.sprite.collide_rect(self, sprite):
                return sprite

#  장애물(운석) class 생성


class Rock(Sprite):
    def __init__(self, xpos, ypos, speed):  # 장애물 역시, 좌표 및 속도를 필요로 함
        super(Rock, self).__init__()
        rock_images = ('rock01.png', 'rock02.png', 'rock03.png', 'rock04.png', 'rock05.png', \
                       'rock06.png', 'rock07.png', 'rock08.png', 'rock09.png', 'rock10.png', \
                       'rock11.png', 'rock12.png', 'rock13.png', 'rock14.png', 'rock15.png', \
                       'rock16.png', 'rock17.png', 'rock18.png', 'rock19.png', 'rock20.png', \
                       'rock21.png', 'rock22.png', 'rock23.png', 'rock24.png', 'rock25.png', \
                       'rock26.png', 'rock27.png', 'rock28.png', 'rock29.png', 'rock30.png')
        #  위에 정의한 30개의 운석중에 랜덤으로 1개만
        self.image = pygame.image.load(os.path.join(img_path, random.choice(rock_images)))
        self.rect = self.image.get_rect()
        self.rect.x = xpos
        self.rect.y = ypos
        self.speed = speed

    def update(self):
        self.rect.y += self.speed  # 운석은 아래로 떨어지므로

    def out_of_screen(self):
        if self.rect.y > WINDOW_HEIGHT:  # y축이 게임화면보다 크다면
            return True

#  기본 함수 정의 점수,폰트, 등 설정하기 위한 함수


def draw_text(text, font, surface, x, y, main_color):
    text_obj = font.render(text, True, main_color)
    text_rect = text_obj.get_rect()
    text_rect.centerx = x
    text_rect.centery = y
    surface.blit(text_obj, text_rect)


def occur_explosion(surface, x, y):
    explosion_image = pygame.image.load(os.path.join(img_path, 'explosion.png'))
    explosion_rect = explosion_image.get_rect()
    explosion_rect.x = x
    explosion_rect.y = y
    surface.blit(explosion_image, explosion_rect)

    explosion_sounds = ('explosion01.wav', 'explosion02.wav', 'explosion03.wav')  # 폭발소리 랜덤
    explosion_sound = pygame.mixer.Sound(os.path.join(img_path, random.choice(explosion_sounds)))
    explosion_sound.play()


def game_loop():
    default_font = pygame.font.Font(os.path.join(img_path, 'NanumGothic.ttf'), 28)
    background = pygame.image.load(os.path.join(img_path, 'background.png'))
    gameover_sound = pygame.mixer.Sound(os.path.join(img_path, 'gameover.wav'))
    pygame.mixer.music.load(os.path.join(img_path, 'music.wav'))
    pygame.mixer.music.play(-1)  # 몇번 재생할건지 -1은 무한 반복(메인 사운드)
    fps_clock = pygame.time.Clock()

    fighter = Fighter()  # 인스턴스 생성
    missiles = pygame.sprite.Group()  # 미사일은 여러개가 들어갈 수있어야 하므로 Group
    rocks = pygame.sprite.Group()  # 운석 또한 Group

    occur_prob = 40  # 확률적으로 얼만큼 나타나게 할 지
    shot_count = 0  # 격추 성공한 횟수
    missed_count = 0  # 놓친 횟수

    done = False
    while not done:
        for e in pygame.event.get():
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_LEFT:
                    fighter.dx -= 7
                elif e.key == pygame.K_RIGHT:
                    fighter.dx += 7
                elif e.key == pygame.K_UP:
                    fighter.dy -= 7
                elif e.key == pygame.K_DOWN:
                    fighter.dy += 7
                elif e.key == pygame.K_SPACE:
                    missile = Missile(fighter.rect.centerx, fighter.rect.y, 10)  # 미사일 생성
                    missile.launch()
                    missiles.add(missile)  # 그룹화한 인스턴스에 현재 미사일 저장
            if e.type == pygame.KEYUP:
                if e.key == pygame.K_LEFT or e.key == pygame.K_RIGHT:
                    fighter.dx = 0
                if e.key == pygame.K_UP or e.key == pygame.K_DOWN:
                    fighter.dy = 0

        # 화면 그리기
        screen.blit(background, background.get_rect())

        # 운석 그리기
        # 점수에 따라서 많이 맞췄을 경우, 점점 운석이 많이 등장하게 구현
        occur_of_rocks = 1 + int(shot_count / 300)
        min_rock_speed = 1 + int(shot_count / 200)  # 100개를 맞췄다면 스피드는 1.5
        max_rock_speed = 1 + int(shot_count / 100)  # 100개를 맞췄다면 스피드가 2로 올라감

        if random.randint(1, occur_prob) == 1:  # 1부터 40 사이에 1이 등장할 확률
            for i in range(occur_of_rocks):  # 운석을 얼만큼 등장하게 할 것인지
                speed = random.randint(min_rock_speed, max_rock_speed)  # 스피드를 하나 선택
                rock = Rock(random.randint(0, WINDOW_WIDTH - 30), 0, 5)
                rocks.add(rock)

        draw_text('파괴한 운석: {}'.format(shot_count), default_font, screen, 100, 20, YELLOW)
        draw_text('놓친 운석: {}'.format(missed_count), default_font, screen, 400, 20, RED)

        # 충돌 여부 판단
        for missile in missiles:
            rock = missile.collide(rocks)  # 미사일과 운석 모두 충돌했는지 비교
            if rock:
                missile.kill()
                rock.kill()
                occur_explosion(screen, rock.rect.x, rock.rect.y)
                shot_count += 1

        for rock in rocks:  # 모든 운석 for
            if rock.out_of_screen():  # 운석이 화면 밖으로 나갔다면
                rock.kill()
                missed_count += 1

        rocks.update()
        rocks.draw(screen)
        missiles.update()
        missiles.draw(screen)
        fighter.update()
        fighter.draw(screen)
        pygame.display.flip() # 전체 반영

        if fighter.collide(rocks) or missed_count >= 3:
            pygame.mixer_music.stop()
            occur_explosion(screen, fighter.rect.x, fighter.rect.y)
            pygame.display.update()
            gameover_sound.play()
            sleep(1)
            done = True

        fps_clock.tick(FPS)

    return 'game_menu'


def game_menu():
    start_image = pygame.image.load(os.path.join(img_path, 'background.png'))
    screen.blit(start_image, [0, 0])
    draw_x = int(WINDOW_WIDTH / 2)
    draw_y = int(WINDOW_HEIGHT / 4)
    font_70 = pygame.font.Font(os.path.join(img_path, 'NanumGothic.ttf'), 70)
    font_40 = pygame.font.Font(os.path.join(img_path, 'NanumGothic.ttf'), 40)

    draw_text('운석 파괴 미니게임', font_40, screen, draw_x, draw_y, YELLOW)
    draw_text('Press The Enter', font_40, screen, draw_x, draw_y + 200, WHITE)
    draw_text('게임을 시작합니다', font_40, screen, draw_x, draw_y + 250, WHITE)

    pygame.display.update()

    for e in pygame.event.get():
        if e.type == pygame.KEYDOWN:
            if e.key == pygame.K_RETURN:  # 엔터값
                return 'play'
        if e.type == QUIT:
            return 'quit'

    return 'game_menu'


def main():
    global screen

    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption('Shooting Game')

    action = 'game_menu'
    while action != 'quit':
        if action == 'game_menu':
            action = game_menu()
        elif action == 'play':
            action = game_loop()

    pygame.quit()


if __name__ == "__main__":
    main()






















