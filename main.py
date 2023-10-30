import serial
import time

arduino = serial.Serial(port='COM3', baudrate=115200, timeout=.1)


def write_read(input_command):
    input_command.strip()  # Strip all EOL characters for consistency
    print('Sending: ' + input_command),
    input_command = (bytes(input_command + '\n', 'utf-8'))
    arduino.write(input_command)  # Send g-code block to grbl
    answer = arduino.readline().decode()  # Wait for grbl response with carriage return
    print(' : ' + answer)
    time.sleep(0.05)


def main():
    while True:
        input_command = input("Enter a command: ")  # Taking input from user
        if input_command == "done":
            break
        write_read(input_command)
    arduino.close()


main()
