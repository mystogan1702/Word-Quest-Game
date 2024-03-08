import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 1280, 720
WHITE = (255, 255, 255)
FONT_SIZE = 30
SCALE_FACTOR = 0.5
WORDLIST_FILENAME = 'wordlist.txt'

# Initialize the game window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Word Game")

# Load letter images
letter_images = {letter: pygame.image.load(f'{letter}.png') for letter in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'}

# Load word list
def load_words(filename):
    with open(filename, 'r') as file:
        return [word.strip().upper() for word in file.readlines()]

word_list = load_words(WORDLIST_FILENAME)

# Letter values
letter_values = {
    'A': 1, 'B': 3, 'C': 3, 'D': 2, 'E': 1, 'F': 4, 'G': 2, 'H': 4, 'I': 1, 'J': 8,
    'K': 5, 'L': 1, 'M': 3, 'N': 1, 'O': 1, 'P': 3, 'Q': 10, 'R': 1, 'S': 1, 'T': 1,
    'U': 1, 'V': 4, 'W': 4, 'X': 8, 'Y': 4, 'Z': 10
}

# Background image
background = pygame.image.load('background.jpg')

# Function to draw text on the screen
def draw_text(text, font, color, surface, x, y):
    text_obj = font.render(text, True, color)
    rect = text_obj.get_rect()
    rect.topleft = (x, y)
    surface.blit(text_obj, rect)

# Function to shuffle player hand
def shuffle_hand(player_hand):
    animation_frames = 20  # Number of frames for the shuffle animation
    original_hand = player_hand.copy()

    for frame in range(animation_frames):
        player_hand.clear()
        player_hand.extend(random.sample(original_hand, len(original_hand)))

        # Draw the game during the shuffle animation
        draw_game()
        pygame.time.delay(20)  # Adjust the delay for smoother animation

    return player_hand

# Function to update player hand after submission
def update_player_hand():
    chosen_word = random.choice(word_list)
    chosen_word_letters = list(chosen_word)
    needed_letters = max(7 - len(chosen_word_letters), 0)
    new_set_letters = chosen_word_letters + random.sample(list(letter_images.keys()), needed_letters)
    return shuffle_hand(new_set_letters)  # Shuffle the letters in the player's hand

# Function to calculate points for a word
def calculate_points(word):
    points = 0
    for letter in word:
        points += letter_values.get(letter, 0)
    return points

# Function to smoothly move letters with animation
def move_letters(target, source, speed=5):
    moved_letters = []
    for letter in source:
        letter_rect = letter_images[letter[0]].get_rect()
        while letter_rect.y < target[1]:
            draw_game()
            pygame.time.delay(10)
            letter_rect.y += speed
        moved_letters.append(source.pop(source.index(letter)))
    return moved_letters

# Function to draw the game
def draw_game():
    screen.blit(background, (0, 0))  # Draw background

    # Draw player hand
    for i, letter in enumerate(player_hand):
        pygame.draw.rect(screen, WHITE, (50 + i * 80, 400, 60, 60))
        scaled_image = pygame.transform.scale(letter_images[letter[0]], (int(256 * SCALE_FACTOR), int(256 * SCALE_FACTOR)))
        screen.blit(scaled_image, (75 + i * 80, 415))

    # Draw answer box
    pygame.draw.rect(screen, WHITE, (50, 500, 600, 60))
    for i, letter in enumerate(answer_box):
        scaled_image = pygame.transform.scale(letter_images[letter[0]], (int(256 * SCALE_FACTOR), int(256 * SCALE_FACTOR)))
        screen.blit(scaled_image, (75 + i * 80, 515))

    # Draw submit button
    pygame.draw.rect(screen, (0, 255, 0), (1100, 500, 80, 60))
    draw_text('Submit', pygame.font.Font(None, FONT_SIZE), (0, 0, 0), screen, 1110, 515)

    # Draw shuffle button
    pygame.draw.rect(screen, (255, 0, 0), (1100, 400, 80, 60))
    draw_text('Shuffle', pygame.font.Font(None, FONT_SIZE), (0, 0, 0), screen, 1110, 415)

    pygame.display.flip()

# Initialize player's hand
player_hand = []

# Initialize answer box
answer_box = []

# Game loop
running = True
clock = pygame.time.Clock()
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            # Check if the mouse click is within a letter tile in player hand
            for i, letter in enumerate(player_hand):
                if 50 + i * 80 <= x <= 50 + i * 80 + 60 and 400 <= y <= 460:
                    answer_box.append(player_hand.pop(i))
            # Check if the mouse click is within a letter tile in the answer box
            for i, letter in enumerate(answer_box):
                if 50 + i * 80 <= x <= 50 + i * 80 + 60 and 500 <= y <= 560:
                    player_hand.append(answer_box.pop(i))
            # Check if the mouse click is within the submit button
            if 1100 <= x <= 1180 and 500 <= y <= 560:
                submitted_word = ''.join(answer_box)
                print(f"Submitted word: {submitted_word}")
                if submitted_word in word_list or submitted_word == ''.join(player_hand):
                    points = calculate_points(submitted_word)
                    print(f"Valid word! Points: {points}")
                    player_hand = update_player_hand()
                    answer_box = []
                else:
                    print("Invalid word. Try again.")
            # Check if the mouse click is within the shuffle button
            elif 1100 <= x <= 1180 and 400 <= y <= 460:
                player_hand = shuffle_hand(player_hand)

    draw_game()
    clock.tick(30)  # Limit the frame rate to 30 FPS

pygame.quit()
sys.exit()
