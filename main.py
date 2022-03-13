from database import ConnectDatabase
import random
from typing import List
import os
import time


class BeforeExam(ConnectDatabase):
    def __init__(self):
        super(BeforeExam, self).__init__()
        self.c = ConnectDatabase()

    def shuffle(self, day: int) -> List[int]:  # 打亂ID
        idcount = self.c.count_id(day)
        idcountlist = [i for i in range(1, int(idcount) + 1)]
        random.shuffle(idcountlist)
        return idcountlist

    def choose_in_up(self):  #選擇註冊或登入
        choose = 0
        c = ConnectDatabase()
        while True:
            try:
                choose = int(input("註冊 1 , 登入 2\n請輸入: "))
            except ValueError:
                print("輸入錯誤，請重新輸入")
                continue
            if choose == 1:
                c.sign_up()
                continue
            elif choose == 2:
                c.sign_in()
                break
            else:
                print("輸入錯誤數字，請重新輸入")
                continue
    def choose_model(self) -> int:  # 選擇模式
        choose = 0
        i = InExam()
        while True:
            try:
                choose = int(input("考試輸入 1 , 複習輸入 2\n請輸入: "))
            except ValueError:
                print("輸入錯誤，請重新輸入")
                continue

            if choose == 1:
                print("目前共有: {0}天".format(self.c.count_days()))
                day = int(input("請輸入要考第幾天: "))
                print("載入中...")
                i.exam(day)
                break
            elif choose == 2:
                print("目前共有: {0}天".format(self.c.count_days()))
                day = int(input("請輸入複習第幾天: "))
                if day <= int(self.c.count_days()):
                    self.c.review(day)
                    os.system("pause")
                    continue
                else:
                    print("輸入錯誤天數，請重新輸入")
                    continue
            else:
                print("輸入錯誤數字，請重新輸入")
                continue
        return day


class InExam(object):
    def __init__(self):
        super(InExam, self).__init__()
        self.c = ConnectDatabase()
        self.b = BeforeExam()

    def listalphabet(self) -> list:
        return list(map(chr, range(97, 101)))

    def exam(self, day: int, tcount: int = 0):  # 考試
        wronglist = []
        anslist = []
        alphabet = InExam.listalphabet(self)
        listlen = int(self.c.count_id(day))
        # start = time.time()
        vocabulary = self.c.shuffle_voc(day, self.b.shuffle(day)) #要優化
        # end = time.time()
        # print(end - start)
        for i in range(listlen):
            print("{0}.".format(i + 1), vocabulary[i][1:3])  # 題目 [1:3]

            anslist.append(vocabulary[i])  # 製作四個答案
            while len(anslist) < 4:
                rcv = random.choice(vocabulary)
                if rcv != vocabulary[i]:
                    if rcv not in anslist:
                        anslist.append(rcv)
            random.shuffle(anslist)
            for j in range(4):
                answer = "".join(anslist[j][3:4])
                print("{0}.".format(alphabet[j]), answer, end="\n")

            ans = input("答案: ")  # 判斷答案是否正確
            if ans == vocabulary[i][3]:
                print("答對")
                anslist.clear()
                tcount += 1
            else:
                print("答錯")
                print("正確答案:", vocabulary[i][3])
                anslist.clear()
                wronglist.append(vocabulary[i][1:4])
        print("答題數:", tcount, "/", listlen)  # 考試結果
        print("錯誤題目:")
        for i in range(len(wronglist)):
            print("{0}.".format(i + 1), wronglist[i], end="\n")
        os.system("pause")
        self.b.choose_model()


def main():
    b = BeforeExam()
    c = ConnectDatabase()
    print("英文單字練習程式 v3.0 作者: 黃致瑋", end="\n")
    print("此程式為簡答題，請輸入選項後的文字，連標點符號都不能少!!", end="\n")
    print("------------------------------------------------")
    b.choose_in_up()
    b.choose_model()


if __name__ == "__main__":
    main()
