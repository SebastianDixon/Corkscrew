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
        salt = os.urandom(32)
        pass_key = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)
        key_string = str(pass_key)

        users = []

        try:
            with self.connection.cursor() as cursor:
                last_row = cursor.execute("SELECT `UserID` FROM Hardware.Login")
                new_row = last_row+1
                print('new row =', new_row)

                update_sql1 = "UPDATE Hardware.Login SET `Username` = %s WHERE `UserID` = %s"
                data1 = (user1, new_row)

                update_sql2 = "UPDATE Hardware.Login SET `PasswordHash` = %s WHERE `UserID` = %s"
                data2 = (key_string, new_row)

                sql = cursor.execute("SELECT `Username` FROM Hardware.Login")
                if sql == user1:
                    print('username taken')
                    return self.reject_user()
                else:
                    cursor.execute("INSERT INTO Hardware.Login(UserID) VALUES(%s)", new_row)
                    cursor.execute(update_sql1, data1)
                    cursor.execute(update_sql2, data2)

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
