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
block_size = 10
FPS = 15
font = pygame.font.SysFont(None, 30)

# for drawing snake.
def snake(snakelist): #snakelist for all snake blocks for lengthening.
	for xny in snakelist: #xny is just a list inside snakelist which has x and y pos.
		pygame.draw.rect(window, blue, [xny[0], xny[1], block_size, block_size]) 

# To display text to screen.
def message_to_screen(msg, color):
	screen_text = font.render(msg, True, color) #created text.
	window.blit(screen_text, [display_width/2, display_height/2]) #now defined postion for text.

def gameLoop():
	game_exit = False
	game_over = False

	# Snake block stuff.
	x = 300
	y = 300
	x_change = 0
	y_change = 0
	snakelist = [] #all snake block pos
	snakelen = 1 #allowed snake size

	# Apple stuff.
	# using round(x/10.0)*10.0 formula to round any num to multiple of 10 so that apple will perfectly align with our snake block.
	rand_apple_x = round(random.randrange(0, display_width-block_size)/10.0)*10.0
	rand_apple_y = round(random.randrange(0, display_height-block_size)/10.0)*10.0

	# Main game loop.
	while not game_exit:
		
		# Loop which will run when we lose in game.
		while game_over == True:
			window.fill(white)
			message_to_screen("You lost, press 'p' to play again or 'q' to exit.", red)
			pygame.display.update()
			# taking input from user either to play again or quit.
			for event in pygame.event.get():
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
		pygame.draw.rect(window, black, [rand_apple_x, rand_apple_y, block_size, block_size])

		
		snakehead = [] #for head of snake(new block as x and y changes)
		snakehead.append(x)
		snakehead.append(y)
		snakelist.append(snakehead)
		# to keep snake length only as much allowed.
		if len(snakelist) > snakelen:
			del snakelist[0] #deleting older blocks(blocks at snake's tail)

		# to check if snake ran into itself.
		for each_snake_block in snakelist[:-1]: #all snake block except current snake head which is last list element.
			
		snake(snakelist) 

		pygame.display.update()
		clock.tick(FPS)

		# Crossover handling of snake and apple then generating new apple
		if x == rand_apple_x and y == rand_apple_y:
			rand_apple_x = round(random.randrange(0, display_width-block_size)/10.0)*10.0
			rand_apple_y = round(random.randrange(0, display_height-block_size)/10.0)*10.0
			snakelen += 1 #to increase snake length

	pygame.quit()
	quit()

gameLoop()
