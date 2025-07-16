import tkinter as tk
from pyModbusTCP.client import ModbusClient

# Modbus connect
client = ModbusClient(host="127.0.0.1", port=12345, auto_open=True)

joint1_angle = 0
joint2_angle = 0

# Writing to server
def update_server():
    client.write_multiple_registers(0, [joint1_angle, joint2_angle])
    update_labels()
    root.title(f"Joint1: {joint1_angle}°, Joint2: {joint2_angle}°")

def update_labels():
    label_joint1.config(text=f"Joint 1: {joint1_angle}°")
    label_joint2.config(text=f"Joint 2: {joint2_angle}°")

# Control functions
def increase_joint1(event=None):
    global joint1_angle
    if joint1_angle < 180:
        joint1_angle += 5
        update_server()

def decrease_joint1(event=None):
    global joint1_angle
    if joint1_angle > 0:
        joint1_angle -= 5
        update_server()

def increase_joint2(event=None):
    global joint2_angle
    if joint2_angle < 180:
        joint2_angle += 5
        update_server()

def decrease_joint2(event=None):
    global joint2_angle
    if joint2_angle > 0:
        joint2_angle -= 5
        update_server()

# GUI
root = tk.Tk()
root.title("Robot Arm Control Panel")
root.geometry("300x200")

label_joint1 = tk.Label(root, text="Joint 1: 0°", font=("Arial", 14))
label_joint1.pack(pady=5)

frame1 = tk.Frame(root)
frame1.pack()
tk.Button(frame1, text="−", width=5, command=decrease_joint1).pack(side=tk.LEFT, padx=10)
tk.Button(frame1, text="+", width=5, command=increase_joint1).pack(side=tk.RIGHT, padx=10)

label_joint2 = tk.Label(root, text="Joint 2: 0°", font=("Arial", 14))
label_joint2.pack(pady=5)

frame2 = tk.Frame(root)
frame2.pack()
tk.Button(frame2, text="−", width=5, command=decrease_joint2).pack(side=tk.LEFT, padx=10)
tk.Button(frame2, text="+", width=5, command=increase_joint2).pack(side=tk.RIGHT, padx=10)

# Keyboard control
root.bind("<Left>", decrease_joint1)
root.bind("<Right>", increase_joint1)
root.bind("<Down>", decrease_joint2)
root.bind("<Up>", increase_joint2)

update_server()
root.mainloop()