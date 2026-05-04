# 1. 컴퓨터가 숫자를 생각한다. (0, 1 제외)
# 2. 사용자가 숫자를 말한다.
# 3. 숫자가 맞으면 사용자 win
# 4. 틀리면 컴퓨터가 up or down을 알려준다.
# 5. 2~4번까지 반복 7번 반복
# 6. 7번 내에 맞추지 못하면 computer win

import random
limit = 100
attemps = 7

def guess_number():
    number = random.randint(1, limit)
    print("숫자를 맞춰보세요 (1~%d)" % limit)
    for i in range(attemps):
        user_input = int(input("숫자를 입력하세요"))
        if user_input == number:
            print("숫자를 맞췄습니다")
            return
        elif user_input < number:
            print("UP")
        else:
            print("DOWN")
        print("남은 기회 = %d" % (attemps -i -1))
    print("정답은 %d 였습니다" % number)
guess_number()