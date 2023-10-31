import serial
import time
import math
import datetime

arduino = serial.Serial(port='COM3', baudrate=115200, timeout=.1)
Max_Y = 430
Max_X = 310
Speed = 6000
Total_gcode_lines = 0
last_position_x, last_position_y = 0, 0

# Basic Functions
def initialize():
    global Max_X, Max_Y
    input_command = (input
                     ("Welcome\n "
                      "Please choose a drawing Area ('A3', 'A4', or 'custom')\n "
                      "Remember to align your Paper in portrait or choose a custom area\n:"))
    if input_command == 'A4' or input_command == "a4":
        Max_X = 210
        Max_Y = 295
    if input_command == 'A3' or input_command == "a3":
        Max_X = 295
        Max_Y = 420
    if input_command == 'custom':
        input_command = (input("please input Max_X:"))
        Max_X = int(input_command)
        input_command = (input("please input Max_Y:"))
        Max_Y = int(input_command)

    home()
    time.sleep(2)
    print("Max_X set to " + str(Max_X) + ", " + "Max_Y set to " + str(Max_Y))
    print(" Available Functions: \n\n SquareArt, test, SquareArt2, file\n ")
def main():
    initialize()
    while True:
        input_command = input("Enter a command: ")  # Taking input from user
        if input_command == "done":
            break
        elif input_command == "SquareArt":
            square_art()
        elif input_command == "SquareArt2":
            square_art2()
        elif input_command == "test":
            move_to(Max_X, Max_Y)
        elif input_command == "file":
            read_file()
        else:
            write_read(input_command)
    arduino.close()

# Main helper functions, movement and non-specific-tasks
def write_read(command):
    arduino.write(bytes(command + '\n', 'utf-8'))
    # arduino.write(bytes(input_command, 'utf-8'))
    while True:
        answer = arduino.readline().decode().strip()
        if answer == "":
            break
        print(' : ' + answer)
        time.sleep(0.05)
def home():
    write_read("$H")
def pen_down():
    write_read("m3 s50")
def pen_up():
    write_read("m5")
def stop_pen_noise():
    global arduino
    arduino.close()
    time.sleep(1)
    arduino = serial.Serial(port='COM3', baudrate=115200, timeout=.1)
def move_to(x, y):
    print("move_to(" + str(x) + ", " + str(y) + ")")
    x = int(x)
    y = int(y)
    if x > Max_X or x < 0 or y > Max_Y or y < 0:
        print("Movement outside maximum Border canceled")
        exit()

    to_write = "G1 X" + str(x) + " Y" + str(y) + " F" + str(Speed)
    write_read(to_write)
    time.sleep(calc_time_move_and_update_last_pos(x, y))
    return
def calc_time_move_and_update_last_pos(x, y):
    global last_position_y, last_position_x
    distance = math.sqrt((last_position_x - x) * (last_position_x - x) +
                         (last_position_y - y) * (last_position_y - y))
    last_position_y = y
    last_position_x = x
    time_to_wait = distance / Speed * 62
    return time_to_wait

# specific functions and user-callable tasks
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

    move_to(90,180)
    pen_down()

    for t in range(500):
        angle1 = t * angle_value
        angle2 = t * 93 * angle_value

        move_to(90 + math.sin(angle1) * 70 + math.sin(angle2) * 20,
                90 + math.cos(angle1) * 70 + math.cos(angle2) * 20)
    pen_up()
def read_file():
    current_line = 0
    link = "C:\\Users\\poffe\\Desktop\\Plotter\\Mi_Grbl_Python\\Code\\drawing.gcode"
    mirror_choice = input(
        "Do you want to mirror the result , so it looks 1:1? The gcode extractor\n"
        "from inkscape mirrors the image around the y axis. I can fix that, but \n"
        "you had to select the right canvas size earlier (Y/N): ")

    print("Total estimated Time: " + str(datetime.timedelta(seconds=(int(calc_time_file(link))))))
    input("GO?")
    file = open(link, "r")
    while True:
        line = file.readline().split()
        if line.__len__() > 4:
            if line[2][0] == "X":
                if line[0] == "G00":
                    pen_up()
                else:
                    pen_down()

                # X68.320 --> 68; Y176.898 --> 176
                x = line[2].translate({ord(i): None for i in ".XY;"})[-7:-3]
                y = int(line[3].translate({ord(i): None for i in ".XY;"})[-7:-3])
                if mirror_choice == "Y" or mirror_choice == "y":
                    y = Max_Y-y
                current_line += 1
                print("Progress: " + str(current_line) + "/" + str(Total_gcode_lines))
                move_to(x, y)

        elif line.__len__() == 0:
            file.close()
            break
    pen_up()
    move_to(0, 0)
    stop_pen_noise()
def calc_time_file(link):
    global Total_gcode_lines
    total_time_sec = 0
    file = open("C:\\Users\poffe\Desktop\Plotter\Mi_Grbl_Python\Code\drawing.gcode", "r")
    while True:
        line = file.readline().split()
        if line.__len__() > 4:
            if line[2][0] == "X":
                Total_gcode_lines += 1
                # X68.320 --> 68; Y176.898 --> 176
                x = int(line[2].translate({ord(i): None for i in ".XY;"})[-7:-3])
                y = int(line[3].translate({ord(i): None for i in ".XY;"})[-7:-3])

                total_time_sec += calc_time_move_and_update_last_pos(x, y)

        elif line.__len__() == 0:
            break
    total_time_sec += calc_time_move_and_update_last_pos(0, 0)
    file.close()
    return total_time_sec


main()
