from pynput import keyboard
import socket
import sys
# ? Import needed libraries.

HOST = '192.168.2.69'
PORT = 7002
BUFFER_SIZE = 1024
IP = (HOST, PORT)
# ? define the ip address and port that will
# ? be used to communicate with the server.


def send_data(key, status):
    key_status = key + ' ' + str(status)
    sock.send(bytes(key_status, 'utf-8'))
    print(key_status)
# ? Take the pressed/released button and tell the
# ? server (by converting the message to a binary
# ? value) that button was pressed/released.


def button_check(key, status):
    char_keys = ['a', 'w', 's', 'd', '0', '1', '2', '3', '4', '5']
    # ? Array of potential buttons.

    for i in range(len(char_keys)):
        try:
            if key.char == char_keys[i]:
                print(key.char)
                send_data(key.char, status)
    # ? Iterate though the array until the button that  was
    # ? pressed/released is an entry in the array, if it is,
    # ? tell the server that button was pressed/released.

        except AttributeError:
            arrow_keys = [key.left, key.up, key.down, key.right]
            for j in arrow_keys:
                if(key == key.esc):
                    print("Disconnecting...")
                    sock.send(b'quit')
                    sock.close()
                    sys.exit()
                elif key == j:
                    print(str(j)[4:])
                    send_data(str(j)[4:], status)
        # ? If the char of the button wasn't found then its probably
        # ? a special key, if its one of the arrow keys tell the
        # ? server that the button was pressed/released. If the
        # ? escape button was pressed/released then tell the server
        # ? to quit and then quit the program.

            break


def on_press(key):
    status = 1
    button_check(key, status)


def on_release(key):
    status = 0
    button_check(key, status)
# ? If status is 1 then the button is pressed
# ? if status is 0 then the button is released.


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    sock.connect(IP)
    sock.sendall(b'Connected...')
    data = sock.recv(BUFFER_SIZE)
# ? Open a socket and connect to the server using the defined ip and port.

    with keyboard.Listener(
            on_press=on_press,
            on_release=on_release
    ) as listener:
        listener.join()
    # ? Listen to when a button is pressed/released.
