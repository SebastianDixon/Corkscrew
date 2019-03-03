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



def cpu_search_database():
    cpu = input('CPU name: ')
    try:
        with connection.cursor() as cursor:
            sql = "SELECT `GPU` FROM `Leaderboard` WHERE `CPU`= %s"
            cursor.execute(sql, (cpu,))
            for row in cursor:
                print(row['GPU'])
        connection.commit()

    finally:
        connection.close()

def gpu_search_database():
    gpu = input('GPU name: ')
    try:
        with connection.cursor() as cursor:
            sql = "SELECT `CPU` FROM `Leaderboard` WHERE `GPU`= %s"
            cursor.execute(sql, (gpu,))
            for row in cursor:
                print(row['CPU'])
        connection.commit()

    finally:
        connection.close()

def write_database():
    try:
        with connection.cursor() as cursor:
            sql = "INSERT INTO `Leaderboard` (`CPU`,`GPU`,`SCORE`, `FPS`) VALUES (%s, %s,%s, %s)"
            cursor.execute(sql, ('5257U', 'intel', results[1], results[0]))
        connection.commit()

    finally:
        connection.close()


def read_database_prompt():
    pos = int(input('Which Position? :'))
    try:
        with connection.cursor() as cursor:
            sql = "SELECT `CPU`, `GPU`, `SCORE`, `FPS` FROM `Leaderboard` WHERE `POSITION`= %s"
            cursor.execute(sql, (pos, ))
            result = cursor.fetchone()
        print(result)

    finally:
        connection.close()