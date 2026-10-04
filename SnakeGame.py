import pygame
import random

GRID_SIZE = 30
BLOCK_SIZE = 20

SCREEN_WIDTH = GRID_SIZE * BLOCK_SIZE
SCREEN_HEIGHT = GRID_SIZE * BLOCK_SIZE

pygame.init()
pygame.sprite.Sprite()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((SCREEN_WIDTH , SCREEN_HEIGHT))
font = pygame.font.SysFont(None, 36)

is_running = True

class Snake(pygame.sprite.Sprite):
    def __init__(self, snake):
        pygame.sprite.Sprite.__init__(self)
        
        self.snake_body = snake
        self.direction = (BLOCK_SIZE , 0)
        self.grow_pending = False
    
    def draw(self,surface):
        for x , y in self.snake_body:
            pygame.draw.rect(surface, "Pink", (x, y, BLOCK_SIZE, BLOCK_SIZE))
    
    def move(self):
        
        dx , dy = self.direction
        self.head = self.snake_body[0]
        self.new_head = (self.head[0] + dx , self.head[1] + dy)  
        
        if not self.grow_pending:
            self.snake_body.insert(0, self.new_head)
            self.snake_body.pop()
        
        if self.grow_pending:
            self.snake_body.insert(0, self.new_head)
            self.grow_pending = False
            
            
        
class Food(pygame.sprite.Sprite):
        def __init__(self):
            pygame.sprite.Sprite.__init__(self)
            
            self.position = (0,0)
            
        
        def respawn(self,snake_body):
            while True:
                self.position = (random.randint(0,GRID_SIZE-1) * BLOCK_SIZE ,random.randint(0,GRID_SIZE-1) * BLOCK_SIZE)
                if self.position not in snake_body:
                    break
        
        def draw(self, surface):
            pygame.draw.rect(surface,"Green", ((self.position),(BLOCK_SIZE, BLOCK_SIZE))) 
            
            
            
        
        
snake = Snake([(100, 100), (80, 100), (60, 100)])
food = Food()
food.respawn(snake.snake_body)
length_snake = 3
Game_over = False

while is_running:
    screen.fill("White")
    
    for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_running = False
            
            if event.type == pygame.KEYDOWN:
                    if (event.key == pygame.K_UP or event.key == pygame.K_w) and snake.direction != (0,BLOCK_SIZE):
                        snake.direction = (0,-BLOCK_SIZE)
                    if (event.key == pygame.K_DOWN or event.key == pygame.K_s) and snake.direction != (0,-BLOCK_SIZE):
                        snake.direction = (0,BLOCK_SIZE)
                    if (event.key == pygame.K_LEFT or event.key == pygame.K_a) and snake.direction != (BLOCK_SIZE,0):
                        snake.direction = (-BLOCK_SIZE,0)
                    if (event.key == pygame.K_RIGHT or event.key == pygame.K_d) and snake.direction != (-BLOCK_SIZE,0):
                        snake.direction = (BLOCK_SIZE,0)
                    
    if not Game_over:
        if snake.snake_body[0] == food.position:
                food.respawn(snake.snake_body)
                snake.grow_pending = True
                length_snake += 1
        
        snake.move()
        if snake.snake_body[0][0] < 0 or snake.snake_body[0][0] >= SCREEN_WIDTH:
            Game_over = True
        if snake.snake_body[0][1] < 0 or snake.snake_body[0][1] >= SCREEN_HEIGHT:
            Game_over = True
        if snake.snake_body[0] in snake.snake_body[1:]:
            Game_over = True
            
        food.draw(screen)
        snake.draw(screen)
            
    else:
        gameover = font.render("Game Over", True, "Red")               
        again = font.render("Play again: Press 'R' to play again", True, "Red")
        screen.blit(gameover, ((SCREEN_WIDTH/2) - 70,(SCREEN_HEIGHT/2)-100))
        screen.blit(again, ((SCREEN_WIDTH/2) - 200,(SCREEN_HEIGHT / 2)))
        keys = pygame.key.get_pressed()
        if keys[pygame.K_r]:
            snake = Snake([(100, 100), (80, 100), (60, 100)])
            food = Food()
            food.respawn(snake.snake_body)
            length_snake = 3
            Game_over = False    
    
    score_text = font.render(f"Length: {length_snake}", True, "Red")
            
    
    screen.blit(score_text, (450,10))
    pygame.display.flip()
    clock.tick(8)

pygame.quit()
    
    