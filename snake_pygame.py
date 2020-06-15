import pygame
import time
import random

pygame.init()

# defining colors
white = (255, 255, 255)
black = (0, 0, 0)
blue = (0, 0, 255)
red = (255, 0, 0)
green = (0, 180, 0)

display_width = 800
display_height = 600

window = pygame.display.set_mode((display_width, display_height))
apple_img = pygame.image.load("img/apple_sprite.png")
icon = pygame.image.load("img/icon.jpeg")
pygame.display.set_caption("Pysnake")
pygame.display.set_icon(icon)

clock = pygame.time.Clock()
block_size = 15
apple_size = 30  #changing apple_size will need to change apple sprite size too. 
FPS = 10

# for drawing snake.
def snake(snakelist): #snakelist for all snake blocks for lengthening.
	for xny in snakelist: #xny is just a list inside snakelist which has x and y pos.
		pygame.draw.rect(window, blue, [xny[0], xny[1], block_size, block_size]) 

# to get text surface and text rectangle.
def text_objects(text, color, font_size):
	font = pygame.font.SysFont("comicsansms", font_size)
	text_surf = font.render(text, True, color)
	text_rect = text_surf.get_rect()
	return text_surf, text_rect

# To display text centered to screen.
# y-asix pos of text can be changed by changing y_displacement variable. 
def message_to_screen(msg, color, y_displacement= 0, font_size= 26):
	text_surf, text_rect = text_objects(msg, color, font_size) #getting those objects for out text.
	text_rect.center = (display_width/2), (display_height/2) + y_displacement  #alligning center of our text rect with screen center/with some y-axis displacement.
	window.blit(text_surf, text_rect)

def score(score_num):
	font = pygame.font.SysFont("comicsansms", 22)
	text = font.render("Score: {}".format(str(score_num)), True, black)
	window.blit(text, (0, 0))

def pause():
	pause = True
	message_to_screen("Paused", black, -50, 50)
	message_to_screen("Press any key to continue...", black, 10, 24 )
	while pause:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				quit()
			if event.type == pygame.KEYDOWN:
				pause = False
		pygame.display.update()
		clock.tick(5)

def game_intro():
	intro = True
	while intro:
		window.fill(white)
		message_to_screen("Welcome to Pysnake", green, -65, 54)
		message_to_screen("Just eat as much as apples to gain length and score", black, font_size= 22)
		message_to_screen("And don't run into yourself like an idiot :)", black, 35, font_size= 22)
		message_to_screen("Press any key to start the game...", black, 100)
		message_to_screen("(you can press 'ESC' to pause the game)", black, 130, 22)
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				quit()
			if event.type == pygame.KEYDOWN:
				intro = False
				
		pygame.display.update()
		clock.tick(15)	

def gameLoop():
	game_exit = False
	game_over = False

	# Snake block stuff.
	x = 300
	y = 300
	x_change = 0
	y_change = 0
	snakelist = [] #all snake block pos
	snakelen = 1 #initial snake size
	score_num = 0

	# round(x/10.0)*10.0 formula can be used to round any num to multiple of 10.
	# Apple stuff.
	rand_apple_x = round(random.randrange(0, display_width-apple_size))
	rand_apple_y = round(random.randrange(0, display_height-apple_size))

	# Main game loop.
	while not game_exit:
		
		# Loop which will run when we lose in game.
		while game_over == True:
			window.fill(white)
			message_to_screen("Game Over!", red, -50, font_size= 54)
			message_to_screen("Press 'p' to play again or 'q' to quit", black, 20, font_size= 36)
			pygame.display.update()
			# taking input from user either to play again or quit.
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					game_over = False
					game_exit = True
				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_q:
						game_over = False
						game_exit = True
					elif event.key == pygame.K_p:
						gameLoop()

		# Event handling loop for playing game.
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				game_exit = True
			# Movement handling.
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_LEFT:
					x_change = -block_size
					y_change = 0
				elif event.key == pygame.K_RIGHT:
					x_change = block_size
					y_change = 0
				elif event.key == pygame.K_UP:
					x_change = 0
					y_change = -block_size
				elif event.key == pygame.K_DOWN:
					x_change = 0
					y_change = block_size
				elif event.key == pygame.K_ESCAPE:
					pause()

		# Boundary condition.
		if x >= display_width or x<0 or y >= display_height or y<0:
			game_over = True

		# moving snake block constantly.
		x += x_change
		y += y_change

		window.fill(white)
		window.blit(apple_img, (rand_apple_x, rand_apple_y))
		
		snakehead = [] #for head of snake(new block as x and y changes)
		snakehead.append(x)
		snakehead.append(y)
		snakelist.append(snakehead)
		# to keep snake length only as much allowed.
		if len(snakelist) > snakelen:
			del snakelist[0] #deleting older blocks(blocks at snake's tail)

		# to check if snake ran into itself.
		for each_snake_block in snakelist[:-1]: #all snake block except current snake head which is last list element.
			if each_snake_block == snakehead:
				game_over = True

		snake(snakelist) 
		score(score_num)
		pygame.display.update()
		clock.tick(FPS)

		# Crossover handling of snake and apple then generating new apple
		# when either of snake's two x boundries is bet. both x boundries of apple and either of two snake's y boundries is bet. apple's y boundries.
		if (x > rand_apple_x and x < rand_apple_x + apple_size) or (x + block_size > rand_apple_x and x + block_size < rand_apple_x + apple_size):  # X crossover
			if (y > rand_apple_y and y < rand_apple_y + apple_size) or (y + block_size > rand_apple_y and y + block_size < rand_apple_y + apple_size): # Y crossover
				rand_apple_x = round(random.randrange(0, display_width-apple_size))
				rand_apple_y = round(random.randrange(0, display_height-apple_size))
				snakelen += 1 #to increase snake length
				score_num += 1

	pygame.quit()
	quit()

game_intro()
gameLoop()
