import pymysql.cursors
from PyQt5.QtWidgets import *
from bs4 import BeautifulSoup
import GUI

connection = pymysql.connect(host='localhost',
                             user='root',
                             password='password',
                             db='Hardware',
                             charset='utf8mb4',
                             autocommit=True,
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
    print('Fps =', results)


def test_item():
    if GUI.bottle == 'cpu':
        choice = int(input('Test? (1/0)'))
        if choice == 1:
            itemName = input('GPU name: ')
        else:
            itemName = GUI.gpu_name().model
    else:
        choice = int(input('Test? (1/0)'))
        if choice == 1:
            itemName = input('CPU name: ')
        else:
            itemName = GUI.cpu_name().model
    print(itemName)

"""
def cpu_search_database():
    itemName = input('CPU name: ')
    try:
        with connection.cursor() as cursor:
            sql = "SELECT 'GPU' FROM 'Parts' WHERE 'CPU' = %s"
            cursor.execute(sql, (itemName, ))
            result = cursor.fetchone()
            print(result)
    finally:
        connection.close()
"""


def cpu_search_database():
    cpu = input('CPU name: ')
    try:
        with connection.cursor() as cursor:
            sql = "SELECT `GPU` FROM `Hardware`.`Parts` WHERE `CPU`= %s"
            cursor.execute(sql, (cpu,))
            for row in cursor:
                recommend_gpu.append(row['GPU'])
                print(row['GPU'])
            gpu_URL()
    finally:
        connection.close()


def gpu_search_database():
     gpu = input('GPU name: ')
     try:
        with connection.cursor() as cursor:
            sql = "SELECT `CPU` FROM `Hardware`.`Parts` WHERE `GPU`= %s"
            cursor.execute(sql, (gpu,))
            for row in cursor:
                recommend_cpu.append(row['CPU'])
                print(row['CPU'])
            cpu_URL()
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
