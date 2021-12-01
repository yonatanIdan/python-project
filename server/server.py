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
    PORT = 54322
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

    try:
        accept_socket.listen(BUFFERSIZE)
        while True:
            # accept a new client if exists:
            try:
                c, a = accept_socket.accept()
            except (socket.timeout, BlockingIOError) as error:
                print("Error: {}".format(error))
                exit(0)
            else:
                print("new client connected:", a)
                client_list.append(c)

            # for each client do
            # for c in client_list.copy():

                try:
                    data = c.recv(1024)
                except (socket.timeout, BlockingIOError) as error:
                    print("error: {}".format(error))
                    exit(0)
                except OSError:
                    print("client {}:{} crashed".format(*c.getpeername()))
                    client_list.remove(c)
                else:
                    # empty data == server closed
                    if len(data) == 0:
                        print("client {}:{} closed. Don't have data".format(*c.getpeername()))
                        client_list.remove(c)

                    # if client actually send something
                    else:
                        station, A1, A2 = data.decode().split(" ")
                        # print the receive data => print(station, int(A1), int(A2))
                        # timestamp for the database
                        timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')

                        # write in database the data from the client
                        try:
                            with sqlite3.connect(DB_FILENAME) as conn:
                                conn.execute(SQL_INSERT_TABLE, (int(station), timestamp, int(A1), int(A2)))
                                print("added successfully\nStation:{} A1:{} A2:{} Time:{}".format(station, A1, A2, timestamp))
                        except ValueError as valueError:
                            print("error in the value --> {}".format(valueError))

                        try:
                            print("{}:{} -> {}\nTime: {}".format(*c.getpeername(), [station, int(A1), int(A2)], timestamp))
                            response = compute_response(data)
                            print("response -> {}".format(response))
                            string = "{},{},{}".format(response, station, str(timestamp))
                            c.send(string.encode())
                        except OSError:
                            print("client {}:{} crashed".format(*c.getpeername()))

    except KeyboardInterrupt:
        print("the server was closed")
        exit(0)
    finally:
        for c in client_list:
            c.close()
        accept_socket.close()


def compute_response(data):

    try:
        message = data.decode().split(" ")
    except UnicodeDecodeError:
        response = 'error could not decode (accepts only UTF8).'
    else:
        if message[1] == '0' and message[2] == '0':
            response = 'the station {} ID is safe!'.format(message[0])
        elif message[1] == '1' and message[2] == '1':
            response = 'the station {} ID is in danger! alarm 1 and 2 is on! '.format(message[0])
        elif message[1] == '0':
            response = 'the station {} ID have problem in alarm 1'.format(message[0])
        elif message[2] == '0':
            response = 'the station {} ID have problem in alarm 2'.format(message[0])
        else:
            response = 'I did not understand that {}'.format(message[1])
    return response.encode()


if __name__ == '__main__':
    main()
