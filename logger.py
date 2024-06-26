import mysql.connector

password_for_log = {'host': 'mysql.itcareerhub.de',
                    'user': 'ich1',
                    'password': 'ich1_password_ilovedbs',
                    'database': 'project_220424ptm_Vasiliy_Gubenkov'}

def write_log(x):
    connection = mysql.connector.connect(**password_for_log)
    cursor = connection.cursor()
    cursor.execute(f"insert into log (content) values ('{x}')")
    connection.commit()
    cursor.close()
    connection.close()



