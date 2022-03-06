import socket
import sys
# ? Import needed libraries.

HOST = socket.gethostname()
PORT = 7002
BUFFER_SIZE = 1024
IP = (HOST, PORT)
# ? Define the ip address and port that will
# ? be used to communicate with the client.


class wheel:
    def __init__(self, speed, direction):
        self.speed = speed
        self.direction = direction
# ? Create a wheel class.
# ? Each wheel object has a velocity.


class rover:
    def __init__(self, wheel_1, wheel_2, wheel_3, wheel_4):
        self.wheel_1 = wheel(0, 'f')
        self.wheel_2 = wheel(0, 'f')
        self.wheel_3 = wheel(0, 'f')
        self.wheel_4 = wheel(0, 'f')
# ? Rover class creates 4 instances of the wheel object
# ? giving all of then an initial direction and magnitude.


curiosity = rover("wheel_1", "wheel_2", "wheel_3", "wheel_4")
# ? Create 1 instance of the rover object, creating 4 wheel objects.

speed = 0
# ? Initial magnitude of all wheels is set to 0.

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    sock.bind(IP)
    sock.listen()
    connect, address = sock.accept()
    with connect:
        # ? listen to any connections on the same port.

        try:
            print('Connected by', address)
            while True:
                bin_data = connect.recv(BUFFER_SIZE)
                if bin_data == b'quit':
                    print("Client disconnecting...")
                    sock.close()
                    sys.exit()
                    # ? If the binary message is `b'quit'` kill
                    # ? the connection and quit the program.

                data = bytes.decode(bin_data).lower().replace(' ', '')
                key = data[0:-1]
                status = data[-1]
                forward = 'f'
                reverse = 'r'
                # ? Convert the message from binary to utf-8 then make
                # ? all characters lowercased and remove spaces. Then
                # ? define some variables using the aforementioned message.

                if status == '1':
                    if key == 'a' or key == 'left':
                        curiosity.wheel_1.direction = reverse
                        curiosity.wheel_2.direction = reverse
                        curiosity.wheel_3.direction = forward
                        curiosity.wheel_4.direction = forward
                    if key == 'w' or key == 'up':
                        curiosity.wheel_1.direction = forward
                        curiosity.wheel_2.direction = forward
                        curiosity.wheel_3.direction = forward
                        curiosity.wheel_4.direction = forward
                    if key == 's' or key == 'down':
                        curiosity.wheel_1.direction = reverse
                        curiosity.wheel_2.direction = reverse
                        curiosity.wheel_3.direction = reverse
                        curiosity.wheel_4.direction = reverse
                    if key == 'd' or key == 'right':
                        curiosity.wheel_1.direction = forward
                        curiosity.wheel_2.direction = forward
                        curiosity.wheel_3.direction = reverse
                        curiosity.wheel_4.direction = reverse
                    # ? If a directional button was pressed make
                    # ? all wheels face in that direction.

                    if key == '0':
                        speed = 0
                    if key == '1':
                        speed = 51
                    if key == '2':
                        speed = 102
                    if key == '3':
                        speed = 153
                    if key == '4':
                        speed = 204
                    if key == '5':
                        speed = 255
                    #! Need to change speed with PWM
                    # ? If a certian numerical button was pressed
                    # ? then set the motors to a certian speed.

                    curiosity.wheel_1.speed = speed
                    curiosity.wheel_2.speed = speed
                    curiosity.wheel_3.speed = speed
                    curiosity.wheel_4.speed = speed
                    # ? set the speed of each wheel object
                    # ? to the chosen speed above.

                    print("[{0}{1}][{2}{3}][{4}{5}][{6}{7}]".format(curiosity.wheel_1.direction, curiosity.wheel_1.speed, curiosity.wheel_2.direction,
                          curiosity.wheel_2.speed, curiosity.wheel_3.direction, curiosity.wheel_3.speed, curiosity.wheel_4.direction, curiosity.wheel_4.speed))
                    # ? Print velocity of each wheel object to the terminal.

                connect.sendall(bin_data)
        except BrokenPipeError:
            print("Terminating...")
