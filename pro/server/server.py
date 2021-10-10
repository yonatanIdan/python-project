import socket
import datetime
import sqlite3


def main():
    # None -> blocking mode (the default)
    # 0 -> immediate mode (must have the data immediately)
    # >0 -> seconds to wait
    socket.setdefaulttimeout(120)
    accept_socket = socket.socket()
    client_list = []

    IP = '127.0.0.1'
    PORT = 54321
    BUFFERSIZE = 16
    accept_socket.bind((IP, PORT))
    DB_FILENAME = "data.sqlite"

    SQL_CREATE_TABLE = """
CREATE TABLE IF NOT EXISTS station_status (
station_id INT,
last_date TEXT,
alarm1 INT,
alarm2 INT,
PRIMARY KEY(station_id) 
);"""
    SQL_INSERT_TABLE = """
INSERT OR REPLACE INTO station_status
VALUES (?, ?, ?, ?)
"""
    # create status table and if not exists make one
    with sqlite3.connect(DB_FILENAME) as conn:
        conn.execute(SQL_CREATE_TABLE)

if __name__ == '__main__':
    main()