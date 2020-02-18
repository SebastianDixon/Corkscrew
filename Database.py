import pymysql.cursors
from PyQt5.QtWidgets import *
from bs4 import BeautifulSoup
import os
import hashlib
import GUI
import cryptography

results = []
recommend_cpu = []
recommend_gpu = []


class Database():

    def __init__(self):
        self.connection = pymysql.connect(host='localhost',
                                          user='root',
                                          password='password',
                                          db='Hardware',
                                          charset='utf8mb4',
                                          cursorclass= pymysql.cursors.DictCursor)

    def openFile(self):
        options = QFileDialog.Options()

        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self, "QFileDialog.getOpenFileName()", "",
                                                  "All Files (*);;Python Files (*.py)", options=options)
        if fileName:
            file = open(fileName)
            data = file.read()
            soup = BeautifulSoup(data, "lxml")
            for item in soup.find_all('strong'):
                results.append(float(item.text))
        print('Score =', results[1])
        print('Fps =', results[0])

    def registration(self, user1, password):
        Database.salt_hash(self, password)
        users = []

        try:
            with self.connection.cursor() as cursor:
                total = cursor.execute("SELECT COUNT(*) FROM Hardware.Login")
                total_str = str(total + 1)
                sql = "SELECT `Username` FROM Hardware.Login WHERE `UserID` = %s"
                for i in range(total+1):
                    str_i = str(i)
                    sql = cursor.execute(sql, str_i)
                    if sql == user1:
                        users.append(sql)
                existingusercount = len(users)

                if existingusercount == 1:
                    print('username taken')
                    return self.reject_user()
                else:
                    cursor.execute("INSERT INTO Hardware.Login(Username) VALUES(%s)", user1)
                    cursor.execute("INSERT INTO Hardware.Login(PasswordHash) VALUES(%s)", password)
                    cursor.execute("INSERT INTO Hardware.Login(UserID) VALUES(%s)", total_str)
            self.connection.commit()

        except pymysql.err.IntegrityError:
            print('Wrong')

    def reject_user(self):
        gui = GUI.Window()
        return gui.loginWindow()

    def login(self, user2, password):
        print('login')

    def salt_hash(self, plain_word):
        salt = os.urandom(32)
        pass_key = hashlib.pbkdf2_hmac('sha256', plain_word.encode('utf-8'), salt, 100000)
        print(pass_key)
        return pass_key

    def pop_name(self):
        text, okPressed = QInputDialog.getText(self, "Component Name", "name:", QLineEdit.Normal, "")
        if okPressed and text != '':
            return text
        elif okPressed and text == '':
            self.pop_name()

    def getCpuDetails(self):
        item = self.pop_name()

        try:
            with self.connection.cursor() as cursor:
                print("Searching for ", item)
                sql = "SELECT `GPU` FROM Hardware.Parts WHERE `CPU` = %s"
                cursor.execute(sql, item)
                for row in cursor.fetchall():
                    recommend_cpu.append(row['GPU'])

            self.connection.commit()

        except pymysql.err.IntegrityError:
            print('Wrong')

    def getGpuDetails(self):
        item = self.pop_name()

        try:
            with self.connection.cursor() as cursor:
                print("Searching for ", item)
                sql = "SELECT" + "`CPU`" + "FROM `" + "`Hardware.Parts`" + "`WHERE`" + "`GPU`" + "` = '" + item + "'"
                cursor.execute(sql)
                for row in cursor.fetchall():
                    recommend_gpu.append(row['CPU'])

            self.connection.commit()

        except pymysql.err.IntegrityError:
            print('Wrong')

    def cpu_URL(self):
        part1 = 'https://www.amazon.co.uk/s?k='
        part2 = '&ref=nb_sb_noss_2'
        for i in range(0, len(recommend_cpu)):
            try:
                split1 = recommend_cpu[i].split(' ')
                joined = split1[0] + split1[1]
                url = part1 + joined + part2
            except:
                url = part1 + recommend_cpu[i] + part2
            print(url)

    def gpu_URL(self):
        part1 = 'https://www.amazon.co.uk/s?k='
        part2 = '&ref=nb_sb_noss_2'
        for i in range(0, len(recommend_gpu)):
            split1 = recommend_gpu[i].split(' ')
            joined = split1[0] + split1[1]
            url = part1 + joined + part2
            print(url)
