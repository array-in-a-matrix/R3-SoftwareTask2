# R3 Software Task 2
Demo video located in `./src/demo.mp4` or you can watch it online [here](https://drive.google.com/file/d/1WdfjwOwl6IZ-8ncvbbLWbhZIyo85mqj6/view?usp=sharing).

## Transmission Control Protocol (TCP)
Before setting up any connection between the client script `input.py` and server script `output.py` they need to agree on which port to use. The server script is executed first so it can start listening on the defined port. Then the client script is executed, which then it will connect to the server and start sending data.

### Client:

```python
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    sock.connect(IP)
    sock.sendall(b'Connected...')
    data = sock.recv(BUFFER_SIZE)
```

### Server:

```python
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    sock.bind(IP)
    sock.listen()
    connect, address = sock.accept()
    with connect:
```

<br>

## Button Input
For controls, [pynput](https://pypi.org/project/pynput/) was used due to prior experience with it. The client script listens for any key presses:

```python
with keyboard.Listener(
        on_press=on_press,
        on_release=on_release
) as listener:
    listener.join()
```

If any of the buttons in the array `char_keys` or the arrow keys is pressed or released the client script sends that to the server as a binary data over TCP.

```python
char_keys = ['a', 'w', 's', 'd', '0', '1', '2', '3', '4', '5']
...
arrow_keys = [key.left, key.up, key.down, key.right]
```

 The character keyboard buttons `a`, `w`, `s`, `d` and the arrow keys control the direction of the rover. The numbers `0` through `5` control the speed of the motors. The escape key `Esc` is reserved to quit both client and server scripts. Each button is  usually  accompanied by a `status` variable. The `status` variable is a boolean value which is set to `1` when the button is pressed and `0` when the button is released.

<br>

## Server Interpretation
Upon execution, the server script defines the port and ip needed for a TCP connection. Then 2 classes are created, `wheel` and `rover` classes. When a `rover` object is created it creates 4 `wheel` objects. Each wheel object contains 2 attributes, `speed` and `direction` (a velocity).

```python
class wheel:
    def __init__(self, speed, direction):
        self.speed = speed
        self.direction = direction

class rover:
    def __init__(self, wheel_1, wheel_2, wheel_3, wheel_4):
        self.wheel_1 = wheel(0, 'f')
        self.wheel_2 = wheel(0, 'f')
        self.wheel_3 = wheel(0, 'f')
        self.wheel_4 = wheel(0, 'f')
```

After a successful connection has been made, the server listens to any keys pressed or released. The client script filters out any keys that are not used. The server only gets button inputs that control the rover. The server only takes action if the buttons were pressed down not if they where released. 

### Direction
Pressing either the `left` arrow key or `a` will set the direction of the first and second `wheel` objects to reverse and the third and forth `wheel` objects to forward. If the motors were given a non-zero speed the rover should start rotating counter-clockwise (assuming the code controls a physical rover).

```python
if key == 'a' or key == 'left':
    curiosity.wheel_1.direction = reverse
    curiosity.wheel_2.direction = reverse
    curiosity.wheel_3.direction = forward
    curiosity.wheel_4.direction = forward
```

 The same process is used when the `right` arrow key or `d` are pressed, however the directions are inverted. Pressing the `up` arrow key or `w` changes the direction of all `wheel` objects to forward. Again the same process is done for the `down` arrow key or `s` button but the direction is backwards. 

```python
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
```

### Speed
The speed of the rover is controlled by pressing any of the numerical keys from `0` to `5` (`5` being the maximum speed and `0` being off). I could not figure how to implement a Pulse Width Modulation (PWM) to control the speed yet.

```python
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
```

After a new `speed` as been set, all the `wheel` objects `speed` value change to that new `speed`.

```python
curiosity.wheel_1.speed = speed
curiosity.wheel_2.speed = speed
curiosity.wheel_3.speed = speed
curiosity.wheel_4.speed = speed
```

Finally, after the `rover` object acquires the `speed` and `direction` of all of its children `wheel` objects, it prints it to the terminal.

```python
print("[{0}{1}][{2}{3}][{4}{5}][{6}{7}]".format(curiosity.wheel_1.direction, curiosity.wheel_1.speed, curiosity.wheel_2.direction,
                          curiosity.wheel_2.speed, curiosity.wheel_3.direction, curiosity.wheel_3.speed, curiosity.wheel_4.direction, curiosity.wheel_4.speed))
```

<br>

## Reflection
I have never directly programmed something that deals with a TCP connection and I thought it would be more difficult. There are some parts of the code relating to the TCP connection that I don't fully understand though. The code has a lot of room for improvements and can be shrunk down to a significantly smaller size. At the beginning, I thought of using both button presses and releases to control the rover but then  just made the code work on only button presses, making a few parts of the program obsolete (like the `on_release` function and all the code that uses the `status` variable). I had difficulty implementing PWM into the code, I don't know how to start.
