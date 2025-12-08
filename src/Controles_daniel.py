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
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
<title>🏎️ RC Car Controller</title>

<style>
/* VARIABLES */
:root {
    --bg-color: #1a1a1a;
    --canvas-bg: #333;
    --joystick-color: #08f;
    --text-color: #eee;
    --outline-color: #555;
}

body {
    background: var(--bg-color);
    color: var(--text-color);
    text-align: center;
    font-family: Arial, sans-serif;
    margin: 0;
    padding: 20px;
    user-select: none; /* Evita la selección de texto en móviles */
}

h2 {
    margin-bottom: 30px;
}

.box {
    display: flex;
    justify-content: center;
    align-items: flex-start; /* Alinea arriba si el contenido varía */
    flex-wrap: wrap; /* Permite que los joysticks se apilen en pantallas pequeñas */
    gap: 20px;
}

.control-container {
    display: flex;
    flex-direction: column;
    align-items: center;
    margin: 10px;
}

canvas {
    background: var(--canvas-bg);
    border-radius: 50%;
    touch-action: none;
    box-shadow: 0 0 15px rgba(0, 0, 0, 0.5);
}

.value-display {
    margin-top: 10px;
    font-size: 1.2em;
    min-height: 1.4em; /* Para evitar saltos de diseño */
}
</style>
</head>
<body>
<script src="Java.js"></script>
<h2>🏎️ RC Car Web Controller</h2>

<div class="box">
    <div class="control-container">
        <canvas id="joy1" width="200" height="200"></canvas>
        <div class="value-display" id="motor-val">Potencia: 0</div>
    </div>
    
    <div class="control-container">
        <canvas id="joy2" width="200" height="200"></canvas>
        <div class="value-display" id="servo-val">Ángulo: 90°</div>
    </div>
</div>

<script>
function throttle(func, limit) {
    let lastFunc;
    let lastRan;
    return function() {
        const context = this;
        const args = arguments;
        if (!lastRan) {
            func.apply(context, args);
            lastRan = Date.now();
        } else {
            clearTimeout(lastFunc);
            lastFunc = setTimeout(function() {
                if ((Date.now() - lastRan) >= limit) {
                    func.apply(context, args);
                    lastRan = Date.now();
                }
            }, limit - (Date.now() - lastRan));
        }
    };
}

// ===========================
// GENERIC JOYSTICK CLASS
// ===========================
class Joystick {
    constructor(canvasId, callback) {
        this.canvas = document.getElementById(canvasId);
        this.ctx = this.canvas.getContext("2d");
        this.w = this.canvas.width;
        this.h = this.canvas.height;
        this.cx = this.w / 2;
        this.cy = this.h / 2;
        this.radius = 80; // Radio del área de control
        this.knobRadius = 30; // Radio de la perilla
        this.active = false;
        
        // Usar throttle para limitar la frecuencia de envío de comandos a 50ms
        this.throttledCallback = throttle(callback, 50); 
        this.stopCallback = callback; // Para el comando de parada (se ejecuta inmediatamente)

        this.draw(this.cx, this.cy);
        this.setupListeners();
    }

    draw(x, y) {
        this.ctx.clearRect(0, 0, this.w, this.h);
        
        // Dibujar borde/círculo exterior
        this.ctx.beginPath();
        this.ctx.arc(this.cx, this.cy, this.radius, 0, Math.PI * 2);
        this.ctx.strokeStyle = "var(--outline-color)";
        this.ctx.lineWidth = 4;
        this.ctx.stroke();

        // Dibujar perilla
        this.ctx.beginPath();
        this.ctx.arc(x, y, this.knobRadius, 0, 2 * Math.PI);
        this.ctx.fillStyle = this.active ? "#0cf" : "var(--joystick-color)"; // Feedback visual
        this.ctx.fill();
    }

    handle(evt) {
        const rect = this.canvas.getBoundingClientRect();
        // Manejar el primer toque si es un evento touch
        const touch = evt.touches ? evt.touches[0] : evt; 
        
        let x = touch.clientX - rect.left;
        let y = touch.clientY - rect.top;
        let dx = x - this.cx;
        let dy = y - this.cy;
        let dist = Math.sqrt(dx * dx + dy * dy);

        if (dist > this.radius) {
            // Limitar a la circunferencia
            dx = dx * this.radius / dist;
            dy = dy * this.radius / dist;
        }

        this.draw(this.cx + dx, this.cy + dy);

        // Mapear -radius..radius a -100..100
        const valX = Math.round((dx / this.radius) * 100);
        const valY = Math.round((dy / this.radius) * 100);

        this.throttledCallback(valX, valY);
    }
    
    stop() {
        this.active = false;
        this.draw(this.cx, this.cy);
        this.stopCallback(0, 0); 
    }

    setupListeners() {
        // Desktop (Mouse)
        this.canvas.addEventListener('mousedown', (e) => {
            this.active = true;
            this.handle(e);
        });
        document.addEventListener('mousemove', (e) => { 
            if (this.active) this.handle(e); 
        });
        document.addEventListener('mouseup', () => { 
            if (this.active) this.stop(); 
        });
        this.canvas.addEventListener('mouseleave', () => {
            // Permite que el control de document.onmouseup maneje la detención
            // o se detiene si el mouse sale sin soltarlo
            if (this.active) this.stop(); 
        });

        // Mobile (Touch)
        this.canvas.addEventListener('touchstart', (e) => {
            e.preventDefault(); // Evita scroll/zoom
            this.active = true;
            this.handle(e);
        }, {passive: false}); // passive: false es importante para preventDefault
        document.addEventListener('touchmove', (e) => {
            if (this.active) this.handle(e);
        });
        document.addEventListener('touchend', (e) => {
            if (this.active) this.stop();
        });
        document.addEventListener('touchcancel', (e) => {
            if (this.active) this.stop();
        });
    }
}

new Joystick("joy1", (x, y) => {
    // Usamos -y ya que Arriba es negativo en coordenadas de pantalla, 
    // pero queremos que Arriba = positivo para la potencia.
    const power = -y;
    document.getElementById("motor-val").textContent = `Potencia: ${power}`;
    
    // 💡 Fetch: No necesita esperar la respuesta, ya que el servidor enviará 204 No Content
    fetch(`/motor?power=${power}`).catch(e => console.error("Error motor:", e));
});

// ===========================
// JOYSTICK 2 = SERVO (Dirección)
// ===========================
new Joystick("joy2", (x, y) => {
    // Mapear -100..100 (horizontal x) a 0..180 grados
    // (x + 100) -> 0..200. Multiplicar por 0.9 (180/200) -> 0..180
    const angle = Math.round((x + 100) * 0.9); 
    document.getElementById("servo-val").textContent = `Ángulo: ${angle}°`;

    fetch(`/servo?angle=${angle}`).catch(e => console.error("Error servo:", e));
});

let motorActive = false;
let servoActive = false;

// Almacena el estado actual para evitar enviar comandos duplicados
const commandState = {
    power: 0,
    angle: 90
};

// Función para enviar comandos de motor
function sendMotorCommand(power) {
    if (commandState.power !== power) {
        commandState.power = power;
        document.getElementById("motor-val").textContent = `Potencia: ${power} (KEY)`;
        fetch(`/motor?power=${power}`).catch(e => console.error("Error motor:", e));
    }
}

// Función para enviar comandos de servo (dirección)
function sendServoCommand(angle) {
    if (commandState.angle !== angle) {
        commandState.angle = angle;
        // Mapea el ángulo de 0-180 a un texto de dirección
        let direction = angle > 90 ? 'Derecha' : (angle < 90 ? 'Izquierda' : 'Centro');
        document.getElementById("servo-val").textContent = `Ángulo: ${angle}° (${direction})`;
        fetch(`/servo?angle=${angle}`).catch(e => console.error("Error servo:", e));
    }
}

document.addEventListener('keydown', (event) => {
    // Evita la acción por defecto (ej. scroll de la página)
    if (['ArrowUp', 'ArrowDown', 'ArrowLeft', 'ArrowRight'].includes(event.key)) {
        event.preventDefault();
    }

    switch (event.key) {
        case 'ArrowUp':
        case 'w':
            if (!motorActive) {
                sendMotorCommand(100);
                motorActive = true;
            }
            break;
        case 'ArrowDown':
        case 's':
            if (!motorActive) {
                sendMotorCommand(-100); // Máxima potencia negativa (Atrás)
                motorActive = true;
            }
            break;

        // --- SERVO (DIRECCIÓN) ---
        case 'ArrowLeft':
        case 'a':
            if (!servoActive) {
                sendServoCommand(0); // Máximo a la izquierda
                servoActive = true;
            }
            break;
        case 'ArrowRight':
        case 'd':
            if (!servoActive) {
                sendServoCommand(180); // Máximo a la derecha
                servoActive = true;
            }
            break;
    }
});

document.addEventListener('keyup', (event) => {
    switch (event.key) {
        // --- MOTOR (PARADA) ---
        case 'ArrowUp':
        case 'ArrowDown':
        case 'w':
        case 's':
            if (motorActive) {
                sendMotorCommand(0); // Potencia 0 (Parar)
                motorActive = false;
            }
            break;

        // --- SERVO (CENTRO) ---
        case 'ArrowLeft':
        case 'ArrowRight':
        case 'a':
        case 'd':
            if (servoActive) {
                sendServoCommand(90); // Ángulo central
                servoActive = false;
            }
            break;
    }
});
</script>

</body>
</html>

"""

# ===============================
# SIMPLE HTTP SERVER
# ===============================
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