import pygame
import sys
import random


# moving snake
class Snake:
    def __init__(self): # how the snake will appear at the start of the game
        self.length = 1
        self.positions = [((screen_width / 2), (screen_height / 2))]  # starts centered in the grid
        self.direction = random.choice([up, down, left, right])  # pointing in a random direction
        self.color = (201, 44, 44)
        self.score = 0

    def get_head_position(self):
        return self.positions[0]

    def turn(self, point):
        # if the snake is just one block long, it can move in any of the four directions
        if self.length > 1 and (point[0]*-1, point[1]*-1) == self.direction:
            return
        # if the snake is longer than one block, it cannot turn backwards
        else:
            self.direction = point

    def move(self): #move snake
        # to calculate new position of snake
        cur = self.get_head_position()
        x,y = self.direction
        new = (((cur[0]+(x*gridsize))%screen_width), (cur[1]+(y*gridsize))%screen_height)
        # if length of snake is greater than 2 and the new position of the snake overlaps with any other part
        # of the snake, the game is over
        if len(self.positions) > 2 and new in self.positions[2:]:
            self.reset()
        # otherwise add new head position to the positions list and pop the last element
        else:
            self.positions.insert(0,new)
            if len(self.positions) > self.length:
                self.positions.pop()

    def reset(self): # reset snake position
        self.length = 1
        self.positions = [((screen_width / 2), (screen_height / 2))] # starts centered in the grid
        self.direction = random.choice([up, down, left, right]) # pointing in a random direction
        self.score = 0

    def draw(self,surface): # represent snake on screen
        for p in self.positions:
            r = pygame.Rect((p[0], p[1]), (gridsize,gridsize))
            pygame.draw.rect(surface, self.color, r)
            pygame.draw.rect(surface, (0, 0, 0), r, 1)

    def handle_keys(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.turn(up)
                elif event.key == pygame.K_DOWN:
                    self.turn(down)
                elif event.key == pygame.K_LEFT:
                    self.turn(left)
                elif event.key == pygame.K_RIGHT:
                    self.turn(right)

# moving food
class Food():
    def __init__(self):
        self.position = (0,0)
        self.color = (73, 214, 106)
        self.randomize_position()

    def randomize_position(self): # randomize positive of food
        self.position = (random.randint(0, grid_width-1) * gridsize, random.randint(0, grid_height-1) * gridsize)

    def draw(self, surface): # draw representation of food object
        r = pygame.Rect((self.position[0], self.position[1]), (gridsize, gridsize))
        pygame.draw.rect(surface, self.color, r)
        pygame.draw.rect(surface, (73, 214, 106), r, 1)

# draw the screen and surface that gets updated whenever an action is performed
def drawGrid(surface):
    # double for loop to iterate over each x,y coordinate
    for y in range(0, int(grid_height)):
        for x in range(0, int(grid_width)):
            # to draw gridlines
            if (x+y) % 2 == 0:
                r = pygame.Rect((x*gridsize, y*gridsize), (gridsize,gridsize))
                pygame.draw.rect(surface, (0, 0, 0), r)
            else:
                rr = pygame.Rect((x*gridsize, y*gridsize), (gridsize,gridsize))
                pygame.draw.rect(surface, (20, 20, 20), rr)

# Global variables for important game features
screen_width = 480
screen_height = 480

gridsize = 20
grid_width = screen_width/gridsize
grid_height = screen_height/gridsize

# possible movements of snake
up = (0,-1)
down = (0,1)
left = (-1,0)
right = (1,0)

def main():
    # create screen and game environment
    pygame.init()
    # initialize game and game clock, which keeps track of game at a given time
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((screen_width, screen_height), 0, 32)
    # draw the screen and surface that gets updated whenever an action is performed
    surface = pygame.Surface(screen.get_size())
    surface = surface.convert()
    drawGrid(surface)

    snake = Snake()
    food = Food()

    myfont = pygame.font.SysFont("impact", 16)

    while (True):
        clock.tick(10)
        snake.handle_keys()
        drawGrid(surface)
        snake.move()
        if snake.get_head_position() == food.position:
            snake.length += 1
            snake.score += 1
            food.randomize_position()
        # once an action happens we update + refresh the screen and surface
        snake.draw(surface)
        food.draw(surface)
        screen.blit(surface, (0,0))
        text = myfont.render("Score {0}".format(snake.score), 1, (255, 255, 255))
        screen.blit(text, (5, 10))
        pygame.display.update()

main()

