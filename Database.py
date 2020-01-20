import pymysql
from PyQt5.QtWidgets import *
from bs4 import BeautifulSoup

results = []
recommend_cpu = []
recommend_gpu = []


class Database():

    """
     database class works for both databases for hardware and login.
     insertion and query of rows
    """

    def __init__(self, host, root, password, hardware, charset, cursorclass):

        self.table_columns = []

        self.connection = pymysql.connect(host = host,
                                     user = root,
                                     password = password,
                                     db = hardware,
                                     charset = charset,
                                     cursorclass = cursorclass)

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

    def setTable(self, table):
        self.table_columns = []

        try:
            with self.connection.cursor() as cursor:
                cursor.execute("SHOW columns FROM " + table)
                for dictionary in cursor.fetchall():
                    self.table_columns.append(dictionary['Field'])
        except:
            print("incorrect table name.")

    def insertRow(self):
        print('insert value')

    def registration(self):
        print('register')

    def login(self):
        print('login')


    def pop_name(self):
        text, okPressed = QInputDialog.getText(self, "Component Name", "name:", QLineEdit.Normal, "")
        if okPressed and text != '':
            return text
        elif okPressed and text == '':
            Database.pop_name(self)

    def getCpuDetails(self):
        item = Database.pop_name(self)

        try:
            with self.connection.cursor() as cursor:
                print("Searching for ", item)
                sql = "SELECT" + "`GPU`" + "FROM `" + "`Hardware.Parts`" + "`WHERE`" + "`CPU`" + "` = '" + item + "'"
                cursor.execute(sql)
                for row in cursor.fetchall():
                    recommend_cpu.append(row['GPU'])

            self.connection.commit()

        except pymysql.err.IntegrityError:
            print('Wrong')

    def getGpuDetails(self):
        item = Database.pop_name(self)

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

