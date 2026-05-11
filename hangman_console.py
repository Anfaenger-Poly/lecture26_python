from hangman import Hangman

print()
print('==========Hangman==========')
word_list = ['apple', 'banana', 'man', 'woman', 'tomato']

# 단어 선택
hangman = Hangman(word_list)
print(f'{hangman.display_word} ({len(hangman.word)}글자)')

while True:
    # 알파벳 입력
    letter = input('>> 알파벳 입력 : ').strip().lower()

    # 정답 확인
    result = hangman.check_letter(letter)
    if result == Hangman.RIGHT:
        print(f'정답: {hangman.display_word}')
    elif result == Hangman.WRONG:
        print(f'오답: {hangman.num_try}회 시도')
    elif result == Hangman.EXIST:
        print(f'이미 입력한 알파벳입니다 : {hangman.tried_letters}')

    # 승패 확인
    result = hangman.is_win()
    if result == Hangman.WIN:
        print(f'You win! : {hangman.num_try}회 시도')
        break
    elif result == Hangman.LOOSE:
        print(f'You loose! : {hangman.word}')
        break