import random

def select_word():
    word_list = ['apple', 'banana', 'man', 'woman', 'tomato']
    return random.choice(word_list)

# 게임 로직
# 1. computer 단어 선택하고 빈칸 보여주기(몇 글자 인지)
target_word = select_word()
blank_char = '_'
word_screen = blank_char * len(target_word)
print(f'>> {word_screen} ({len(target_word)}글자)')

limit_error = 7
num_error = 0
used_chars = set()

while num_error < limit_error:

    # 2. 사용자 알파벳 입력
    user_input = input(">> 알파벳을 입력하세요 : ").strip().lower()

    # 3. 이미 입력한 알파벳이면 다시 입력
    if user_input in used_chars:
        print(f'>> 이미 입력한 알파벳입니다 : {used_chars}')
        continue
    used_chars.add(user_input)

    # 4. 게임 상태 업데이트
    if target_word.find(user_input) == -1:
        num_error += 1
        print(f'오답 : {num_error}회')
    else:
        for i in range(len(target_word)):
            if user_input == target_word[i]:
                word_screen = word_screen[:i] + user_input + word_screen[i+1:]
        print('정답 :', word_screen)

    # 5. 단어를 다 맞췄으면 사용자 win
    if word_screen.count(blank_char) == 0:
        print(f'You win! : {num_error}회 시도')
        break

# 6. 시도 횟수가 7회 이상이면 loose
else:
    print("You loose! : ", target_word)