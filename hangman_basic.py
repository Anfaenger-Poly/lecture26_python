# 자료구조
word_list = ['apple', 'banana', 'man']
limit_error = 7
import random
def select_word():
    word_list = ['apple', 'banana', 'man', 'woman', 'tomato']
    return random.choice(word_list)

# 게임 로직
# 1. computer 단어 선택하고 빈칸 보여주기(몇 글자 인지)
target_word = select_word()
print(">> 컴퓨터가 생각한 단어 : ", target_word)
blank_char = '_'
word_screen = blank_char * len(target_word)

num_error = 0
while num_error < limit_error:

    # 2. 사용자 알파벳 입력
    user_input = input(">> 알파벳을 입력하세요 : ").lower()

    # 3. 게임 상태 업데이트
    # 알파벳이 단어에 있으면 채워주기
    if target_word.find(user_input) == -1: # 없으면 오류 횟수 증가
        num_error += 1
        print(f'오답 : {num_error}회')
    else: # 알파벳이 단어에 있으면 채워주기
        for i in range(len(target_word)):
            if user_input == target_word[i]:
                word_screen = word_screen[:i] + user_input + word_screen[i+1:]
        print('정답 :', word_screen)

    # 4. 단어를 다 맞췄으면(word_screen에 _가 없으면) 사용자 win
    if word_screen.count(blank_char) == 0:
        print("win")
        break

# 5. 틀렸으면 계속 진행, 시도 횟수가 7회 이상이면 loose
if num_error >= limit_error:
    print("loose : ", target_word)