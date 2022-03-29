import mysql.connector
from mysql.connector import Error

host = "localhost"
port = 3306
username = "isiblog"
password = "isiblog"
database = "dbisiblog"

def mysql_connect():
    try:
        connection = mysql.connector.connect(host=host, port=port, user=username, password=password, database=database)
        
        if connection.is_connected():
            is_connected = True
            db_info = connection.get_server_info()
            print("Connected to MySQL Server version :", db_info)
            cursor = connection.cursor()
            cursor.execute("select database();")
            record = cursor.fetchone()
            print("You're connected to database :", record)
            cursor.close()
            return connection
    except Error as e:
        print("Error while connecting to MySQL", e)
        return None

def transform_record_to_dict(records) -> dict:
    record_dict = {}
    for record in records:
        record_dict[record[0]] = {
            "id": record[0],
            "auteur": record[1],
            "titre": record[2],
            "contenu": record[3],
            "dateCreation": record[4]
        }
    return record_dict

def get_all_comments(connection):
    if connection != None and connection.is_connected():
        query = f"SELECT * FROM {database}.comments ORDER BY dateCreation DESC"
        cursor = connection.cursor()
        cursor.execute(query)
        result = cursor.fetchall()
        cursor.close()
        return transform_record_to_dict(result)

def get_last_id(connection) -> int:
    if connection != None and connection.is_connected():
        query = f"SELECT MAX(id) FROM {database}.comments"
        cursor = connection.cursor()
        cursor.execute(query)
        result = cursor.fetchone()[0]
        cursor.close()
        if result == None:
            return 0
        else:
            return result+1

def delete_comment(connection, id: int) -> bool:
    if connection != None and connection.is_connected():
        query = f"DELETE FROM {database}.comments WHERE id = {id}"
        cursor = connection.cursor()
        cursor.execute(query)
        rowcount = cursor.rowcount
        cursor.close()
        connection.commit()
        return rowcount > 0

def insert_comment(connection, comment: dict) -> bool:
    if connection != None and connection.is_connected():
        try:
            id = comment["id"]
            auteur = comment["auteur"].replace("'", "''")
            titre = comment["titre"].replace("'", "''")
            contenu = comment["contenu"].replace("'", "''")
            dateCreation = comment["dateCreation"]
            query = f"INSERT INTO {database}.comments VALUES ({id}, '{auteur}', '{titre}', '{contenu}', '{dateCreation}')"
            cursor = connection.cursor()
            cursor.execute(query)
            rowcount = cursor.rowcount
            cursor.close()
            connection.commit()
            return rowcount > 0
        except Error as e:
            return False





