class Account:
    def __init__(self, account_no, owner, balance):
        self.__account_no = account_no
        self.__owner = owner
        self.__balance = balance

    def deposit(self, amount):
        self.__balance += amount

    def withdraw(self, amount):
        if self.__balance < amount:
            print('잔액이 부족합니다')
            return False
        self.__balance -= amount
        return True

    def __str__(self):
        return f'계좌번호: {self.__account_no} | 계좌주: {self.__owner} | 잔액: {self.__balance}'

    def get_account_no(self):
        return self.__account_no
    
    def get_owner(self):
        return self.__owner
    
    def get_balance(self):
        return self.__balance


class AccountService:
    def __init__(self):
        self.__account_list = []

    def create_account(self, account_no, owner, balance):
        account = Account(account_no, owner, balance)
        self.__account_list.append(account)
        return True

    def list_account(self):
        return self.__account_list

    def deposit(self, account_no, amount):
        for account in self.__account_list:
            if account.get_account_no() == account_no:
                account.deposit(amount)
                print(f'결과 : {amount}원 입금되었습니다. 잔액: {account.get_balance()}')
                return True
        print('결과 : 존재하지 않는 계좌입니다.')
        return False

    def withdraw(self, account_no, amount):
        for account in self.__account_list:
            if account.get_account_no() == account_no:
                return account.withdraw(amount)
        print('결과 : 존재하지 않는 계좌입니다.')
        return False