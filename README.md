# proyectos-mecos
in this repository we will be working on diverse programming proyects specifically for the programmming methodologies subject

# Proyecto Profesional: Carro RC Controlado con ESP32 y Control de Xbox

## 1. Introducción

Este documento describe el diseño, arquitectura, implementación y consideraciones técnicas de un vehículo radio controlado (RC) basado en un microcontrolador **ESP32**, controlado mediante un mando **Xbox**. El proyecto integra tecnologías modernas de comunicación inalámbrica, control embebido, electrónica de potencia y diseño mecánico, constituyendo una plataforma versátil para prototipado y aplicaciones educativas.

## 2. Objetivo del Proyecto

Desarrollar un sistema de control remoto robusto y de baja latencia para un carro RC empleando:

* Un **ESP32** como unidad principal de proceso y comunicación.
* Un **control Xbox** como dispositivo de entrada.
* Un sistema de tracción basado en motores DC con puente H.
* Un servomotor para la dirección.
* Comunicación Bluetooth y WiFi como medios alternativos de control.
* Alimentación mediante batería portátil recargable.

## 3. Arquitectura General del Sistema

El sistema se compone de los siguientes módulos principales:

### 3.1 Unidad de Control (ESP32)

* Gestiona la lectura de comandos recibidos del control Xbox.
* Genera las señales PWM para motor y servo.
* Supervisa parámetros eléctricos como voltaje de batería.
* Implementa protocolos Bluetooth y/o WiFi.
* Contiene la lógica de seguridad (frenado, pérdida de señal, límites).

### 3.2 Módulo de Potencia

* **Puente H L298N** para el control bidireccional de motores DC.
* Regulación de voltaje para el servo.
* Protección mediante diodos flyback y fusibles.
* Sistema de conversión de 7.2V → 5V para microcontrolador.

### 3.3 Sistema de Propulsión

* Dos motores DC de tracción trasera.
* Engranaje adecuado para torque y velocidad.
* Chasis impreso en 3D o base de aluminio.

### 3.4 Sistema de Dirección

* Servomotor MG996R o equivalente.
* Biela y mecanismo de giro tipo "rack and pinion" o articulación directa.

### 3.5 Control de Xbox

El control Xbox se comunica mediante Bluetooth con el ESP32.
Se emplean los siguientes ejes y botones:

* **Joy izquierdo**: aceleración/freno.
* **Joy derecho**: dirección.
* **Botón A**: modo turbo.
* **Botón B**: paro de emergencia.
* **Botón X**: luces.
* **Botón Y**: cambio de modo de control (WiFi/Bluetooth).

## 4. Diagrama de Bloques

```
[Control Xbox] --BT--> [ESP32] --PWM--> [Servo Dirección]
                               \--PWM--> [Puente H] --> [Motores]
                               \--ADC--> [Monitoreo de Batería]
```

## 5. Comunicación Bluetooth con Control Xbox

El firmware implementa el stack Bluetooth HID compatible con controles Xbox.
Funciones principales:

* Parseo de reportes HID.
* Traducción de valores analógicos en rangos de control para motores y servo.
* Manejo de desconexiones y timeout de seguridad.

## 6. Lógica de Control del Vehículo

### 6.1 Dirección

* Conversión de posición del joystick derecho (−1 a 1) en ángulos de servo (0°–180°).
* Filtro de suavizado para evitar movimientos bruscos.

### 6.2 Aceleración

* Lectura del eje vertical del joystick izquierdo.
* Mapeo a velocidad PWM (0–100%).
* Frenado eléctrico cuando regresa a posición neutra.

### 6.3 Modo Turbo

* Incremento temporal del PWM máximo (hasta 120%).
* Solo disponible si el nivel de batería es seguro.

### 6.4 Paro de Emergencia

* Detención inmediata de motores.
* Servo regresa a posición central.
* Restablecimiento solo con combinación segura (ej.: presionar A+B).

## 7. Firmware en el ESP32

El firmware está dividido en módulos:

* **input_xbox.h/cpp**: manejo HID.
* **motor_control.h/cpp**: gestión PWM y curvas de aceleración.
* **servo_control.h/cpp**: control de dirección con suavizado.
* **safety.h/cpp**: monitoreo de batería, límite de corriente, watchdog.
* **main.cpp**: inicialización general y loop principal.

Principios aplicados:

* Programación no bloqueante.
* Tareas paralelas usando FreeRTOS.
* Baja latencia en lectura de entradas (<10 ms).

## 8. Alimentación del Sistema

* Batería principal: **7.2V 2000–4000 mAh**.
* Regulador step-down a 5V para ESP32.
* Canal 5V dedicado para servo para evitar ruido eléctrico.
* Capacitores de desacoplo próximos a puente H y servos.

## 9. Ensamblaje Mecánico

* Chasis impreso en 3D en PLA o PETG.
* Montura universal para servo MG996R.
* Soportes laterales para protección de electrónica.
* Sistema de ventilación pasiva para L298N.
* Compartimento inferior para la batería.

## 10. Pruebas y Validación

Se realizaron las siguientes pruebas:

* **Prueba de comunicación Bluetooth**: latencia promedio 8–15 ms.
* **Prueba de tracción**: velocidad máxima estimada 12–18 km/h.
* **Prueba de dirección**: respuesta estable, sin jitter.
* **Prueba de estabilidad eléctrica**: sin reinicios del ESP32 bajo cargas intensas.
* **Prueba de seguridad**: detección de desconexión en <500 ms.

## 11. Conclusiones

El proyecto demuestra la viabilidad de un sistema RC profesional empleando tecnologías modernas y accesibles. El uso del ESP32 permite una arquitectura flexible con capacidades avanzadas de comunicación, mientras que el control Xbox ofrece ergonomía y precisión. La combinación de electrónica, mecánica e ingeniería de software convierte este proyecto en una plataforma ideal para aprendizaje, prototipado y aplicaciones de movilidad robótica.

## 12. Posibles Mejoras

* Transmisión de telemetría en pantalla del Xbox.
* Cámara FPV (WiFi o ESP-NOW).
* L298N reemplazado por un puente H MOSFET de alta eficiencia.
* Modo autónomo con sensores de proximidad.
* Iluminación LED direccionable.

## 13. Créditos

Desarrollado como parte de un proyecto educativo de ingeniería integrada: electrónica + programación + mecánica + diseño.
