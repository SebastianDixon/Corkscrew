import pymysql.cursors
from PyQt5.QtWidgets import *
from bs4 import BeautifulSoup


connection = pymysql.connect(host='localhost',
                             user='root',
                             password='password',
                             db='Database',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)
results = []

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

def write_database():
    try:
        with connection.cursor() as cursor:
            sql = "INSERT INTO `Leaderboard` (`POSITION`,`SCORE`, `FPS`) VALUES (%s, %s, %s)"
            cursor.execute(sql, ('101', results[1], results[0]))
        connection.commit()

    finally:
        connection.close()

def read_database():
    try:
        with connection.cursor() as cursor:
            sql = "SELECT `SCORE`, `FPS` FROM `Leaderboard` WHERE `POSITION`= %s"
            cursor.execute(sql, (1,))
            result = cursor.fetchone()
        print(result)

    finally:
        connection.close()

read_database()