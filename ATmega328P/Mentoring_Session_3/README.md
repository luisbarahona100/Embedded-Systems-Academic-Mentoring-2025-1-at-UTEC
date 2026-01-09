# Retardos, Macros y Subrutinas en AVR

**Autor:** Luis David Barahona Valdivieso  
**Fecha:** 25/04/2025

---

## Tabla de Contenidos

1. [Macros](#1-macros)
   - [1.1. Planteamiento del problema e identificación de requerimientos](#11-planteamiento-del-problema-e-identificación-de-requerimientos)
   - [1.2. Diagrama de bloques y de flujo](#12-diagrama-de-bloques-y-de-flujo)
   - [1.3. Código en Ensamblador y C](#13-código-en-ensamblador-y-c)
   - [1.4. Simulación de los casos en Microchip y Proteus](#14-simulación-de-los-casos-en-microchip-y-proteus)
   - [1.5. Implementación](#15-implementación)
   - [1.6. Documentación en GITHUB](#16-documentación-en-github)
2. [Subrutinas](#2-subrutinas)
   - [2.1. Planteamiento del problema](#21-planteamiento-del-problema)
   - [2.2. Identificación de requerimientos](#22-identificación-de-requerimientos)
   - [2.3. Diagrama de bloques y de flujo](#23-diagrama-de-bloques-y-de-flujo)
   - [2.4. Código en Ensamblador](#24-código-en-ensamblador)
   - [2.5. Código en C](#25-código-en-c)
   - [2.6. Simulación de los casos en Microchip y Proteus](#26-simulación-de-los-casos-en-microchip-y-proteus)
   - [2.7. Implementación](#27-implementación)
   - [2.8. Documentación en GITHUB](#28-documentación-en-github)
3. [Anexo](#3-anexo)
   - [3.1. Plantilla base de un código en AVR Ensamblador](#31-plantilla-base-de-un-código-en-avr-ensamblador)
   - [3.2. Plantilla base de un código en C](#32-plantilla-base-de-un-código-en-c)

---

## 1. Macros

### 1.1. Planteamiento del problema e identificación de requerimientos

Crear una macro capaz de permitir el **desplazamiento aritmético a la derecha**. Recordemos que este operador permite realizar divisiones con números que son potencias de 2.

**Ejemplo:**  
Dividir `1024 / 128` es igual a `1024 >> 7`, pues `2^7 = 128`. En ambos casos el resultado debe generar `8`.

### 1.2. Diagrama de bloques y de flujo

```
INICIO
  ↓
Cargar valor a dividir
  ↓
Cargar número de desplazamientos (n)
  ↓
¿n = 0? → SÍ → FIN
  ↓ NO
Desplazamiento aritmético a la derecha
  ↓
Decrementar n
  ↓
Volver a verificar n
```

### 1.3. Código en Ensamblador y C

**Código en Ensamblador:**  
[ASR_Code_Assembler](https://github.com/luisbarahona100/Mentorias/blob/main/Mentor%C3%ADa%204/ASR_Arithmetic_Shift_Right/ASR_Code_Assembler/AssemblerApplication1/main.asm)

**Código en C con macro:**  
[ASR_Code_C_Macro](https://github.com/luisbarahona100/Mentorias/blob/main/Mentor%C3%ADa%204/ASR_Arithmetic_Shift_Right/ASR_Code_C_Macro/ASR_Code_C_Macro/main.c)

**Código en C con rutina:**  
[ASR_Code_C_Rutina](https://github.com/luisbarahona100/Mentorias/blob/main/Mentor%C3%ADa%204/ASR_Arithmetic_Shift_Right/ASR_Code_C_Rutina/ASR_C_Code/main.c)

### 1.4. Simulación de los casos en Microchip y Proteus

#### SIMULACIÓN USANDO MACRO

**CASO 1:** Mientras `n ≠ 0` aún no hemos realizado los 7 desplazamientos necesarios

**CASO 2:** Cuando `n = 0` (quiere decir que han pasado 7 desplazamientos), `low` debería ser `0x08`, pues la división entre `1024` y `128` es `8`.

#### SIMULACIÓN USANDO RUTINA

**CASO 1:** Dentro de la rutina, realizando los desplazamientos

**CASO 2:** Dividir `1024/128 = 1024 >> 7 = 8`

**CASO 3:** Dividir `1024/1024 = 1024 >> 10 = 1`

### 1.5. Implementación

*(Incluir imágenes o descripción de la implementación física si está disponible)*

### 1.6. Documentación en GITHUB

[Repositorio completo - ASR_Arithmetic_Shift_Right](https://github.com/luisbarahona100/Mentorias/tree/main/Mentor%C3%ADa%204/ASR_Arithmetic_Shift_Right)

---

## 2. Subrutinas

### 2.1. Planteamiento del problema

Prender y apagar un LED cada segundo.

### 2.2. Identificación de requerimientos

- **Entrada:** Switch en pull-down
- **Salida:** LED

### 2.3. Diagrama de bloques y de flujo

```
INICIO
  ↓
Configurar puertos
  ↓
LOOP PRINCIPAL
  ↓
¿Switch presionado? → NO → Volver al loop
  ↓ SÍ
Encender LED
  ↓
Llamar subrutina de retardo (1s)
  ↓
Apagar LED
  ↓
Llamar subrutina de retardo (1s)
  ↓
Volver al loop principal
```

### 2.4. Código en Ensamblador

[RetardoAVREnsamblador/main.asm](https://github.com/luisbarahona100/Mentorias/blob/main/Mentor%C3%ADa%204/Retardos/RetardoAVREnsamblador/RetardoAVREnsamblador/main.asm)

### 2.5. Código en C

[RetardoAVR_CodeC/main.c](https://github.com/luisbarahona100/Mentorias/blob/main/Mentor%C3%ADa%204/Retardos/RetardoAVR_CodeC/RetardoAVR_CodeC/main.c)

### 2.6. Simulación de los casos en Microchip y Proteus

**CASO 1:** SWITCH NO PRESIONADO  
- El LED permanece apagado

**CASO 2:** SWITCH PRESIONADO  
- El LED parpadea cada segundo (1s encendido, 1s apagado)

### 2.7. Implementación

*(Incluir imágenes o descripción de la implementación física si está disponible)*

### 2.8. Documentación en GITHUB

**Code AVR Ensamblador:**  
[RetardoAVREnsamblador/main.asm](https://github.com/luisbarahona100/Mentorias/blob/main/Mentor%C3%ADa%204/Retardos/RetardoAVREnsamblador/RetardoAVREnsamblador/main.asm)

**Code AVR C:**  
[RetardoAVR_CodeC/main.c](https://github.com/luisbarahona100/Mentorias/blob/main/Mentor%C3%ADa%204/Retardos/RetardoAVR_CodeC/RetardoAVR_CodeC/main.c)

**Script Python para calcular el valor de los R:**  
[delay2AVR.py](https://github.com/luisbarahona100/Mentorias/blob/main/Mentor%C3%ADa%204/Retardos/delay2AVR.py)

---

## 3. Anexo

### 3.1. Plantilla base de un código en AVR Ensamblador

#### 3.1.1. Plantilla general de un programa en AVR Ensamblador

```asm
; --- Directivas iniciales ---
.include "m328Pdef.inc"

; --- Definición de macros ---

; --- Redireccionamiento a la posición 0x00 de la memoria de programa
.org 0x00
    rjmp RESET

; --- Variables temporales ---
.def temp = r16

; --- Configuración de puertos e inicialización ---
RESET:

; --- Programa principal ---
MAIN:

; --- Subrutinas ---
OTRAS_ETIQUETAS:
```

#### 3.1.2. Plantilla de una macro en AVR Ensamblador

```asm
; CREACIÓN DE MACRO
.macro toggle_bit
    ; Lógica de la macro
.endm

; USO DE MACRO
toggle_bit
```

> **Nota:** Es definido antes del MAIN

#### 3.1.3. Plantilla de una rutina en AVR Ensamblador

```asm
; CONFIGURAR STACK POINTER
.include "m328Pdef.inc"
.org 0x00
    rjmp RESET

RESET:
    LDI R19, LOW(RAMEND)
    OUT SPL, R19
    LDI R19, HIGH(RAMEND)
    OUT SPH, R19

; USAR RUTINA
MAIN:
    RCALL RUTINA_SUMAR
    RJMP MAIN

; DEFINIR RUTINA
RUTINA_SUMAR:
    ; Lógica de la suma
    RET
```

### 3.2. Plantilla base de un código en C

#### 3.2.1. Plantilla general de un programa en C

```c
#include <avr/io.h>
#include <util/delay.h>
#include <avr/interrupt.h>
#include "DEF_ATMEGA328P.h"
#include <avr/sfr_defs.h>

int main(){
    // Configuración inicial
    
    while (1){
        // Loop principal
    }
}
```

> **Recomendación:** Abrir el archivo `debug/.lss` para poder observar el código ensamblador equivalente al código C escrito.

#### 3.2.2. Plantilla de una macro en C

```c
// Macro para alternar el estado de un bit en un puerto
#define TOGGLE_BIT(port, pin) ((port) ^= (1 << (pin)))

// USO
TOGGLE_BIT(PORTB, PB0); // Alterna PB0
```

#### 3.2.3. Plantilla de una subrutina en C

```c
int rutina(int param1, int param2){
    // LÓGICA: Sumar param1 y param2
    return param1 + param2;
}

// USO
int resultado = 0;
resultado = rutina(1, 2);
```

> **Nota:** En C, una rutina es la función que conocemos de toda la vida.

---

## Recursos Adicionales

- [Repositorio completo de la Mentoría 4](https://github.com/luisbarahona100/Mentorias/tree/main/Mentor%C3%ADa%204)
- Documentación oficial de AVR
- Microchip Studio
- Proteus Design Suite

---

**© 2025 Luis David Barahona Valdivieso**
