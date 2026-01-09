# Mentoría 4: Retardos, Macros y Subrutinas en AVR (ATmega328P)

**Autor:** Luis David Barahona Valdivieso  
**Fecha:** 25/04/2025

---

## 1. Macros

### 1.1. Planteamiento del problema e identificación de requerimientos
El objetivo es crear una **macro** en ensamblador que permita realizar un **desplazamiento aritmético a la derecha (ASR)**. Esta operación es fundamental para realizar divisiones rápidas entre potencias de 2 (2^n).

* **Ejemplo:** Para dividir $1024$ entre $128$, realizamos $1024 >> 7$, ya que $2^7 = 128$. El resultado esperado es $8$.

### 1.2. Diagrama de bloques y de flujo
La macro se inserta en el código fuente y el preprocesador la expande cada vez que se invoca.



### 1.3. Código de Referencia
* **Ensamblador:** [ASR_Code_Assembler/main.asm](https://github.com/luisbarahona100/Mentorias/blob/main/Mentor%C3%ADa%204/ASR_Arithmetic_Shift_Right/ASR_Code_Assembler/AssemblerApplication1/main.asm)
* **C (Con Macro):** [ASR_Code_C_Macro/main.c](https://github.com/luisbarahona100/Mentorias/blob/main/Mentor%C3%ADa%204/ASR_Arithmetic_Shift_Right/ASR_Code_C_Macro/ASR_Code_C_Macro/main.c)
* **C (Con Rutina):** [ASR_C_Code/main.c](https://github.com/luisbarahona100/Mentorias/blob/main/Mentor%C3%ADa%204/ASR_Arithmetic_Shift_Right/ASR_Code_C_Rutina/ASR_C_Code/main.c)

### 1.4. Simulación de Casos
| Caso | Descripción | Resultado en Registro |
| :--- | :--- | :--- |
| **Caso 1** | Proceso iterativo mientras $n \neq 0$. | Desplazamiento bit a bit. |
| **Caso 2** | Finalización tras 7 desplazamientos. | Registro Low = `0x08` (8 decimal). |
| **Caso 3** | División $1024 / 1024$ ($1024 >> 10$). | Registro Low = `0x01`. |

---

## 2. Subrutinas y Retardos

### 2.1. Planteamiento del problema
Implementar un sistema que permita conmutar (encender/apagar) un LED cada segundo.

### 2.2. Identificación de requerimientos
* **Entrada:** Switch con resistencia pull-down.
* **Salida:** LED indicador.
* **Lógica:** El parpadeo solo ocurre si el switch está activado.

### 2.3. Diagrama de bloques y de flujo
Se utiliza una subrutina de retardo basada en ciclos de máquina para lograr el tiempo de 1 segundo de forma precisa.



### 2.4. Implementación y Documentación
* **Código Ensamblador:** [RetardoAVREnsamblador/main.asm](https://github.com/luisbarahona100/Mentorias/blob/main/Mentor%C3%ADa%204/Retardos/RetardoAVREnsamblador/RetardoAVREnsamblador/main.asm)
* **Código en C:** [RetardoAVR_CodeC/main.c](https://github.com/luisbarahona100/Mentorias/blob/main/Mentor%C3%ADa%204/Retardos/RetardoAVR_CodeC/RetardoAVR_CodeC/main.c)
* **Herramienta de Cálculo:** [Script Python para valores de R](https://github.com/luisbarahona100/Mentorias/blob/main/Mentor%C3%ADa%204/Retardos/delay2AVR.py)

---

## 3. Anexo: Plantillas Base

### 3.1. Plantillas en AVR Ensamblador

#### 3.1.1. Estructura General
```assembly
.include "m328Pdef.inc"

.org 0x00
    rjmp RESET

.def temp = r16

RESET:
    ; Configuración de Stack Pointer y Puertos
MAIN:
    ; Lógica principal
    rjmp MAIN
