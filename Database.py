import pymysql.cursors
# Connect to the database
connection = pymysql.connect(host='localhost',
                             user='root',
                             password='password',
                             db='Database',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

def input_database():
    try:
        with connection.cursor() as cursor:
            sql = "INSERT INTO `Leaderboard` (`POSITION`,`SCORE`, `FPS`) VALUES (%s, %s, %s)"
            cursor.execute(sql, ('101','999', '911'))
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