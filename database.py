import psycopg2
import os


class ConnectDatabase(object):  # 連結時間 1.27 S
    # connect to database
    # env = os.environ.get("PYTHON_ENV")
    # if (env == "production"):
    DATABASE_URL = os.environ[
        "DATABASE_URL"] = "postgres://qsamrabatiyelo:433fedd48e84326c3db335406302d0af952e43a397e704e1272ec36b27f15d99@ec2-3-230-219-251.compute-1.amazonaws.com:5432/danc0iei9kn9ld"
    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    cur = conn.cursor()

    # else:
    #     conn = psycopg2.connect(
    #         host="localhost",
    #         database="vocabulary",
    #         user="postgres",
    #         password="0000",
    #         port="5432"
    #     )
    # cur = conn.cursor()

    def count_days(self) -> str:  # 計算有幾天
        self.cur.execute("SELECT COUNT(*) FROM information_schema.tables WHERE table_schema = 'public'")
        rows = self.cur.fetchall()

        return "".join("%s" % i for i in rows)

    def review(self, day):  # 複習
        self.cur.execute("SELECT * FROM day{0} ORDER BY id ASC".format(day))
        rows = self.cur.fetchall()

        print(*rows, sep="\n")

    def count_id(self, day: int) -> str:  # 計算有多少ID
        self.cur.execute("SELECT COUNT(id) FROM day{0};".format(day))
        rows = self.cur.fetchall()

        return "".join("%s" % i for i in rows)

    def shuffle_voc(self, day: int, idcountlist: list) -> list:  # 打亂的ID印出單字
        rows = []
        for i in idcountlist:
            self.cur.execute("SELECT * FROM day%s WHERE id = %s", [day, i])
            rows += self.cur.fetchall()
        return rows

    def count_user_id(self) -> str:  # 計算使用者數量
        self.cur.execute('SELECT COUNT(id) FROM private.user')
        rows = self.cur.fetchall()
        return "".join("%s" % i for i in rows)

    def select_user_name(self, name) -> str:  # 選擇使用者名稱
        self.cur.execute("SELECT * FROM private.user WHERE name = %s ORDER BY id ASC", [name])
        rows = self.cur.fetchall()
        # return "".join("{0}".format(i) for i in rows)
        return rows

    def select_user_name_account(self) -> str:  # 選擇使用者名稱和帳號
        self.cur.execute('SELECT id,name,account FROM private.user ORDER BY id ASC')
        rows = self.cur.fetchall()
        # return "".join("{0}".format(i) for i in rows)
        return rows

    def enter_a_p(self, name, account, password):  # 輸入使用者、帳號、密碼
        self.cur.execute(
            'SELECT name,account,password FROM private.user WHERE name = %s AND account = %s AND password = %s',
            [name, account, password])
        rows = self.cur.fetchall()
        # return "".join("{0}".format(i) for i in rows)
        return rows

    def sign_up(self):  # 註冊
        c = ConnectDatabase()
        id = int(c.count_user_id())
        sna = c.select_user_name_account()
        print("------------------------------------------------")
        while True:  # 判斷使用者會不會過
            name = input("創建使用者名稱: ")
            if len(name) < 1:
                print("名稱不能留白")
                continue
            elif len(name) > 10:
                print("名稱過長")
                continue
            else:
                break
        while True:  # 判斷帳號會不會過
            account = input("創建帳號: ")
            if len(account) < 1:
                print("帳號不能留白")
                continue
            elif len(account) > 10:
                print("帳號過長，最多10位數")
                continue
            elif len(account) >= 1 and len(account) <= 10:
                for i in range(id):
                    if name == sna[i][1] and account == sna[i][2]:
                        print("已有此帳號")
                        break
                else:
                    break
        while True:  # 判斷密碼會不會過
            password = input("創建密碼: ")
            verification = input("請輸入驗證碼: ")
            if len(password) < 6:
                print("長度過短，至少6位數")
                continue
            elif len(password) > 10:
                print("長度過長，最多10位數")
                continue
            elif verification != "01010101":
                print("驗證碼錯誤!")
                continue
            else:
                self.cur.execute('INSERT INTO private.user (id,name,account,password) VALUES (%s,%s,%s,%s)',
                                 (int(id) + 1, name, account, password))
                print("註冊成功!")
                print("------------------------------------------------")
                break
        self.conn.commit()

    def sign_in(self):  # 登入
        c = ConnectDatabase()
        id = int(c.count_user_id())
        while True:  # 判斷是否有此使用者
            try:
                name = input("輸入使用者名稱: ")
                sn = c.select_user_name(name)
                for i in range(id):
                    if name == sn[i][1]:
                        break
            except IndexError:
                print("沒有此使用者")
                continue
            try:  # 判斷是否有這些帳號密碼
                account = input("輸入帳號: ")
                password = input("輸入密碼: ")
                eap = c.enter_a_p(name, account, password)
                for i in range(id):
                    if name == eap[i][0] and account == eap[i][1] and password == eap[i][2]:
                        print("登入成功!")
                        print("------------------------------------------------")
                        break
                    else:
                        print("名稱或帳號或密碼有錯，請重新輸入")
                        continue
                else:
                    break
            except IndexError:
                print("名稱或帳號或密碼有錯，請重新輸入")
                continue
            else:
                break

# c = ConnectDatabase()
# c.count_user_id()
# c.select_name_account()
