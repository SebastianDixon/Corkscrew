import pymysql.cursors
from PyQt5.QtWidgets import *
from bs4 import BeautifulSoup
import GUI

connection = pymysql.connect(host='localhost',
                             user='root',
                             password='password',
                             db='Database',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)
results = []
recommend_cpu = []
recommend_gpu = []

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
                recommend_gpu.append(row['GPU'])
                print(row['GPU'])
            gpu_URL()
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
                recommend_cpu.append(row['CPU'])
                print(row['CPU'])
            cpu_URL()
        connection.commit()

    finally:
        connection.close()

def write_database():
    try:
        with connection.cursor() as cursor:
            sql = "INSERT INTO `Leaderboard` (`CPU`,`GPU`,`SCORE`, `FPS`) VALUES (%s, %s,%s, %s)"
            cursor.execute(sql, (GUI.cpu_name(), 'intel', results[1], results[0]))
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

def cpu_URL():
    part1 = 'https://www.amazon.co.uk/s?k='
    part2 = '&ref=nb_sb_noss_2'
    for i in range(0, len(recommend_cpu)):
        url = part1 + recommend_cpu[i] + part2
        print(url)

def gpu_URL():
    part1 = 'https://www.amazon.co.uk/s?k='
    part2 = '&ref=nb_sb_noss_2'
    for i in range(0, len(recommend_gpu)):
        split1 = recommend_gpu[i].split(' ')
        joined = split1[0] + split1[1]
        url = part1 + joined + part2
        print(url)