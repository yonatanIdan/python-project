import socket
import time

IP = '127.0.0.1'
PORT = 54321
SERVER_ADDRESS = (IP, PORT)
FILENAME = "status.txt"
sleepSecond = 10
s = socket.socket()
data = ""

try:
    # connect to the server
    print('connecting to server at {}:{} ...'.format(*SERVER_ADDRESS))
    s.connect(SERVER_ADDRESS)
    print('connected...')
    while True:
        # read file
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

        # send data to server
        try:
            msg = data
            s.send(msg.encode())
            response = s.recv(1024).decode()
            print("{}\nstation {}\nTime: {}".format(*response.split(",")))
        except:
            print("none data receive")
            exit(0)

        # make program sleep for time loop
        time.sleep(sleepSecond)

except BrokenPipeError:
    exit(1)
except KeyboardInterrupt:
    print("your keyboard want to exit ☻☺")
    exit(0)
finally:
    s.close()