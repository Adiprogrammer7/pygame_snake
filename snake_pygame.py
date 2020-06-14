import pygame
import time
import random

pygame.init()

# defining colors
white = (255, 255, 255)
black = (0, 0, 0)
blue = (0, 0, 255)
red = (255, 0, 0)
green = (0, 255, 0)

display_width = 800
display_height = 600

window = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption("Pysnake")

clock = pygame.time.Clock()
block_size = 15
apple_size = 20
FPS = 10
font = pygame.font.SysFont(None, 30)

# for drawing snake.
def snake(snakelist): #snakelist for all snake blocks for lengthening.
	for xny in snakelist: #xny is just a list inside snakelist which has x and y pos.
		pygame.draw.rect(window, blue, [xny[0], xny[1], block_size, block_size]) 

# to get text surface and text rectangle.
def text_objects(text, color):
	text_surf = font.render(text, True, color)
	text_rect = text_surf.get_rect()
	return text_surf, text_rect

# To display text centered to screen.
def message_to_screen(msg, color):
	text_surf, text_rect = text_objects(msg, color) #getting those objects for out text.
	text_rect.center = (display_width/2), (display_height/2)  #alligning center of our text rect with screen center.
	window.blit(text_surf, text_rect)

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

	# round(x/10.0)*10.0 formula can be used to round any num to multiple of 10.
	# Apple stuff.
	rand_apple_x = round(random.randrange(0, display_width-apple_size))
	rand_apple_y = round(random.randrange(0, display_height-apple_size))

	# Main game loop.
	while not game_exit:
		
		# Loop which will run when we lose in game.
		while game_over == True:
			window.fill(white)
			message_to_screen("You lost, press 'p' to play again or 'q' to exit.", red)
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

		# Boundary condition.
		if x >= display_width or x<0 or y >= display_height or y<0:
			game_over = True

		# moving snake block constantly.
		x += x_change
		y += y_change

		window.fill(white)
		pygame.draw.rect(window, black, [rand_apple_x, rand_apple_y, apple_size, apple_size])

		
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

		pygame.display.update()
		clock.tick(FPS)

		# Crossover handling of snake and apple then generating new apple
		# when either of snake's two x boundries is bet. both x boundries of apple and either of two snake's y boundries is bet. apple's y boundries.
		if (x > rand_apple_x and x < rand_apple_x + apple_size) or (x + block_size > rand_apple_x and x + block_size < rand_apple_x + apple_size):  # X crossover
			if (y > rand_apple_y and y < rand_apple_y + apple_size) or (y + block_size > rand_apple_y and y + block_size < rand_apple_y + apple_size): # Y crossover
				rand_apple_x = round(random.randrange(0, display_width-block_size))
				rand_apple_y = round(random.randrange(0, display_height-block_size))
				snakelen += 1 #to increase snake length

	pygame.quit()
	quit()

gameLoop()
