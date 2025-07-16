from pyModbusTCP.server import ModbusServer
from vpython import box, cylinder, vector, rate
import threading
import time
from math import sin, cos

# VPython scene
base = box(pos=vector(0, 0, 0), size=vector(1, 0.1, 1), color=vector(0.5, 0.5, 0.5))
joint1 = cylinder(pos=vector(0, 0.05, 0), axis=vector(1, 0, 0), radius=0.05, length=1, color=vector(0.2, 0.6, 0.8))
joint2 = cylinder(pos=joint1.pos + joint1.axis, axis=vector(1, 0, 0), radius=0.04, length=1, color=vector(0.8, 0.4, 0.2))


server = ModbusServer("127.0.0.1", port=12345, no_block=True)

def start_modbus_server():
    print("Starting Modbus Server...")
    server.start()


def update_robot_arm():
    prev_j1, prev_j2 = 0, 0
    while True:
        rate(20)

        regs = server.data_bank.get_holding_registers(0, 2)
        if regs is None:
            continue

        joint1_deg, joint2_deg = regs[0], regs[1]

        if joint1_deg != prev_j1 or joint2_deg != prev_j2:
            prev_j1, prev_j2 = joint1_deg, joint2_deg

            # degree to radian
            j1_rad = joint1_deg * 3.1416 / 180
            j2_rad = joint2_deg * 3.1416 / 180

            # Update joints
            joint1.axis = vector(cos(j1_rad), sin(j1_rad), 0)
            joint2.pos = joint1.pos + joint1.axis
            joint2.axis = vector(cos(j1_rad + j2_rad), sin(j1_rad + j2_rad), 0)


# Thread starting
t = threading.Thread(target=start_modbus_server)
t.start()

update_robot_arm()
