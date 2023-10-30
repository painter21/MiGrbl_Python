import serial
import time

arduino = serial.Serial(port='COM3', baudrate=115200, timeout=.1)


def write_read(x):
    arduino.write(x.encode())
    print(x.encode())
    time.sleep(0.05)
    data = arduino.readline()
    return data


def main():
    while True:
        input_command = input("Enter a command: ")  # Taking input from user
        if input_command == "done":
            break
        value = write_read(input_command)
        print(value)  # printing the value
    arduino.close()


main()
