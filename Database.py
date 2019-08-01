import pymysql.cursors
from PyQt5.QtWidgets import *
from bs4 import BeautifulSoup
import GUI

connection = pymysql.connect(host='sql2.freemysqlhosting.net',
                             user='sql2300540',
                             password='wZ6!dU7!',
                             db='sql2300540',
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


def name_check():
    model = GUI.cpu_name.model()
    with connection.cursor() as cursor:
        sql = "SELECT COUNT(*) FROM `leaderboardtable`"
        cursor.execute(sql, )
        index = cursor.fetchone()

    if GUI.bottle == 'CPU':
        for i in range(index[0]):
            sql = "SELECT ALL FROM `leaderboardtable` WHERE 'CPU' = {}".format(index)
            if sql == model:
                try:
                    with connection.cursor() as cursor:
                        sql = "SELECT `GPU` FROM `leaderboardtable` WHERE `CPU`= %s"
                        cursor.execute(sql, (model,))
                        for row in cursor:
                            recommend_gpu.append(row['GPU'])
                            print(row['GPU'])
                        gpu_URL()
                    connection.commit()

                finally:
                    connection.close()
            else:
                print('cpu not found')

    else:
        for i in range(index[0]):
            sql = "SELECT ALL FROM `leaderboardtable` WHERE 'GPU' = {}".format(index)
            if sql == model:
                try:
                    with connection.cursor() as cursor:
                        sql = "SELECT `CPU` FROM `leaderboardtable` WHERE `GPU`= %s"
                        cursor.execute(sql, (model,))
                        for row in cursor:
                            recommend_gpu.append(row['CPU'])
                            print(row['CPU'])
                        cpu_URL()
                    connection.commit()

                finally:
                    connection.close()
            else:
                print('gpu not found')


def cpu_search_database():
    cpu = input('CPU name: ')
    try:
        with connection.cursor() as cursor:
            sql = "SELECT `GPU` FROM `leaderboardtable` WHERE `CPU`= %s"
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
            sql = "SELECT `CPU` FROM `leaderboardtable` WHERE `GPU`= %s"
            cursor.execute(sql, (gpu,))
            for row in cursor:
                recommend_cpu.append(row['CPU'])
                print(row['CPU'])
            cpu_URL()
        connection.commit()

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