import network
import machine
import time
import uasyncio as asyncio
import uwebsockets.server as ws

# ======================
#   WIFI ACCESS POINT
# ======================
ap = network.WLAN(network.AP_IF)
ap.active(True)
ap.config(essid="CarroRC", password="12345678")  # cambia si quieres
print("AP Iniciado:", ap.ifconfig())

# ======================
#   MOTOR L298N
# ======================
ENA = machine.PWM(machine.Pin(14), freq=1000)
IN1 = machine.Pin(27, machine.Pin.OUT)
IN2 = machine.Pin(26, machine.Pin.OUT)

def motor_stop():
    ENA.duty(0)
    IN1.value(0)
    IN2.value(0)

def motor_forward(speed):
    IN1.value(1)
    IN2.value(0)
    ENA.duty(int(speed * 1023))

def motor_backward(speed):
    IN1.value(0)
    IN2.value(1)
    ENA.duty(int(speed * 1023))

motor_stop()

# ======================
#       SERVO
# ======================
servo = machine.PWM(machine.Pin(15), freq=50)

def set_servo(angle):
    # 0° → 0.5 ms → 1638 duty_u16
    # 180° → 2.5 ms → 8192 duty_u16
    min_duty = 1638
    max_duty = 8192
    duty = int(min_duty + (angle/180) * (max_duty - min_duty))
    servo.duty_u16(duty)

set_servo(90)

# ======================
#   WEBSOCKET SERVER
# ======================
async def ws_handler(reader, writer):
    websocket = await ws.serve(reader, writer)
    print("Cliente conectado")

    try:
        while True:
            msg = await websocket.recv()
            if not msg:
                break

            print("CMD:", msg)

            if msg == "F": motor_forward(0.8)
            elif msg == "B": motor_backward(0.8)
            elif msg == "S": motor_stop()

            elif msg == "L": set_servo(45)
            elif msg == "R": set_servo(135)
            elif msg == "C": set_servo(90)

    except Exception as e:
        print("Error:", e)

    print("Cliente desconectado")
    await websocket.close()

# ======================
#     MAIN LOOP
# ======================
async def main():
    print("Servidor WebSocket listo en ws://192.168.4.1:8765")
    await asyncio.start_server(ws_handler, "0.0.0.0", 8765)

asyncio.run(main())
