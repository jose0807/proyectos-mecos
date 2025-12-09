import network
import socket
from machine import Pin, PWM
import time

ssid = "RC_CAR_WIFI"
password = "12345678"

ap = network.WLAN(network.AP_IF)
ap.active(True)
ap.config(essid=ssid, password=password)
print("Conéctate a:", ssid)
print("IP:", ap.ifconfig()[0])

in1 = Pin(27, Pin.OUT)
in2 = Pin(25, Pin.OUT)
pwm_motor = PWM(Pin(26), freq=1000)
pwm_motor.duty(0)

servo = PWM(Pin(15), freq=50)

def set_servo(angle):
    duty = int((angle / 180) * 100) + 25
    servo.duty(duty)

set_servo(90)

def set_motor(power):
    if power > 0:
        in1.value(1)
        in2.value(0)
    elif power < 0:
        in1.value(0)
        in2.value(1)
    else:
        in1.value(0)
        in2.value(0)

    duty = int(abs(power) * 10.23)
    pwm_motor.duty(duty)


set_motor(0)

html = """<!DOCTYPE html>
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>RC Car</title>

<style>
body{background:#111;color:white;text-align:center;}
.box{display:flex;justify-content:center;margin-top:40px;}
canvas{background:#222;border-radius:50%;touch-action:none;}
</style>
</head>
<body>

<h2>🚗 RC Car Web Controller</h2>

<div class="box">
  <canvas id="joy1" width="200" height="200"></canvas>
  <canvas id="joy2" width="200" height="200" style="margin-left:30px;"></canvas>
</div>

<script>
function Joystick(canvas, callback){
    const ctx = canvas.getContext("2d");
    const w = canvas.width, h = canvas.height;
    const cx = w/2, cy = h/2;
    let active = false;

    function draw(x, y){
        ctx.clearRect(0,0,w,h);
        ctx.beginPath();
        ctx.arc(cx,cy,80,0,Math.PI*2);
        ctx.strokeStyle="#555"; ctx.lineWidth=4; ctx.stroke();

        ctx.beginPath();
        ctx.arc(x, y, 30, 0, 2*Math.PI);
        ctx.fillStyle="#08f"; ctx.fill();
    }

    draw(cx,cy);

    function handle(evt){
        const rect = canvas.getBoundingClientRect();
        const touch = evt.touches ? evt.touches[0] : evt;
        let x = touch.clientX - rect.left;
        let y = touch.clientY - rect.top;
        let dx = x - cx;
        let dy = y - cy;
        let dist = Math.sqrt(dx*dx + dy*dy);

        if (dist > 80){
            dx = dx * 80 / dist;
            dy = dy * 80 / dist;
        }

        draw(cx + dx, cy + dy);

        const valX = Math.round((dx / 80) * 100);
        const valY = Math.round((dy / 80) * 100);

        callback(valX, valY);
    }

    canvas.onmousedown = e=>{active=true; handle(e);}
    canvas.onmousemove = e=>{ if(active) handle(e); }
    canvas.onmouseup = e=>{active=false; draw(cx,cy); callback(0,0);}
    canvas.onmouseleave = e=>{active=false; draw(cx,cy); callback(0,0);}

    canvas.ontouchstart = e=>{active=true; handle(e);}
    canvas.ontouchmove = e=>{handle(e); }
    canvas.ontouchend = e=>{active=false; draw(cx,cy); callback(0,0);}
}

new Joystick(document.getElementById("joy1"), (x,y)=>{
    fetch(`/motor?power=${-y}`);   // Arriba = positivo
});

new Joystick(document.getElementById("joy2"), (x,y)=>{
    let angle = Math.round((x + 100) * 0.9); // map -100..100 → 0..180
    fetch(`/servo?angle=${angle}`);
});
</script>

</body>
</html>
"""

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(("0.0.0.0", 80))
s.listen(5)

print("Servidor iniciado. Abre en el navegador:", ap.ifconfig()[0])

while True:
    conn, addr = s.accept()
    req = conn.recv(1024).decode()

    if "GET /motor" in req:
        try:
            power = int(req.split("power=")[1].split(" ")[0])
            set_motor(power)
        except:
            pass

    if "GET /servo" in req:
        try:
            angle = int(req.split("angle=")[1].split(" ")[0])
            set_servo(angle)
        except:
            pass

    conn.send("HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n")
    conn.send(html)
    conn.close()
