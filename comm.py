# communicate with arduino nano driver board
# to control stepper motors

import serial, time

# Set up commlink
import serial.tools.list_ports
ports = serial.tools.list_ports.comports()

print("available ports:")
for port, desc, hwid in sorted(ports):
    print("{}: {} [{}]".format(port, desc, hwid))

# If there is more than one port, ask user to choose
if len(ports) > 1:
    port = ""#input("select port> ")
    if port == "": port = sorted(ports)[0][0]
else:
    ports = []
    while len(ports) == 0:
        ports = serial.tools.list_ports.comports()
    port = ports[0][0]
print("establishing connection...")
time.sleep(1)

nano = serial.Serial(port, 115200, timeout=0.1)

def send_command(command):
    global nano
    try:
        nano.write(command.encode("utf-8"))
        nano.write(b"\n")
        return True
    except:
        print("command failed")
        return False

def reconnect():
    global nano
    try:
        nano.close()
        nano = serial.Serial(port, 115200, timeout=1)
    except:
        print("reconnection attempt failed")
        return False

if __name__ == "__main__":
    while True:
        command = input("command> ")
        if command == "exit":
            break
        if send_command(command):
            print("command sent")
        else:
            print("command failed")
            if not reconnect():
                break