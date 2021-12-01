import socket
import time

SERVER_ADDRESS = ('127.0.0.1', 54322)
BUFFER_SIZE = 1024
FILENAME = "status.txt"
sleepSecond = 60
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

        try:
            with socket.socket() as client_socket:
                print("connecting to server at {}:{}...".format(*SERVER_ADDRESS))
                client_socket.connect(SERVER_ADDRESS)

                print("connected. sending message...")
                msg = data
                client_socket.send(msg.encode())

                print("waiting for response...")
                response = client_socket.recv(BUFFER_SIZE)
                print('server sent back: "{}"'.format(response.decode()))
        except socket.error as error:
            print("Caught exception socket.error : {}".format(error))
            exit(1)
        except ConnectionAbortedError or ConnectionResetError:
            print("problem in the server\nget look if the server off")
            exit(0)

        time.sleep(sleepSecond)
except IndexError or BrokenPipeError as error:
    print("the Error is: {}".format(error))
    exit(1)
except ValueError as valueError:
    print("error in the value --> {}".format(valueError))
    exit(1)
except ConnectionAbortedError or ConnectionResetError:
    print("problem in the server\nget look if the server off")
    exit(0)
except KeyboardInterrupt:
    print("good bay")

