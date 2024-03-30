import pygame
import random
from lowPlatform import *
from settings import *
from platforms import *
from enemies import *
from Clouds import *
vec=pygame.math.Vector2
from os import path


class Game:
    def __init__(self): #инициализация игрового окна и других элементов игры.
        pygame.init()
        self.gameDisplay = pygame.display.set_mode((display_width, display_height))
        self.gameDisplay.fill(white)
        pygame.display.set_caption("Sky Ascend")
        self.clock = pygame.time.Clock()
        self.img_pikachu=pygame.sprite.Sprite()
        self.img_pikachuR = pygame.image.load('data/pikachu_Right.png').convert_alpha()
        self.img_pikachuL = pygame.image.load('data/pikachu_Left.png').convert_alpha()
        self.start_button_img = pygame.image.load('data/play.png').convert_alpha()
        self.img_pikachu.image = self.img_pikachuR
        self.img_pikachu.rect = self.img_pikachu.image.get_rect()
        self.img_pikachu.rect=self.img_pikachu.image.get_rect()
        self.background = pygame.image.load('data/blue_back.jpg').convert()
        self.font = pygame.font.SysFont(None, 25)
        self.gameExit = False
        self.pos=vec(display_width-100,display_height)
        self.img_pikachu.rect.topleft=[self.pos.x,self.pos.y]
        self.vel=vec(0,0)
        self.acc=vec(0,0)
        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.platforms = pygame.sprite.Group()
        self.powerups = pygame.sprite.Group()
        self.playerSprite=pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.clouds = pygame.sprite.Group()
        self.playerSprite.add(self.img_pikachu)
        p1 = lowPlatform(0, display_height - 40, display_width, 40)
        platform_obj=Platform(self)
        self.platform_images=platform_obj.getImages()
        p2=Platform(self)
        p2.getPlatform(display_width/2 - 50,display_height-150,self.platform_images)
        p3 = Platform(self)
        p3.getPlatform(display_width/2 - 100,display_height-300, self.platform_images)
        p4 = Platform(self)
        p4.getPlatform(display_width / 2, display_height - 450, self.platform_images)
        p5 = Platform(self)
        p5.getPlatform(0, display_height - 600, self.platform_images)
        self.platforms.add(p1)
        self.platforms.add(p2)
        self.platforms.add(p3)
        self.platforms.add(p4)
        self.platforms.add(p5)
        self.score=0
        self.count = 0
        self.font_name=pygame.font.match_font(Font_Name)
        self.load_data()
        self.enemies_timer=0
        for i in range(8):
            c=Cloud(self)
            c.rect.y+= 600

    def load_data(self):
        # загрузка рекордного балла из файла
        self.dir = path.dirname(__file__)
        with open(path.join(self.dir, hs_file), 'r+') as f:
            try:
                self.highscore = int(f.read())
            except:
                self.highscore = 0

        # загрузка облаков
        cloud_dir = path.join(self.dir, 'data/clouds_img')
        self.cloud_images=[]
        for i in range(1,4):
            self.cloud_images.append(pygame.image.load(path.join(cloud_dir,'cloud{}.png'.format(i))).convert())

        # загрузка звуков
        self.sound_dir=path.join(self.dir,'data/sounds')
        self.jump_sound=pygame.mixer.Sound(path.join(self.sound_dir,'jump.wav'))
        self.jump_sound.set_volume(0.1)
        self.pow_sound = pygame.mixer.Sound(path.join(self.sound_dir,'springshoes-arcade.mp3'))
        self.falling_sound = pygame.mixer.Sound(path.join(self.sound_dir,'falling-sound-arcade.mp3'))
        self.win_sound =  pygame.mixer.Sound(path.join(self.sound_dir,'win.mp3'))

    def updateScreen(self):
        if self.vel.x < 0:  #Движение влево
            self.img_pikachu.image = self.img_pikachuL
        else:  # Движение вправо
            self.img_pikachu.image = self.img_pikachuR
        now_time=pygame.time.get_ticks()
        if now_time-self.enemies_timer>5000 + random.choice([-1000,-500,0,500,1000]):
            self.enemies_timer=now_time
            Enemies(self)

        enemies_hits=pygame.sprite.spritecollide(self.img_pikachu,self.enemies,False, pygame.sprite.collide_mask)
        if enemies_hits:
            self.gameOver=True
            self.falling_sound.play()

        #Обновление позии спрайтов
        self.img_pikachu.rect.midbottom = [self.pos.x, self.pos.y]
        #Проверка на наличие столкновений между игроком и спрайтами.
        powerup_hits = pygame.sprite.spritecollide(self.img_pikachu, self.powerups, False)
        for x in powerup_hits:
            self.pow_sound.play()
            self.vel.y = power_up_boost

        if self.vel.y > 0:
            hits = pygame.sprite.spritecollide(self.img_pikachu, self.platforms, False)
            if hits:
                lowest = hits[0]
                for hit in hits:
                    if hit.rect.bottom > lowest.rect.bottom:
                        lowest = hit

                if self.pos.x < lowest.rect.right + 30 and self.pos.x > lowest.rect.left - 30:
                    if self.pos.y < lowest.rect.centery:
                        # Добавляем плавное опускание на платформу.
                        self.pos.y = lowest.rect.top
                        self.vel.y = 0

        #Прокрутка экрана вверх по мере продвижения игрока вверх. Уничтожение платформ, которые больше не требуются.
        if self.img_pikachu.rect.top <= display_height / 4:
            if random.randrange(100) < 99 and len(self.clouds) < 10:  # Проверка количества облаков
                Cloud(self)

            self.pos.y+=abs(self.vel.y)

            for cloud in self.clouds:
                cloud.rect.y+=max(abs(self.vel.y / 2), 2)

            for platform in self.platforms:
                platform.rect.y+=abs(self.vel.y)
                if platform.rect.top>=display_height:
                    platform.kill()
                    self.score+=10

            for enemy in self.enemies:
                 enemy.rect.y += abs(self.vel.y)





         #Проверка окочание игры.
        if self.img_pikachu.rect.bottom>display_height:
            self.gameOver=True;
            self.falling_sound.play()
            for sprite in self.platforms:
                sprite.rect.y-=max(self.vel.y,10)

        #Создание новы  х платформ
        while len(self.platforms)<6:#На экране должно быть не менее 6 платформ.
            width=random.randrange(50,100)
            p = Platform(self)
            p.getPlatform(random.randrange(0,display_width-width), random.randrange(-50,-30), self.platform_images)
            self.platforms.add(p)

        for x in self.powerups: #обновление позиции спрайтов
            x.update()

        if self.score == 5000 and self.count == 0:
            self.game_Completed()
            self.count += 1

        self.gameDisplay.fill(black)
        self.enemies.update()
        self.powerups.update()
        self.platforms.update()
        self.clouds.update()
        self.playerSprite.update( )
        self.gameDisplay.blit(self.background,(0,0))
        self.clouds.draw(self.gameDisplay)
        self.platforms.draw(self.gameDisplay)
        self.powerups.draw(self.gameDisplay)
        self.enemies.draw(self.gameDisplay)

        self.playerSprite.draw(self.gameDisplay)
        #Отображение счета
        self.messageToScreen("SCORE: "+(str)(self.score), 25, black, display_width / 2 , 15)
        pygame.display.update()

    def run(self):
        self.score=0
        self.gameOver = False
        while not self.gameExit:
            self.checkEvent()
            self.acc.x+=self.vel.x*player_Fric
            self.vel+=self.acc
            self.pos+=self.vel+0.5*self.acc
            self.checkHorizontalCrossing()
            self.updateScreen()
            self.clock.tick(fps)
            if self.gameOver==True:
                self.gameOverScreen()
        pygame.mixer.music.fadeout(500)

        pygame.quit()
        quit()

    def checkHorizontalCrossing(self):
        if self.pos.x > display_width:
            self.pos.x = 0
        if self.pos.x < 0:
            self.pos.x = display_width
        if self.pos.y == display_height:
            self.gameOver = True
        if self.pos.y == -50:
            self.pos.y = display_height

    def checkEvent(self):
        self.acc = vec(0, gravity)
        self.jump()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.gameExit = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.acc.x = -player_Acc
                if event.key == pygame.K_RIGHT:
                    self.acc.x = player_Acc
                if event.key == pygame.K_SPACE:
                    self.jump()
                if event.key == pygame.K_ESCAPE:
                    self.pauseGame()  # Вызываем метод для паузы игры кнопкой Esc

    def pauseGame(self):
        background_img = pygame.image.load('data/background.png').convert()
        play_button_img = pygame.image.load('data/play.png').convert_alpha()
        # Отображаем фон и кнопку Play
        self.gameDisplay.blit(background_img, (0, 0))
        self.messageToScreen("Score: " + (str)(self.score), 80, white, display_width / 2,
                             display_height / 2 - 50)
        button_x = display_width / 2 - play_button_img.get_width() / 2
        button_y = display_height / 2
        self.gameDisplay.blit(play_button_img, (button_x, button_y))
        play_text_y = button_y + play_button_img.get_height() + 20
        self.messageToScreen("Continue", 60, white, display_width / 2, play_text_y)
        pygame.display.update()

        # Ждем нажатия кнопки Play
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    waiting = False
                    self.gameExit = True
                elif event.type == pygame.MOUSEBUTTONUP or event.type == pygame.KEYDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    button_rect = pygame.Rect(display_width / 2 - play_button_img.get_width() / 2,
                                              display_height / 2,
                                              play_button_img.get_width(),
                                              play_button_img.get_height())
                    if button_rect.collidepoint(mouse_pos):
                        waiting = False
        # Продолжаем игру
        pygame.display.update()

    def messageToScreen(self,msg,size, color, x, y):
        font=pygame.font.Font(self.font_name,size)
        text_surface=font.render(msg,True,color)
        text_rect=text_surface.get_rect()
        text_rect.midtop=(x,y)
        self.gameDisplay.blit(text_surface,text_rect)

    def jump(self):
        # Мы проверяем, стоит ли спрайт игрока на платформе или нет.
        if self.vel.y > 0:
            # Увеличиваем область детекции столкновений на 11 пикселей вниз.
            self.img_pikachu.rect.y += 11
            hits = pygame.sprite.spritecollide(self.img_pikachu, self.platforms, False)
            self.img_pikachu.rect.y -= 11
            if hits:
                self.jump_sound.play()
                self.vel.y = -11

    def startScreen(self):
        start_button_img = pygame.image.load('data/play.png').convert_alpha()
        background_img = pygame.image.load('data/background.png').convert()
        self.gameDisplay.blit(background_img, (0, 0))
        button_x = display_width / 2 - start_button_img.get_width() / 2
        button_y = display_height / 2
        self.gameDisplay.blit(start_button_img, (button_x, button_y))
        play_text_y = button_y + start_button_img.get_height() + 20
        self.messageToScreen("Play", 60, white, display_width / 2, play_text_y)
        highest_score_text_y = play_text_y + 50
        self.messageToScreen("Highest Score: " + str(self.highscore), 45, white, display_width / 2,
                             highest_score_text_y)
        pygame.display.update()
        self.waitForStart()

    def waitForStart(self):
        waiting = True
        while waiting:
            self.clock.tick(fps)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    waiting = False
                    self.gameExit = True
                elif event.type == pygame.MOUSEBUTTONUP or event.type == pygame.KEYDOWN:
                    waiting = False
                    self.gameOver = False
                    self.gameExit = False
        g.run()
    def gameOverScreen(self):
        background2_img = pygame.image.load('data/background2.jpg').convert()
        start_button_img = pygame.image.load('data/play.png').convert_alpha()
        self.gameDisplay.blit(background2_img, (0, 0))
        self.messageToScreen("Score: " + (str)(self.score), 80,white, display_width / 2,
                                 display_height / 2 - 50)
        self.gameDisplay.blit(start_button_img,
                              (display_width / 2 - start_button_img.get_width() / 2, display_height / 2 + 50))
        button_y = display_height / 2
        play_text_y = button_y + start_button_img.get_height() + 20
        self.messageToScreen("Play Again", 60, white, display_width / 2, play_text_y+20)

        if self.score > self.highscore:
            self.highscore = self.score
            self.messageToScreen("CONGRATULATIONS!!!  NEW HIGHEST SCORE!", 30, white, display_width / 2,
                                 display_height / 2 + 10)
            with open(path.join(self.dir, hs_file), 'w') as f:
                f.write(str(self.score))
        else:
            self.messageToScreen("Highest Score: " + str(self.highscore), 45, white, display_width / 2, display_height / 2)

        pygame.display.update()
        self.waitForPlayAgain(start_button_img)

    def waitForPlayAgain(self, start_button_img):
        waiting = True
        while waiting:
            self.clock.tick(fps)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    waiting = False
                    self.gameExit = True
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    button_rect = start_button_img.get_rect(
                        topleft=(display_width / 2 - start_button_img.get_width() / 2, display_height / 2 + 50))
                    if button_rect.collidepoint(mouse_pos):
                        waiting = False
                        self.gameOver = False
                        self.gameExit = False
                if event.type == pygame.KEYDOWN:
                    waiting = False
                    self.gameOver = False
                    self.gameExit = False
        g.__init__()
        g.run()

    def game_Completed(self):
        self.win_sound.play()
        background_img = pygame.image.load('data/background.png').convert()
        play_button_img = pygame.image.load('data/play.png').convert_alpha()
        button_x = display_width / 2 - play_button_img.get_width() / 2
        button_y = display_height / 2
        play_text_y = button_y + play_button_img.get_height() + 20

        waiting = True
        while waiting:
            self.gameDisplay.blit(background_img, (0, 0))
            font = pygame.font.SysFont(None, 33)
            congrats_text = font.render("CONGRATULATIONS!!!", True, (255, 255, 255))
            completed_text = font.render("The game has been successfully completed!", True, (255, 255, 255))
            congrats_text_rect = congrats_text.get_rect(
                center=(display_width / 2, display_height / 4 + 130))
            completed_text_rect = completed_text.get_rect(
                center=(display_width / 2, display_height / 4 + 160))
            self.gameDisplay.blit(congrats_text, congrats_text_rect)
            self.gameDisplay.blit(completed_text, completed_text_rect)
            self.gameDisplay.blit(play_button_img, (button_x, button_y))
            self.messageToScreen("Continue", 60, white, display_width / 2, play_text_y)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    waiting = False
                    self.gameExit = True
                elif event.type == pygame.MOUSEBUTTONUP:
                    mouse_pos = pygame.mouse.get_pos()
                    button_rect = pygame.Rect(display_width / 2 - play_button_img.get_width() / 2,
                                              display_height / 2,
                                              play_button_img.get_width(),
                                              play_button_img.get_height())
                    if button_rect.collidepoint(mouse_pos):
                        waiting = False

        # Продолжаем игру
        pygame.display.update()


g=Game()
g.startScreen()