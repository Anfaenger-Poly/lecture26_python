import random
class Hangman:
    MAX_TRY = 7
    MASK_CHAR = '_'
    RIGHT = 1
    WRONG = 0
    EXIST = -1
    WIN = 1
    LOOSE = 0
    CONTINUE = -1
    def __init__(self, word_list):
        self.word = random.choice(word_list)
        self.display_word = Hangman.MASK_CHAR * len(self.word) # 글자 수 만큼
        self.num_try = 0
        self.tried_letters = [] # 이미 시도한 알파벳

    def check_letter(self, letter):
        # 이미 입력한 알파벳이면 EXIST 반환
        if letter in self.tried_letters:
            return Hangman.EXIST
        self.tried_letters.append(letter)
        # 알파벳이 단어에 있으면 display_word에서 위치를 찾아 수정
        if self.word.count(letter) > 0:
            for i in range(len(self.word)):
                if self.word[i] == letter:
                    self.display_word = self.display_word[:i] + letter + self.display_word[i+1:]
            return Hangman.RIGHT
        else:
            self.num_try += 1
            return Hangman.WRONG

    def is_win(self):
        # 이겼을 때
        if self.display_word.count(Hangman.MASK_CHAR) == 0:
            return Hangman.WIN
        # 졌을 때
        elif self.num_try >= Hangman.MAX_TRY:
            return Hangman.LOOSE
        return Hangman.CONTINUE