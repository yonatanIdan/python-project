import socket
import time

SERVER_ADDRESS = ('127.0.0.1', 54322)
BUFFER_SIZE = 1024
FILENAME = "status.txt"
sleepSecond = 10
try:

    while True:
        try:
            with open(FILENAME) as file:
                ID = int(file.readline(16)[:-1])
                ALARM1 = int(file.readline(2)[:-1])
                ALARM2 = int(file.readline(2))
            # check sense in Alarms
            if (ALARM1 != 0) & (ALARM1 != 1):
                print("The alarm 1 condition does not make sense --> [ALARM1 = {}]".format(ALARM1))
                break
            if (ALARM2 != 0) & (ALARM2 != 1):
                print("The alarm 2 condition does not make sense --> [ALARM2 = {}]".format(ALARM2))
                break
            data = str(ID) + " " + str(ALARM1) + " " + str(ALARM2)
        except FileNotFoundError:
            print("Something went wrong when reading the file {}".format(FILENAME))
            break

        # print data station from file
        print("---------------------------")
        print("""
    Station ID:     {}
    Alarm 1 status: {:1}
    Alarm 2 status: {:1}\n""".format(ID, ALARM1, ALARM2))

        print("---------------------------")


        with socket.socket() as client_socket:
            print("connecting to server at {}:{}...".format(*SERVER_ADDRESS))
            client_socket.connect(SERVER_ADDRESS)

            print("connected. sending message...")
            msg = data
            client_socket.send(msg.encode())

            response = client_socket.recv(BUFFER_SIZE)
            print('server sent back: "{}"'.format(response.decode()))

        time.sleep(sleepSecond)
except KeyboardInterrupt:
    print("good bay! ")