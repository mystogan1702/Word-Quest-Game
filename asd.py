import pygame
import random
import sys

class WordGame:
    def __init__(self):
        pygame.init()
        self.WIDTH, self.HEIGHT = 1280, 720
        self.WHITE = (255, 255, 255)
        self.FONT_SIZE = 30
        self.SCALE_FACTOR = 0.25
        self.SHUFFLE_COOLDOWN_MS = 2000
        self.last_shuffle_time = 0
        self.clock = pygame.time.Clock()

        self.points_font = pygame.font.Font(None, self.FONT_SIZE)

        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Word Game")

        self.letter_images = {letter: pygame.image.load(f'assets/img/letter tiles/{letter}.png') for letter in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'}

        self.word_list = self.load_words('assets/word list 1.txt')

        self.letter_values = {
            'A': 1, 'B': 3, 'C': 3, 'D': 2, 'E': 1, 'F': 4, 'G': 2, 'H': 4, 'I': 1, 'J': 8,
            'K': 5, 'L': 1, 'M': 3, 'N': 1, 'O': 1, 'P': 3, 'Q': 10, 'R': 1, 'S': 1, 'T': 1,
            'U': 1, 'V': 4, 'W': 4, 'X': 8, 'Y': 4, 'Z': 10
        }

        self.background = pygame.image.load('assets/img/bg and cursor/Background.png')

        self.player_hand = []
        self.answer_box = []

        self.player_hand = self.update_player_hand()

    def load_words(self, filename):
        with open(filename, 'r') as file:
            return [word.strip().upper() for word in file.readlines()]

    def shuffle_hand(self, player_hand):
        animation_frames = 20
        original_hand = player_hand.copy()

        for frame in range(animation_frames):
            player_hand.clear()
            player_hand.extend(random.sample(original_hand, len(original_hand)))

            self.draw_game()
            pygame.display.flip()
            self.clock.tick(60)

        return player_hand

    def update_player_hand(self):
        chosen_word = random.choice(self.word_list)
        chosen_word_letters = list(chosen_word)

        valid_words = [word for word in self.word_list if 3 <= len(word) <= 5]
        chosen_word = random.choice(valid_words)
        chosen_word_letters = list(chosen_word)

        needed_letters = max(10 - len(chosen_word_letters), 0)
        new_set_letters = chosen_word_letters + random.sample(list(self.letter_images.keys()), needed_letters)

        return self.shuffle_hand(new_set_letters[:10])

    def calculate_points(self, word):
        points = 0
        for letter in word:
            points += self.letter_values.get(letter, 0)
        return points

    def move_letters(self, target, source, speed=5):
        moved_letters = []
        for letter in source:
            letter_rect = self.letter_images[letter[0]].get_rect()
            while letter_rect.y < target[1]:
                self.draw_game()
                pygame.time.delay(10)
                letter_rect.y += speed
            moved_letters.append(source.pop(source.index(letter)))
        return moved_letters

    def draw_game(self):
        self.screen.blit(self.background, (0, 0))

        for i, letter in enumerate(self.player_hand):
            pygame.draw.rect(self.screen, self.WHITE, (50 + i * 80, 400, 60, 60))
            scaled_image = pygame.transform.scale(self.letter_images[letter[0]], (int(256 * self.SCALE_FACTOR), int(256 * self.SCALE_FACTOR)))
            self.screen.blit(scaled_image, (50 + i * 80, 397))

        pygame.draw.rect(self.screen, self.WHITE, (50, 500, 600, 60))
        for i, letter in enumerate(self.answer_box):
            scaled_image = pygame.transform.scale(self.letter_images[letter[0]], (int(256 * self.SCALE_FACTOR), int(256 * self.SCALE_FACTOR)))
            self.screen.blit(scaled_image, (50 + i * 80, 500))

        pygame.draw.rect(self.screen, (0, 255, 0), (1100, 500, 80, 60))
        self.draw_text('Submit', pygame.font.Font(None, self.FONT_SIZE), (0, 0, 0), 1110, 515)

        pygame.draw.rect(self.screen, (255, 0, 0), (1100, 400, 80, 60))
        self.draw_text('Shuffle', pygame.font.Font(None, self.FONT_SIZE), (0, 0, 0), 1110, 415)

        pygame.draw.rect(self.screen, (255, 255, 0), (1100, 300, 80, 60))
        self.draw_text('Pass', pygame.font.Font(None, self.FONT_SIZE), (0, 0, 0), 1110, 315)

    def pass_turn(self):
        # Update the player's hand and shuffle again
        self.player_hand = self.update_player_hand()
        self.player_hand = self.shuffle_hand(self.player_hand)

    def draw_text(self, text, font, color, x, y):
        text_obj = font.render(text, True, color)
        rect = text_obj.get_rect()
        rect.topleft = (x, y)
        self.screen.blit(text_obj, rect)

    def run_game(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = event.pos
                    for i, letter in enumerate(self.player_hand):
                        if 50 + i * 80 <= x <= 50 + i * 80 + 60 and 400 <= y <= 460:
                            self.answer_box.append(self.player_hand.pop(i))
                    for i, letter in enumerate(self.answer_box):
                        if 50 + i * 80 <= x <= 50 + i * 80 + 60 and 500 <= y <= 560:
                            self.player_hand.append(self.answer_box.pop(i))
                    if 1100 <= x <= 1180 and 500 <= y <= 560:
                        submitted_word = ''.join(self.answer_box)
                        print(f"Submitted word: {submitted_word}")
                        if submitted_word in self.word_list or submitted_word == ''.join(self.player_hand):
                            points = self.calculate_points(submitted_word)
                            if len(submitted_word) == 4:
                                points += 1
                                bonus_text = '+1'
                            else:
                                bonus_text = ''
                            print(f"Valid word! Points: {points}")
                            self.player_hand = self.update_player_hand()
                            self.answer_box = []
                            self.player_hand = self.shuffle_hand(self.player_hand)

                            points_text = self.points_font.render(f'Points: {points}', True, (255, 255, 255))
                            self.screen.blit(points_text, (50, 50))

                            if bonus_text:
                                bonus_text_rendered = self.points_font.render(bonus_text, True, (255, 255, 255))
                                self.screen.blit(bonus_text_rendered, (50, 90))
                        else:
                            print("Invalid word. Letters will go back to player's hand.")
                            self.player_hand.extend(self.answer_box)
                            self.answer_box = []
                    elif 1100 <= x <= 1180 and 400 <= y <= 460:
                        current_time = pygame.time.get_ticks()
                        if current_time - self.last_shuffle_time >= self.SHUFFLE_COOLDOWN_MS:
                            self.player_hand = self.shuffle_hand(self.player_hand)
                            self.last_shuffle_time = current_time
                    elif 1100 <= x <= 1180 and 300 <= y <= 360:
                        self.pass_turn()

            self.draw_game()

            points_text = self.points_font.render(f'Points: {self.calculate_points("".join(self.answer_box))}', True, (255, 255, 255))
            self.screen.blit(points_text, (50, 50))

            if len("".join(self.answer_box)) == 4:
                bonus_text = self.points_font.render('+1', True, (255, 255, 255))
                self.screen.blit(bonus_text, (150, 50))

            pygame.display.flip()
            self.clock.tick(120)