import serial
import time
import math

arduino = serial.Serial(port='COM3', baudrate=115200, timeout=.1)
Max_Y = 430
Max_X = 310
Speed = 6000
last_position_x, last_position_y = 0, 0


def initialize():
    global Max_X, Max_Y
    home()
    input_command = (input
                     ("Welcome\n "
                      "Please choose a drawing Area ('A3', 'A4', or 'custom')\n "
                      "Remember to align your Paper in portrait or choose a custom area\n:"))
    if input_command == 'A4':
        Max_X = 190
        Max_Y = 270
    if input_command == 'A3':
        Max_X = 270
        Max_Y = 380
    if input_command == 'custom':
        input_command = (input("please input Max_X:"))
        Max_X = int(input_command)
        input_command = (input("please input Max_Y:"))
        Max_Y = int(input_command)

    print("Max_X set to " + str(Max_X) + ", " + "Max_Y set to " + str(Max_Y))
    print(" Available Functions: \n\n SquareArt, test, SquareArt2\n ")
    write_read("$X")


def write_read(command):
    arduino.write(bytes(command + '\n', 'utf-8'))
    # arduino.write(bytes(input_command, 'utf-8'))
    while True:
        answer = arduino.readline().decode().strip()
        if answer == "":
            break
        print(' : ' + answer)
        time.sleep(0.05)


def main():
    initialize()
    while True:
        input_command = input("Enter a command: ")  # Taking input from user
        if input_command == "done":
            break
        elif input_command == "SquareArt":
            square_art()
        elif input_command == "test":
            move_to(Max_X, Max_Y)
        else:
            write_read(input_command)
    arduino.close()


def home():
    write_read("$H")


def pen_down():
    write_read("m3 s50")


def pen_up():
    write_read("m5")


def move_to(x, y):
    int(x), int(y)
    if x > Max_X or y > Max_Y:
        print("Movement outside maximum Border canceled")
        exit()

    to_write = "G1 X" + str(x) + " Y" + str(y) + " F" + str(Speed)
    print(to_write)
    distance = math.sqrt((last_position_x - x) * (last_position_x - x) +
                         (last_position_y - y) * (last_position_y - y))
    time_to_wait = distance / Speed * 61
    print(time_to_wait)
    write_read(to_write)
    time.sleep(time_to_wait)
    return


def square_art():
    for i in range(31):
        pen_down()
        move_to(0 + 4 * i, 50 + 4 * i)
        move_to(50 + 1 + 4 * i, 50 + 1 + 4 * i)
        move_to(50 + 2 + 4 * i, 0 + 2 + 4 * i)
        move_to(0 + 3 + 4 * i, 0 + 3 + 4 * i)
    pen_up()
    move_to(0, 0)


def square_art2():
    angle_value = 3.14 / 180
    for t in range(200):
        angle1 = t * angle_value
        angle2 = t * 93 * angle_value

        move_to(math.sin(angle1) * 70 + math.sin(angle2) * 20,
                math.cos(angle1) * 70 + math.cos(angle2) * 20)

main()
