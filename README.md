# 🚗 RC Car ESP32 – Control por WiFi con Doble Joystick

Este proyecto permite controlar una *camioneta RC pequeña* equipada con:

- 🔧 *1 motor de tracción* (puente H + PWM)  
- 🔄 *1 servomotor de dirección*  
- 📶 *WiFi Access Point integrado*  
- 🎮 *Interfaz web con dos joysticks multitouch*

El ESP32 genera una red WiFi propia y sirve una página web donde puedes manejar el motor y el servo mediante dos joysticks táctiles independientes.

---

## 📡 Características principales

- ✔ Control desde cualquier navegador  
- ✔ Joysticks multitouch sin interferencias  
- ✔ Servo limitado: *20° a 160°*  
- ✔ Motor con control proporcional de velocidad  
- ✔ Todo en un solo archivo MicroPython

---

## 🔌 Conexiones de hardware

| Componente | Pin ESP32 | Descripción |
|-----------|-----------|-------------|
| Motor IN1 | GPIO 27   | Dirección 1 |
| Motor IN2 | GPIO 25   | Dirección 2 |
| Motor PWM | GPIO 26   | Velocidad PWM |
| Servo     | GPIO 17   | Señal (50 Hz) |

---

## 📶 Configuración WiFi

El ESP32 crea una red:

- *SSID:* RC_CAR_WIFI  
- *PASSWORD:* 12345678  
- *IP:* 192.168.4.1  

Abre esta IP en tu navegador para controlar el coche.

---

## 🕹 Interfaz Web

### Joystick izquierdo → Motor  
- Arriba: Avanza  
- Abajo: Retrocede  
- Centro: Stop  
- Control proporcional según distancia al centro

### Joystick derecho → Dirección  
- Izquierda/derecha: Gira  
- Centro: Recto (90°)  
- Rango limitado: *20° a 160°*

---

## ▶ Cómo usarlo

1. Copia el código completo al ESP32 con Thonny.  
2. Reinicia.  
3. Conéctate al WiFi RC_CAR_WIFI.  
4. Abre http://192.168.4.1.  
5. Controla tu camioneta RC.

---

## 🛠 Requisitos

- ESP32 con MicroPython  
- Puente H (L298N, L293D o similar)  
- Servo estándar (SG90, MG996R…)  
- Fuente estable para motor y servo  
- Cualquier celular o PC con navegador

---

## 📌 Notas

- El servo está limitado para proteger la dirección.  
- Si hay vibración, revisa la fuente de alimentación.  
- Funciona perfecto en pantallas táctiles multitouch.

---
## 🔧 Temas a mejorar (Ideas para futuras versiones)
1. Seguridad y estabilidad
- Agregar cifrado WPA2 o cambiar contraseña desde la interfaz.
- Implementar reconexión automática del servidor web ante fallos.
- Proteger las rutas de control con autenticación simple.

2. Control y precisión
- Linearizar la respuesta del servo para movimientos más suaves.
- Usar un control PID para el motor y mejorar la tracción.
- Ajustar el PWM a una curva exponencial para mayor sensibilidad a baja velocidad.

3. Interfaz Web
- Añadir indicadores visuales (velocidad, ángulo actual).
- Usar WebSockets para reducir latencia frente a peticiones HTTP.
- Integrar un modo “gamepad real” compatible con controladores Bluetooth.

4. Hardware
- Utilizar un driver de motor más eficiente (TB6612FNG) para menor consumo.
- Incorporar sensor de batería para evitar descargas profundas.
Añadir luces LED controladas desde la interfaz.

5. Funcionalidades avanzadas
- Modo autónomo con sensores ultrasónicos o cámara.
- Grabación de trayectorias o modos de conducción predefinidos.
---
# ✅ Conclusión del proyecto

- Este proyecto de RC Car controlado por WiFi con ESP32 demuestra una integración eficiente entre hardware y software, logrando un sistema de control remoto estable, intuitivo y fácil de usar desde cualquier dispositivo con navegador. Gracias a la creación de un punto de acceso propio y a la interfaz web con doble joystick, el vehículo puede ser controlado sin necesidad de aplicaciones externas, cables o configuraciones complejas. La implementación en un solo archivo MicroPython simplifica la programación y facilita la replicación del proyecto. En general, se logra un sistema funcional, didáctico y escalable, ideal tanto para aprendizaje como para proyectos más avanzados de robótica o IoT.
---