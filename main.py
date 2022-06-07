from random import randint
import pygame

class Coinster:
    """
    A Game in which the robot must collect three coins before exiting through the door.
    The monster is chasing the robot with increasing velocity as the robot collects coins.
    If the monster hits the robot before the robot exits through the door, the player loses.
    The number of coins collected by the robot are shown in the bottom left corner.
    As the monster accelerates, it becomes difficult to make it to the door.
    The number of coins to open the door is set to 3. This can be changed in a later version.
    """
    W = 640
    H = 480
    def __init__(self) -> None:
        pygame.init()
        self.load_images()
        self.new_game()
        self.clock = pygame.time.Clock()        
        self.window = pygame.display.set_mode((Coinster.W, Coinster.H))
        self.game_font = pygame.font.SysFont("Arial", 24, True)
        pygame.display.set_caption("Coinster")
        self.main_loop()
    
    def new_game(self):
        self.coins = 0
        self.to_right = False
        self.to_left = False
        self.to_down = False
        self.to_up = False
        self.robot_wins = False
        self.monster_wins = False
        self.x = Coinster.W / 2 - self.robot.get_width() / 2
        self.y = Coinster.H - self.robot.get_height()
        self.mox = randint(-10, Coinster.W)
        self.moy = randint(-10, Coinster.H)
        self.cox = randint(0, Coinster.W - self.coin.get_width())
        self.coy = randint(0, Coinster.H - self.coin.get_height())
        self.dox = randint(Coinster.W//4, Coinster.W//4*3)
        self.doy = randint(Coinster.H//4, Coinster.H//4*3)

    def main_loop(self):
        while True:
            self.check_events()
            self.draw_window()
            self.clock.tick(60)

    def draw_window(self):
        self.window.fill((80,120,180))
        game_text = self.game_font.render("Coins: " + str(self.coins), True, (255,255,0))
        self.window.blit(game_text, (25, Coinster.H - 25))
        self.chase()
        if self.catch():
            self.monster_wins = True
        self.move()
        if self.exit() and self.coins >= 3:
            self.robot_wins = True
        if self.collect():
            self.coins += 1
            self.cox = randint(0, Coinster.W - self.coin.get_width())
            self.coy = randint(0, Coinster.H - self.coin.get_height())        
        if self.robot_wins:
            self.game_over("Congratulations, you won!")
        elif self.monster_wins:
            self.game_over("Unfortunately you have lost this time :(")
        else:
            if self.coins < 3:
                self.window.blit(self.coin, (self.cox, self.coy))
            else:
                self.window.blit(self.door, (self.dox, self.doy))
            self.window.blit(self.monster, (self.mox, self.moy))
            self.window.blit(self.robot, (self.x, self.y))
        pygame.display.flip()

    def game_over(self, text):        
        game_text = self.game_font.render(text, True, (255,100,10))
        self.window.blit(game_text, (Coinster.W/2 - 225, Coinster.H/2 - 25))
        game_text = self.game_font.render("F2 = new game", True, (255, 100, 10))
        self.window.blit(game_text, (Coinster.W/2 - 225, Coinster.H/2 + 25))
        game_text = self.game_font.render("Esc = exit game", True, (255, 100, 10))
        self.window.blit(game_text, (Coinster.W/2 + 25, Coinster.H/2 + 25))

    def exit(self):
        a = self.dox + self.door.get_width() > self.x > self.dox - self.robot.get_width()
        b = self.doy + self.door.get_height() > self.y > self.doy - self.robot.get_height()
        return a and b

    def catch(self):
        a = self.mox + self.monster.get_width() > self.x > self.mox - self.robot.get_width()
        b = self.moy + self.monster.get_height() > self.y > self.moy - self.robot.get_height()
        return a and b

    def collect(self):
        a = self.cox + self.coin.get_width() > self.x > self.cox - self.robot.get_width()
        b = self.coy + self.coin.get_height() > self.y > self.coy - self.robot.get_height()
        return a and b

    def move(self):
        if self.to_right:
            self.x += 2
            self.x = min(self.x, Coinster.W - self.robot.get_width())
        if self.to_left:
            self.x -= 2
            self.x = max(self.x, 0)
        if self.to_down:
            self.y += 2
            self.y = min(self.y, Coinster.H - self.robot.get_height())
        if self.to_up:
            self.y -= 2
            self.y = max(self.y, 0)
    
    def chase(self):
        dx = self.x - self.mox
        dy = self.y - self.moy
        hypotenus = pow(pow(dx, 2) + pow(dy, 2), 0.5)
        velocity = 1.1 + 0.7 / 3 * self.coins
        self.mox += velocity * dx / hypotenus
        self.moy += velocity * dy / hypotenus

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    self.to_right = True
                if event.key == pygame.K_LEFT:
                    self.to_left = True
                if event.key == pygame.K_DOWN:
                    self.to_down = True
                if event.key == pygame.K_UP:
                    self.to_up = True
                if event.key == pygame.K_F2:
                    self.new_game()
                if event.key == pygame.K_ESCAPE:
                    exit()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT:
                    self.to_right = False
                if event.key == pygame.K_LEFT:
                    self.to_left = False
                if event.key == pygame.K_DOWN:
                    self.to_down = False
                if event.key == pygame.K_UP:
                    self.to_up = False
            if event.type == pygame.QUIT:
                exit()

    def load_images(self):
        self.coin = pygame.image.load("coin.png")
        self.door = pygame.image.load("door.png")
        self.monster = pygame.image.load("monster.png")
        self.robot = pygame.image.load("robot.png")

if __name__ == '__main__':
    Coinster()