import string, button, random
from settings import *


class Tiles:
    def __init__(self):
        self.screen = pygame.display.get_surface()
        self.letters = string.ascii_letters.lower()
        self.tiles_placement_x = 0
        self.tiles_placement_y = 0

    def tiles(self):
        player_hand = []
        word_box = []

        count = 0
        jumlbed_word = ""
        possible_word = ""

        file = open('assets/word list.txt', 'r', encoding='utf-8')
        words = file.read().splitlines()
        while count != 1:
            random_word = str(random.choice(words))
            possible_word = random_word.strip("''[]")
            if len(possible_word) < 5:
                for x in range(4):
                    random_letter = ''.join(random.choices(string.ascii_lowercase))
                    randomLetter = random_letter.strip("[]''")
                    possible_word = randomLetter + possible_word
                    count = 1

        while possible_word:
            position = random.randrange(len(possible_word))
            jumlbed_word += possible_word[position]
            possible_word = possible_word[:position] + possible_word[(position + 1):]

        for letter in jumlbed_word:
            player_hand.append(letter)
        print(player_hand)



Tiles().tiles()









