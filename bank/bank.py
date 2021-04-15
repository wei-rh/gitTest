# 银行操作
#   开户, 查询, 存款, 取款, 转账, 改密, 锁卡, 解锁, 补卡, 销户, 退出
from cards import Card
from users import User
import random
import pickle
import os
import time


class Bank:
    def __init__(self):
        self.users = []  # 当前银行的所有用户
        self.file_path = 'users.txt'  # 本地文件路径
        # 启动银行系统后,立刻获取user.txt文件中之前保存的所有用户
        self.__get_users()
        print('=> 原来的所有用户:', self.users)

    # 保存用户到文件中
    def __save_users(self):
        # 写入文件
        fp = open(self.file_path, 'wb')
        pickle.dump(self.users, fp)
        fp.close()
        print('=> 当前的所有用户:', self.users)

    #  每次运行项目后都要重新获取user.txt文件中的所有用户
    def __get_users(self):
        #  读取文件
        if os.path.exists(self.file_path):
            fp = open(self.file_path, 'rb')
            self.users = pickle.load(fp)
            fp.close()

    # 开户
    def create_user(self):
        # 1.创建卡
        #  卡号
        cardid = self.__create_cardid()
        print('=> 创建卡号:', cardid)
        # 卡密码
        passwd = self.__set_password()
        if not passwd:
            return
        # 卡余额
        money = float(input('请您输入要预存的金额:'))
        # 创建卡对象
        card = Card(cardid, passwd, money)
        print('=> 创建卡成功:', card)
        self.__Cutdown(3)

        #  2.创建用户
        name = input('请输入您的真实姓名:')
        idcard = input('请输入您的身份证号码:')
        phone = input('请输入您的手机号码:')
        #  创建用户
        user = User(name, phone, idcard, card)
        print('=> 创建用户成功:', user)
        self.__Cutdown(3)

        # 3.存储用户信息
        # 将新用户加入到银行系统中
        self.users.append(user)
        # 存储
        self.__save_users()

    # 创建随机,唯一卡号
    def __create_cardid(self):
        while True:
            # 生成随机卡号
            cardid = '8888'
            for i in range(4):
                cardid += str(random.randint(0, 9))
            # 如果有一个用户的卡号和新生成的卡号相同,则break继续执行while
            # 否则返回卡号
            for user in self.users:
                if user.card.cardid == cardid:
                    break
            else:
                return cardid

    # 设置密码
    def __set_password(self):
        # 允许输错3次
        for i in range(3):
            passwd = input('请您输入密码:')
            passwd2 = input('请再输入一次:')
            #  验证两次密码是否一致
            if passwd == passwd2:
                return passwd
            print('=> 2次密码不一致,请重新输入...')
            self.__Cutdown(3)
        else:
            print('=> 您输入了3次错误的密码.')
            self.__Cutdown(3)
            return False

    # 查询
    def search_money(self):
        pass
        # 1.输入卡号
        user = self.__input_cardid('查询')
        if not user:
            print('=> 卡号不存在.')
            self.__Cutdown(3)
            return
        # 2.输入密码
        passwd = self.__input_passwd(user, 3)
        if not passwd:
            user.card.islock = True
            self.__save_users()
        if self.__check_lock(passwd):
            # 3.显示余额
            print('当前余额:', user.card.money)
            self.__Cutdown(3)

    # 输入卡号
    def __input_cardid(self, serve):
        cardid = input(f'请输入要{serve}的银行卡号:')
        # 如果卡号存在,则返回卡对应的用户对象,否则默认返回None
        for user in self.users:
            if user.card.cardid == cardid:
                return user

    # 输入密码
    def __input_passwd(self, user, n):
        # 2.输入密码
        for i in range(n):
            passwd = input('请输入银行卡密码:')
            if user.card.passwd == passwd:
                return user
            print(f'=> 密码错误{i + 1}次,请重新输入!输错{n}次卡将被锁!')
            self.__Cutdown(3)
        else:
            print('密码输错多次,卡已被锁!')
            self.__Cutdown(3)

    # 存款
    def save_money(self):
        # 1.输入卡号
        user = self.__input_cardid('存款')
        if not user:
            print('=> 卡号不存在.')
            self.__Cutdown(3)
            return
        # 2.输入密码
        passwd = self.__input_passwd(user, 3)
        if not passwd:
            user.card.islock = True
            self.__save_users()
        if self.__check_lock(passwd):
            # 3. 输入存款金额,并将user.card.money+=100
            other = float(input('存入金额为:(圆)'))
            user.card.money += other
            # 4. self.__save_users(),保存
            self.__save_users()

    # 取款
    def get_money(self):
        pass
        # 1.输入卡号
        user = self.__input_cardid('取款')
        if not user:
            print('=> 卡号不存在.')
            self.__Cutdown(3)
            return
        # 2.输入密码
        passwd = self.__input_passwd(user, 3)
        if not passwd:
            user.card.islock = True
            self.__save_users()
        if self.__check_lock(passwd):
            # 3. 输入存款金额,并将user.card.money-=100
            pay = float(input('输入取款金额(圆):'))
            if user.card.money - pay < 0:
                print('余额不足!')
                self.__Cutdown(3)
                return
            # 4. self.__save_users(),保存
            user.card.money -= pay
            print(f'取款成功!余额为:{user.card.money}圆')
            self.__Cutdown(3)
            self.__save_users()

    # 转账
    def transform_money(self):
        pass
        # 1. 输入转出卡号
        user1 = self.__input_cardid('转出')
        if not user1:
            print('=> 卡号不存在.')
            self.__Cutdown(3)
            return
        # 2.输入密码
        passwd = self.__input_passwd(user1, 3)
        if not passwd:
            user1.card.islock = True
            self.__save_users()
        if self.__check_lock(passwd):
            # 3. 输入对方卡号
            user2 = self.__input_cardid('转入')
            if not user2:
                print('=> 卡号不存在.')
                self.__Cutdown(3)
                return
            # 4. 输入存款金额,并将user.card.money-=100
            pay = float(input('请输入转账金额(圆):'))
            if user1.card.money - pay < 0:
                print('余额不足,转账失败!')
                self.__Cutdown(3)
                return
            y = input(f'确定向{user2.name[:1]}*转账{pay}圆吗?确定请按y,取消请按n')
            if y == 'y':
                user1.card.money -= pay
                #       修改对方余额
                user2.card.money += pay
                print('转账成功!')
                self.__Cutdown(3)
                # 5. self.__save_users(),保存
                self.__save_users()
            else:
                print('转账已取消')
                self.__Cutdown(3)

    # 改密
    def modify_password(self):
        pass
        user1 = self.__input_cardid('修改密码')
        if not user1:
            print('=>账号不存在')
            self.__Cutdown(3)
            return
        # 2.输入身份证
        id = input('请输入身份证号码:')
        if id != user1.idcard:
            print('身份验证失败!')
            self.__Cutdown(3)
            return
        # 3.修改密码
        user1.card.passwd = self.__set_password()
        # 4. self.__save_users(),保存
        self.__save_users()

    # 锁卡
    def lock_card(self):
        # 1. 输入转出卡号
        user1 = self.__input_cardid('锁卡')
        if not user1:
            print('=> 卡号不存在.')
            self.__Cutdown(3)
            return
        # 2.输入密码
        passwd = self.__input_passwd(user1, 3)
        if not passwd:
            user1.card.islock = True
            self.__save_users()
        # 3. user.card.islock = True
        user1.card.islock = True
        print('卡已锁定!')
        self.__Cutdown(3)
        # 4.self.__save_users(),保存
        self.__save_users()

    # 解锁
    def unlock_card(self):
        pass
        # 1. 输入转出卡号
        user1 = self.__input_cardid('解锁')
        if not user1:
            print('=> 卡号不存在.')
            self.__Cutdown(3)
            return
        # 2.输入密码
        passwd = self.__input_passwd(user1, 3)
        if not passwd:
            user1.card.islock = True
            self.__save_users()
            # 3. user.card.islock = False
        user1.card.islock = False
        print('卡已解锁!')
        self.__Cutdown(3)
        # 4.self.__save_users(),保存
        self.__save_users()

    # 补卡
    def makeup_card(self):
        pass
        # 1. 输入身份证
        id = self.__input_idcard()
        if not id:
            print('身份验证失败!')
            self.__Cutdown(3)
            return
        # 2. 创建新卡,并替换新卡 user.card = newcard
        cardid = self.__create_cardid()
        print('=> 创建卡号:', cardid)
        self.__Cutdown(3)
        # 卡密码
        passwd = self.__set_password()
        if not passwd:
            return
        # 卡余额
        money = id.card.money
        # 创建卡对象
        newcard = Card(cardid, passwd, money)
        print('=> 创建卡成功:', newcard)
        self.__Cutdown(3)

        id.card = newcard
        # 3.  self.__save_users(),保存
        self.__save_users()

    def __input_idcard(self):
        id = input('请输入身份证号码:')
        # 如果身份证号存在,则返回卡对应的用户对象,否则默认返回None
        for user in self.users:
            if user.idcard == id:
                return user

    # 销户
    def delete_user(self):
        id = self.__input_idcard()
        if not id:
            print('身份验证失败!')
            self.__Cutdown(3)
            return
        print(f'归还用户卡内的余额:{id.card.money}圆')
        self.__Cutdown(3)
        self.users.remove(id)
        print(f'用户{id}已删除!')
        self.__Cutdown(3)
        self.__save_users()

    def __check_lock(self, passwd_user):
        if not passwd_user:
            return
        if passwd_user.card.islock:
            print('该卡已被锁,请解锁后再使用!')
            self.__Cutdown(3)
            return
        return passwd_user
    def __Cutdown(self, n):
        for i in range(n, 0, -1):
            print(str(i).center(60, '-'), end='\t')
            time.sleep(1)
            print('', end='\r')
