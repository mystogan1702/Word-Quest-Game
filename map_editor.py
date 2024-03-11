import pygame
import button
import csv

pygame.init()

clock = pygame.time.Clock()
FPS = 60

save_cooldown = 0
load_cooldown = 0
cooldown_duration = 5
loading_in_progress = False
saving_in_progress = False

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
LOWER_MARGIN = 100
SIDE_MARGIN = 300

screen = pygame.display.set_mode((SCREEN_WIDTH + SIDE_MARGIN, SCREEN_HEIGHT + LOWER_MARGIN))
pygame.display.set_caption('Level Editor')


ROWS = 16
MAX_COLS = 150
TILE_SIZE = SCREEN_HEIGHT // ROWS
TILE_TYPES = 20
level = 0
current_tile = 0
scroll_left = False
scroll_right = False
scroll = 0
scroll_speed = 1

save_text_show = False
load_text_show = False
counter = 5
pygame.time.set_timer(pygame.USEREVENT, 1000)


img_list = []
for x in range(TILE_TYPES):
	img = pygame.image.load(f'assets/img/tile/{x}.png').convert_alpha()
	img = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))
	img_list.append(img)

save_img = pygame.image.load('assets/img/buttons/Save.png').convert_alpha()
load_img = pygame.image.load('assets/img/buttons/Load.png').convert_alpha()
background_img = pygame.image.load('assets/img/bg and cursor/Battle_Field.png').convert_alpha()


GREEN = (144, 201, 120)
WHITE = (255, 255, 255)
RED = (200, 25, 25)


font = pygame.font.SysFont('Futura', 30)


world_data = []
for row in range(ROWS):
	r = [-1] * MAX_COLS
	world_data.append(r)


for tile in range(0, MAX_COLS):
	world_data[ROWS - 1][tile] = 0


def draw_text(text, font, text_col, x, y):
	img = font.render(text, True, text_col)
	screen.blit(img, (x, y))


def draw_bg():
	screen.fill(GREEN)
	width = background_img.get_width()
	for x in range(5):
		screen.blit(background_img, ((x * width) - scroll * 0.8, SCREEN_HEIGHT - background_img.get_height()))


def draw_grid():

	for c in range(MAX_COLS + 1):
		pygame.draw.line(screen, WHITE, (c * TILE_SIZE - scroll, 0), (c * TILE_SIZE - scroll, SCREEN_HEIGHT))

	for c in range(ROWS + 1):
		pygame.draw.line(screen, WHITE, (0, c * TILE_SIZE), (SCREEN_WIDTH, c * TILE_SIZE))


def draw_world():
	for y, row in enumerate(world_data):
		for x, tile in enumerate(row):
			if tile >= 0:
				screen.blit(img_list[tile], (x * TILE_SIZE - scroll, y * TILE_SIZE))


save_button = button.Button(SCREEN_WIDTH // 2, SCREEN_HEIGHT + LOWER_MARGIN - 50, save_img, 1.5)
load_button = button.Button(SCREEN_WIDTH // 2 + 200, SCREEN_HEIGHT + LOWER_MARGIN - 50, load_img, 1.5)

button_list = []
button_col = 0
button_row = 0
for i in range(len(img_list)):
	tile_button = button.Button(SCREEN_WIDTH + (75 * button_col) + 50, 75 * button_row + 50, img_list[i], 1)
	button_list.append(tile_button)
	button_col += 1
	if button_col == 3:
		button_row += 1
		button_col = 0

run = True
while run:

	clock.tick(FPS)

	draw_bg()
	draw_grid()
	draw_world()

	draw_text(f'Level: {level}', font, WHITE, 10, SCREEN_HEIGHT + LOWER_MARGIN - 90)
	draw_text('Press UP or DOWN to change level', font, WHITE, 10, SCREEN_HEIGHT + LOWER_MARGIN - 60)
	draw_text('Right Click to Place or Left Click to Remove', font, WHITE, 10, SCREEN_HEIGHT + LOWER_MARGIN - 30)

	if load_button.draw(screen) and not saving_in_progress:
		if load_cooldown == 0:
			load_text_show = True
			loading_in_progress = True  # Set flag to indicate load action in progress

			scroll = 0
			with open(f'assets/level{level}_data.csv', newline='') as csvfile:
				reader = csv.reader(csvfile, delimiter=',')
				for x, row in enumerate(reader):
					for y, tile in enumerate(row):
						world_data[x][y] = int(tile)

			load_cooldown = cooldown_duration * FPS

	if save_button.draw(screen) and not loading_in_progress:
		if save_cooldown == 0:
			save_text_show = True
			saving_in_progress = True  # Set flag to indicate save action in progress

			with open(f'assets/level{level}_data.csv', 'w', newline='') as csvfile:
				writer = csv.writer(csvfile, delimiter=',')
				for row in world_data:
					writer.writerow(row)

			save_cooldown = cooldown_duration * FPS

	if save_cooldown > 0:
		save_cooldown -= 1
	if load_cooldown > 0:
		load_cooldown -= 1

	if saving_in_progress and save_cooldown == 0:
		saving_in_progress = False
	if loading_in_progress and load_cooldown == 0:
		loading_in_progress = False

	pygame.draw.rect(screen, GREEN, (SCREEN_WIDTH, 0, SIDE_MARGIN, SCREEN_HEIGHT))

	button_count = 0
	for button_count, i in enumerate(button_list):
		if i.draw(screen):
			current_tile = button_count

	pygame.draw.rect(screen, RED, button_list[current_tile].rect, 3)

	if scroll_left == True and scroll > 0:
		scroll -= 5 * scroll_speed
	if scroll_right == True and scroll < (MAX_COLS * TILE_SIZE) - SCREEN_WIDTH:
		scroll += 5 * scroll_speed

	pos = pygame.mouse.get_pos()
	x = (pos[0] + scroll) // TILE_SIZE
	y = pos[1] // TILE_SIZE

	if pos[0] < SCREEN_WIDTH and pos[1] < SCREEN_HEIGHT:
		if pygame.mouse.get_pressed()[0] == 1:
			if world_data[y][x] != current_tile:
				world_data[y][x] = current_tile
		if pygame.mouse.get_pressed()[2] == 1:
			world_data[y][x] = -1

	if save_text_show:
		draw_text(f'Level {level} Map: Saved', font, WHITE, ((SCREEN_WIDTH // 2) + 50), SCREEN_HEIGHT + LOWER_MARGIN - 90)
	if load_text_show:
		draw_text(f'Level {level} Map: Loaded', font, WHITE, ((SCREEN_WIDTH // 2) + 50), SCREEN_HEIGHT + LOWER_MARGIN - 90)

	for event in pygame.event.get():
		if save_text_show:
			if event.type == pygame.USEREVENT:
				counter -= 1
			if counter == 0:
				save_text_show = False
				counter = 5
		if load_text_show:
			if event.type == pygame.USEREVENT:
				counter -= 1
			if counter == 0:
				load_text_show = False
				counter = 5
		if event.type == pygame.QUIT:
			run = False
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_UP:
				level += 1
			if event.key == pygame.K_DOWN and level > 0:
				level -= 1
			if event.key == pygame.K_LEFT:
				scroll_left = True
			if event.key == pygame.K_RIGHT:
				scroll_right = True
			if event.key == pygame.K_RSHIFT:
				scroll_speed = 5
			if event.key == pygame.K_ESCAPE:
				run = False

		if event.type == pygame.KEYUP:
			if event.key == pygame.K_LEFT:
				scroll_left = False
			if event.key == pygame.K_RIGHT:
				scroll_right = False
			if event.key == pygame.K_RSHIFT:
				scroll_speed = 1

	pygame.display.update()

pygame.quit()

