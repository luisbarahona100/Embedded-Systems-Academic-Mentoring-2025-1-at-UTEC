# TIMER/COUNTER: Modos de Configuración y Aplicaciones

> **Autor:** Luis David Barahona Valdivieso  
> **Fecha:** 27.06.2025
> **Documento Completo + Imágenes:** https://docs.google.com/document/d/12DclIE2LXMmhjDwaQSpYQt8y0N6123_-Z8UKY278eEQ/edit?tab=t.0#heading=h.y11qxu3oi3lj

Esta guía presenta ejemplos prácticos de generación de señales PWM utilizando el Timer/Counter 0 del ATmega328P en diferentes modos de operación.

---

## Tabla de Contenidos

- [Introducción](#introducción)
- [1. Fast PWM Mode](#1-fast-pwm-mode)
  - [1.1 Ejemplo 1: Código en C](#11-ejemplo-1-código-en-c)
  - [1.2 Justificación de Cálculos](#12-justificación-de-cálculos)
  - [1.3 Simulación en Proteus](#13-simulación-en-proteus)
- [2. Phase Correct PWM Mode](#2-phase-correct-pwm-mode)
  - [2.1 Ejemplo 2: Código en C](#21-ejemplo-2-código-en-c)
  - [2.2 Justificación de Cálculos](#22-justificación-de-cálculos)
  - [2.3 Simulación en Proteus](#23-simulación-en-proteus)
- [3. CTC Mode Toggle](#3-ctc-mode-toggle)
  - [3.1 Ejemplo 3: Código en C](#31-ejemplo-3-código-en-c)
  - [3.2 Justificación de Cálculos](#32-justificación-de-cálculos)
  - [3.3 Simulación en Proteus](#33-simulación-en-proteus)
- [4. Comparación de Modos](#4-comparación-de-modos)
- [5. Anexos](#5-anexos)

---

## Introducción

Los Timer/Counter del ATmega328P permiten generar señales PWM (Pulse Width Modulation) que son fundamentales para:
- Control de servomotores
- Regulación de velocidad de motores DC
- Control de intensidad de LEDs
- Generación de señales de audio

Las señales PWM generadas se emiten a través de los pines:
- **PD6 (OC0A)**: Salida del canal A del Timer0
- **PD5 (OC0B)**: Salida del canal B del Timer0

---

## 1. Fast PWM Mode

### Características del Fast PWM
- **Operación:** El contador cuenta de 0 a 255 (TOP) de forma ascendente
- **Frecuencia máxima:** Mayor que Phase Correct PWM
- **Uso típico:** Aplicaciones que requieren alta frecuencia de conmutación

### Objetivo del Ejemplo 1
Generar dos señales PWM con el **máximo periodo posible**:
- **Señal 1 (OC0A):** Non-inverting mode, Duty Cycle 50%
- **Señal 2 (OC0B):** Inverting mode, Duty Cycle 25%

### 1.1 Ejemplo 1: Código en C
```c
/*
 * PWM_FAST.c
 * Generación de señales PWM en modo Fast PWM
 * 
 * Referencias:
 * - Video: https://www.youtube.com/watch?v=zpgvK63PLbM
 * - GitHub: https://github.com/CARLOS-QL/ATMEGA328P_EJEMPLOS/blob/main/PWM_FAST/PWM_FAST/main.c
 */

#define F_CPU 1000000  // Reloj de operación: 1 MHz
#include <avr/io.h>
#include <util/delay.h>
#include <avr/interrupt.h>
#include <avr/sfr_defs.h>

// Macros para manipulación de bits
#define set_bit(sfr, bit)   (_SFR_BYTE(sfr) |= _BV(bit))
#define clear_bit(sfr, bit) (_SFR_BYTE(sfr) &= ~_BV(bit))

int main(void)
{
    // Configurar pines como salida
    set_bit(DDRD, 5);  // PD5 -> OC0B
    set_bit(DDRD, 6);  // PD6 -> OC0A
    
    // Configurar Fast PWM Mode (WGM02:0 = 011)
    TCCR0B &= ~(1 << WGM02);  // WGM02 = 0
    TCCR0A |=  (1 << WGM01);  // WGM01 = 1
    TCCR0A |=  (1 << WGM00);  // WGM00 = 1
    
    // Configurar Prescaler = 1024 (CS02:0 = 101)
    TCCR0B &= ~(1 << CS02);   // CS02 = 0
    TCCR0B |=  (1 << CS01);   // CS01 = 1
    TCCR0B |=  (1 << CS00);   // CS00 = 1
    // Prescaler = 64

    // OC0A: Non-inverting mode (COM0A1:0 = 10)
    set_bit(TCCR0A, COM0A1);    // COM0A1 = 1
    clear_bit(TCCR0A, COM0A0);  // COM0A0 = 0
   
    // OC0B: Inverting mode (COM0B1:0 = 11)
    set_bit(TCCR0A, COM0B1);    // COM0B1 = 1
    set_bit(TCCR0A, COM0B0);    // COM0B0 = 1
    
    // Configurar Duty Cycle
    OCR0A = 127;  // 50% duty cycle -> (127+1)/256 = 50%
    OCR0B = 63;   // 25% duty cycle -> (63+1)/256 = 25%
    
    while (1) 
    {
        // Aquí se puede modificar dinámicamente OCR0A y OCR0B
        // para aplicaciones como control de servomotores
    }
}
```

### 1.2 Justificación de Cálculos

#### Frecuencia PWM
```
f_PWM = f_CPU / (Prescaler × 256)
f_PWM = 1,000,000 / (64 × 256)
f_PWM = 61.04 Hz
```

#### Periodo PWM
```
T_PWM = 1 / f_PWM
T_PWM = 1 / 61.04
T_PWM ≈ 16.38 ms
```

#### Duty Cycle
- **OC0A (Non-inverting):** `DC = (OCR0A + 1) / 256 = 128/256 = 50%`
- **OC0B (Inverting):** `DC = (256 - OCR0B - 1) / 256 = 192/256 = 75%` *(modo invertido)*

**Nota:** El documento menciona prescaler 64, lo cual genera un periodo diferente al cálculo mostrado en la imagen.

### 1.3 Simulación en Proteus

**Resultados esperados:**
- Periodo: ~16.38 ms (con prescaler 64)
- OC0A: 50% duty cycle, non-inverting
- OC0B: 25% duty cycle, inverting (equivale a 75% en la señal invertida)

---

## 2. Phase Correct PWM Mode

### Características del Phase Correct PWM
- **Operación:** El contador cuenta de 0 a 255 y luego de 255 a 0 (up-down counting)
- **Ventaja:** Mejor simetría de fase, ideal para control de motores
- **Frecuencia:** La mitad que Fast PWM (debido al conteo bidireccional)

### Objetivo del Ejemplo 2
Generar dos señales PWM con **máximo periodo posible**:
- **Señal 1 (OC0A):** Set on compare match when down-counting, Duty Cycle 50%
- **Señal 2 (OC0B):** Set on compare match when up-counting, Duty Cycle 25%

### 2.1 Ejemplo 2: Código en C
```c
/*
 * PWM_PHASE_CORRECT.c
 * Generación de señales PWM en modo Phase Correct
 */

#define F_CPU 1000000  // Reloj de operación: 1 MHz
#include <avr/io.h>
#include <util/delay.h>
#include <avr/interrupt.h>
#include <avr/sfr_defs.h>

#define set_bit(sfr, bit)   (_SFR_BYTE(sfr) |= _BV(bit))
#define clear_bit(sfr, bit) (_SFR_BYTE(sfr) &= ~_BV(bit))

int main(void)
{
    // Configurar pines como salida
    set_bit(DDRD, 5);  // PD5 -> OC0B
    set_bit(DDRD, 6);  // PD6 -> OC0A
    
    // Configurar Phase Correct PWM Mode (WGM02:0 = 001)
    TCCR0B &= ~(1 << WGM02);  // WGM02 = 0
    TCCR0A &= ~(1 << WGM01);  // WGM01 = 0
    TCCR0A |=  (1 << WGM00);  // WGM00 = 1
    
    // Configurar Prescaler = 1024 (CS02:0 = 101)
    TCCR0B |=  (1 << CS02);   // CS02 = 1
    TCCR0B &= ~(1 << CS01);   // CS01 = 0
    TCCR0B |=  (1 << CS00);   // CS00 = 1

    // OC0A: Set on compare match when down-counting (COM0A1:0 = 10)
    set_bit(TCCR0A, COM0A1);
    clear_bit(TCCR0A, COM0A0);
   
    // OC0B: Set on compare match when up-counting (COM0B1:0 = 11)
    set_bit(TCCR0A, COM0B1);
    set_bit(TCCR0A, COM0B0);
    
    // Configurar Duty Cycle
    OCR0A = 127;  // 50% duty cycle
    OCR0B = 63;   // 25% duty cycle
    
    while (1) 
    {
        // Modificación dinámica de PWM para servomotores
    }
}
```

### 2.2 Justificación de Cálculos

#### Frecuencia PWM
```
f_PWM = f_CPU / (Prescaler × 510)
f_PWM = 1,000,000 / (1024 × 510)
f_PWM ≈ 1.916 Hz
```

**Nota:** En Phase Correct PWM, el divisor es 510 (2 × 255) debido al conteo bidireccional.

#### Periodo PWM
```
T_PWM = 1 / f_PWM
T_PWM ≈ 522 ms
```

#### Duty Cycle
- **OC0A:** `DC = OCR0A / 255 = 127/255 ≈ 50%`
- **OC0B:** `DC = OCR0B / 255 = 63/255 ≈ 25%`

### 2.3 Simulación en Proteus

**Resultados obtenidos:**
- Periodo esperado: 522 ms
- Periodo medido: 521 ms ✓
- OC0A: 50% duty cycle (señal amarilla)
- OC0B: 25% duty cycle (señal celeste)

---

## 3. CTC Mode Toggle

### Características del CTC Mode
- **CTC:** Clear Timer on Compare Match
- **Toggle Mode:** Invierte la salida en cada comparación
- **Duty Cycle:** Siempre 50% (no ajustable)
- **Uso:** Generación de frecuencias precisas

### Objetivo del Ejemplo 3
Generar una señal PWM con 50% de duty cycle fijo usando CTC Toggle.

**Pregunta:** ¿Es posible variar el duty cycle en este modo?  
**Respuesta:** No, el modo Toggle en CTC siempre produce un duty cycle del 50%.

### 3.1 Ejemplo 3: Código en C
```c
/*
 * PWM_CTC_TOGGLE.c
 * Generación de señales PWM en modo CTC Toggle
 */

#define F_CPU 1000000  // Reloj de operación: 1 MHz
#include <avr/io.h>
#include <util/delay.h>
#include <avr/interrupt.h>
#include <avr/sfr_defs.h>

#define set_bit(sfr, bit)   (_SFR_BYTE(sfr) |= _BV(bit))
#define clear_bit(sfr, bit) (_SFR_BYTE(sfr) &= ~_BV(bit))

int main(void)
{
    // Configurar pines como salida
    set_bit(DDRD, 5);  // PD5 -> OC0B
    set_bit(DDRD, 6);  // PD6 -> OC0A
    
    // Configurar CTC Mode (WGM02:0 = 010)
    TCCR0B &= ~(1 << WGM02);  // WGM02 = 0
    TCCR0A |=  (1 << WGM01);  // WGM01 = 1
    TCCR0A &= ~(1 << WGM00);  // WGM00 = 0
    
    // Configurar Prescaler = 1024
    TCCR0B |=  (1 << CS02);   // CS02 = 1
    TCCR0B &= ~(1 << CS01);   // CS01 = 0
    TCCR0B |=  (1 << CS00);   // CS00 = 1

    // OC0A: Toggle on compare match (COM0A1:0 = 01)
    clear_bit(TCCR0A, COM0A1);
    set_bit(TCCR0A, COM0A0);
   
    // OC0B: Toggle on compare match (COM0B1:0 = 01)
    clear_bit(TCCR0A, COM0B1);
    set_bit(TCCR0A, COM0B0);
    
    // Configurar valores de comparación
    OCR0A = 255;  // Periodo máximo
    OCR0B = 1;    // Periodo mínimo
    
    while (1) 
    {
        // En CTC Toggle, el duty cycle siempre es 50%
    }
}
```

### 3.2 Justificación de Cálculos

#### Frecuencia de Toggle
```
f_toggle = f_CPU / (2 × Prescaler × (1 + OCR0A))
```

**Para OCR0A = 255:**
```
f_toggle = 1,000,000 / (2 × 1024 × 256)
f_toggle ≈ 1.907 Hz
T ≈ 524 ms
```

**Para OCR0B = 1:**
```
f_toggle = 1,000,000 / (2 × 1024 × 2)
f_toggle ≈ 244.14 Hz
T ≈ 4.1 ms
```

### 3.3 Simulación en Proteus

**Limitación encontrada:**  
En modo CTC Toggle, el Timer0 del ATmega328P solo puede generar **una señal a la vez**, no dos simultáneas en OC0A y OC0B.

**Solución alternativa:**  
Usar dos timers diferentes (Timer0 y Timer1/Timer2) si se necesitan dos señales CTC independientes.

---

## 4. Comparación de Modos

| Característica | Fast PWM | Phase Correct PWM | CTC Toggle |
|----------------|----------|-------------------|------------|
| **Conteo** | 0 → TOP | 0 → TOP → 0 | 0 → OCR0A (reset) |
| **Frecuencia relativa** | Alta | Media (mitad de Fast) | Configurable |
| **Duty Cycle** | 0-100% | 0-100% | Fijo 50% |
| **Simetría de fase** | No | Sí | Sí (50/50) |
| **Uso típico** | DAC, dimming LEDs | Control de motores | Generación de clocks |
| **TOP** | 255 (8-bit) | 255 (8-bit) | OCR0A |

---

## 5. Anexos

### Anexo A: Configuración en Microchip Studio

#### Pasos para crear un proyecto:
1. **New Project** → GCC C Executable Project
2. Seleccionar el microcontrolador: **ATmega328P**
3. Escribir el código en `main.c`
4. Compilar: **Build** → **Build Solution** (F7)

#### Archivos generados:
- **Debug/.hex:** Archivo para grabar en el microcontrolador
- **Output Files/.lss:** Código ensamblador equivalente (útil para debugging)

### Anexo B: Registros Importantes

#### TCCR0A (Timer/Counter Control Register A)
| Bit 7-6 | Bit 5-4 | Bit 3-2 | Bit 1-0 |
|---------|---------|---------|---------|
| COM0A1:0 | COM0B1:0 | - | WGM01:0 |

#### TCCR0B (Timer/Counter Control Register B)
| Bit 7 | Bit 6-4 | Bit 3 | Bit 2-0 |
|-------|---------|-------|---------|
| FOC0A | FOC0B | WGM02 | CS02:0 |

#### Valores de Prescaler (CS02:0)
| CS02 | CS01 | CS00 | Prescaler |
|------|------|------|-----------|
| 0 | 0 | 0 | No clock (Timer detenido) |
| 0 | 0 | 1 | 1 (sin prescaler) |
| 0 | 1 | 0 | 8 |
| 0 | 1 | 1 | 64 |
| 1 | 0 | 0 | 256 |
| 1 | 0 | 1 | 1024 |

### Anexo C: Recursos Adicionales

- **Datasheet ATmega328P:** [Microchip Official](https://www.microchip.com/en-us/product/ATmega328P)
- **AVR Libc Documentation:** [AVR Libc Reference](https://www.nongnu.org/avr-libc/)
- **GitHub Repository:** [Ejemplos ATmega328P](https://github.com/CARLOS-QL/ATMEGA328P_EJEMPLOS)

---

## Licencia

Este documento es de uso educativo y puede ser distribuido libremente con atribución al autor original.

---

**¿Tienes preguntas o mejoras?** Abre un *issue* o contribuye con un *pull request*.
