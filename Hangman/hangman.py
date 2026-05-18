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
    ERROR = -2
    
    def __init__(self, word_list):
        self.word = random.choice(word_list).upper() # 대문자로 변환
        self.display_word = Hangman.MASK_CHAR * len(self.word) # 글자 수 만큼
        self.num_try = 0
        self.input_letters = [] # 입력한 알파벳
        self.error_status = ""

    def check_letter(self, letter):
        letter = letter.upper()
        if not letter.isalpha():
            self.error_status = '알파벳을 입력하세요.'
            return Hangman.ERROR
        # 이미 입력했던 문자인지 확인
        if letter in self.input_letters:
            self.error_status = f'이미 입력한 알파벳입니다. {self.input_letters}'
            return Hangman.EXIST
        self.input_letters.append(letter)
        
        if self.word.count(letter) > 0:
            # 알파벳이 단어에 있으면 display_word에서 위치를 찾아 수정
            display_list = list(self.display_word)
            for i in range(len(self.word)):
                if self.word[i] == letter:
                    display_list[i] = letter
            self.display_word = ''.join(display_list)
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