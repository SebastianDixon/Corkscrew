import mysql.connector
from PyQt5.QtWidgets import *
from bs4 import BeautifulSoup
import GUI

cnx = mysql.connector.connect(user='root', password='password',
                              host='localhost',
                              database='hardware')

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


def pop_name(self):
    text, okPressed = QInputDialog.getText(self, "Component Name", "name:", QLineEdit.Normal, "")
    if okPressed and text != '':
        return text
    elif okPressed and text == '':
        pop_name(self)


def cpu_search_database(self):
    item = pop_name(self)
    print(item)
    cursor = cnx.cursor()
    cursor.execute("SELECT GPU FROM hardware.parts WHERE CPU = CPU")
    for row in cursor:
        recommend_cpu.append(row['GPU'])
        print(row['GPU'])
    gpu_URL()

    cursor.close()
    cnx.close()


def gpu_search_database(self):
    item = pop_name(self)
    cursor = cnx.cursor()
    query = ("SELECT CPU FROM hardware.parts WHERE GPU = %s")
    cursor.execute(query, (item,))
    for row in cursor:
        recommend_cpu.append(row['CPU'])
        print(row['CPU'])
    cpu_URL()

    cursor.close()
    cnx.close()


def cpu_URL():
    part1 = 'https://www.amazon.co.uk/s?k='
    part2 = '&ref=nb_sb_noss_2'
    for i in range(0, len(recommend_cpu)):
        try:
            split1 = recommend_cpu[i].split(' ')
            joined = split1[0] + split1[1]
            url = part1 + joined + part
        except:
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