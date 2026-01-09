# MANEJO DEl ADC SAR del ATmega328P

**Autor:** Luis David Barahona Valdivieso  
**Fecha:** 10.06.2025

**Documento Completo + Imágenes:** https://docs.google.com/document/d/10z6ESZenzZYtXlVCkWsLMAYJYBVS4xL6o0t_hr-dr90/edit?tab=t.0

---

## Índice

1. [Configuración de un ADC SAR en ATmega328P con el Timer/Counter0 (Ts=100ms)](#1-configuración-de-un-adc-sar-en-atmega328p-con-el-timercounter0-ts100ms)
   - 1.1. [Descripción general del SAR ADC del ATmega328P](#11-descripción-general-del-sar-adc-del-atmega328p)
   - 1.2. [Código C Ejemplo](#12-código-c-ejemplo)
   - 1.3. [Configuración de registros elegida](#13-configuración-de-registros-elegida)
   - 1.4. [Simulación / Evidencias](#14-simulación--evidencias)
2. [Modulación manual de DutyCycle mediante un potenciómetro (ADC10Bit SAR + PWM) - ATmega328p](#2-modulación-manual-de-dutycycle-mediante-un-potenciómetro-adc10bit-sar--pwm---atmega328p)
   - 2.1. [Código](#21-código)
   - 2.2. [Resumen de configuración de registros y justificación de cálculos](#22-resumen-de-configuración-de-registros-y-justificación-de-cálculos)
   - 2.3. [Simulación y evidencias](#23-simulación-y-evidencias)
3. [ADCs en PSoC 5LP, Visualización en una pantalla LCD 16x2, Envío de datos por UART a la PC](#3-adcs-en-psoc-5lp-visualización-en-una-pantalla-lcd-16x2-envío-de-datos-por-uart-a-la-pc)

---

## 1. Configuración de un ADC SAR en ATmega328P con el Timer/Counter0 (Ts=100ms)

### 1.1. Descripción general del SAR ADC del ATmega328P

El ATmega328P cuenta con un **ADC SAR (Successive Approximation Register)** de **10 bits** con las siguientes características:

#### Características principales:
- **Resolución:** 10 bits → Puede digitalizar y diferenciar **2^10 = 1024** valores analógicos
- **Rango de periodo de muestreo:** 65 - 260 μs (puede modificarse usando timer/counters)
- **Frecuencia de muestreo máxima:** 15K SPS (15,000 muestras por segundo) o 15 kHz
- **Canales de entrada:**
  - 6 canales multiplexados de un solo extremo con referencia a GND
  - 2 canales adicionales multiplexados de un solo extremo
- **Rango de voltaje de entrada:** 0 a Vcc (5V)
- **Voltaje de referencia:** Seleccionable de 1.1V o Vcc
- **Modos de operación:**
  - Free running mode
  - Single conversion mode
- **Características adicionales:**
  - Interrupción en conversión ADC completada
  - Cancelador de ruido en modo de suspensión

#### Fórmula de conversión (válida para resolución de 10 bits):

```
ADC_Value = (Vin × 1024) / Vref
```

Donde:
- `ADC_Value`: Valor digital de 0 a 1023
- `Vin`: Voltaje de entrada analógica
- `Vref`: Voltaje de referencia (típicamente 5V)

#### Modo de muestreo seleccionado:

**Timer/Counter0 Compare Match A:**  
Cuando `TCNT0 == OCR0A` → capturar una muestra

---

### 1.2. Código C Ejemplo

#### Enunciado del ejercicio:
Se pide prender un LED si la lectura del potenciómetro es mayor a 4V. El ADC SAR de 10 bits tiene que muestrear la señal proveniente del potenciómetro cada 100ms. Justificar todos los cálculos.

#### Pasos para implementar:

**Paso 1:** Crear un nuevo proyecto
- Elegir el compilador: **GCC C Executable Project**
- Elegir microcontrolador: **ATmega328P**

**Paso 2:** Agregar el siguiente código

[Ver código completo en GitHub](https://github.com/luisbarahona100/Mentorias/blob/main/Mentor%C3%ADa%207/ADC_Code_C/ADC_Code_C/main.c)

```c
#include <avr/io.h>
#include <avr/interrupt.h>

#define LED_PIN PD7

void ADC_Init(void);
void Timer0_Init(void);

int main(void) {
    // Configurar LED como salida
    DDRD |= (1 << LED_PIN);
    
    // Inicializar ADC y Timer0
    ADC_Init();
    Timer0_Init();
    
    // Habilitar interrupciones globales
    sei();
    
    while(1) {
        // El programa principal queda en espera
        // La conversión ADC se dispara automáticamente cada 100ms
    }
}

void ADC_Init(void) {
    // Seleccionar canal ADC0 (PC0)
    ADMUX = (1 << REFS0);  // Referencia AVCC, canal ADC0
    
    // Habilitar ADC, habilitar interrupción, prescaler 128
    // Auto Trigger habilitado
    ADCSRA = (1 << ADEN) | (1 << ADIE) | (1 << ADATE) | 
             (1 << ADPS2) | (1 << ADPS1) | (1 << ADPS0);
    
    // Trigger source: Timer/Counter0 Compare Match A
    ADCSRB = (1 << ADTS1) | (1 << ADTS0);
}

void Timer0_Init(void) {
    // Modo CTC (Clear Timer on Compare)
    TCCR0A = (1 << WGM01);
    
    // Prescaler 1024
    TCCR0B = (1 << CS02) | (1 << CS00);
    
    // Configurar valor de comparación para 100ms
    // OCR0A = (F_CPU * tiempo) / (prescaler) - 1
    // OCR0A = (1MHz * 0.1s) / 1024 - 1 = 96.6 ≈ 97
    OCR0A = 97;
    
    // Habilitar interrupción por comparación A (opcional)
    TIMSK0 = (1 << OCIE0A);
}

// ISR del ADC
ISR(ADC_vect) {
    uint16_t adc_value = ADC;
    
    // Calcular voltaje: V = (ADC_value * 5.0) / 1024
    // Para 4V: ADC_value = (4 * 1024) / 5 = 819.2 ≈ 819
    
    if(adc_value > 819) {
        PORTD |= (1 << LED_PIN);   // Encender LED
    } else {
        PORTD &= ~(1 << LED_PIN);  // Apagar LED
    }
}

// ISR del Timer0 (opcional, para debug)
ISR(TIMER0_COMPA_vect) {
    // El ADC se dispara automáticamente
}
```

---

### 1.3. Configuración de registros elegida

#### Cálculos para el Timer0:

**Objetivo:** Generar una interrupción cada 100ms para disparar el ADC

**Datos:**
- Frecuencia del reloj (F_CPU): 1 MHz
- Prescaler: 1024
- Tiempo deseado: 100 ms = 0.1 s

**Fórmula:**
```
OCR0A = (F_CPU × tiempo) / Prescaler - 1
OCR0A = (1,000,000 × 0.1) / 1024 - 1
OCR0A = 100,000 / 1024 - 1
OCR0A = 97.66 ≈ 97
```

**Tiempo real obtenido:**
```
T_real = (OCR0A + 1) × Prescaler / F_CPU
T_real = (97 + 1) × 1024 / 1,000,000
T_real = 100.352 ms ≈ 100 ms
```

#### Configuración de registros:

| Registro | Bits configurados | Función |
|----------|-------------------|---------|
| **ADMUX** | REFS0 = 1 | Referencia AVCC (5V) |
| | MUX3:0 = 0000 | Canal ADC0 (PC0) |
| **ADCSRA** | ADEN = 1 | Habilitar ADC |
| | ADIE = 1 | Habilitar interrupción ADC |
| | ADATE = 1 | Auto Trigger habilitado |
| | ADPS2:0 = 111 | Prescaler 128 (ADC clock = 7.8 kHz) |
| **ADCSRB** | ADTS2:0 = 011 | Trigger: Timer0 Compare Match A |
| **TCCR0A** | WGM01 = 1 | Modo CTC |
| **TCCR0B** | CS02 = 1, CS00 = 1 | Prescaler 1024 |
| **OCR0A** | - | Valor = 97 (para 100ms) |

---

### 1.4. Simulación / Evidencias

#### Paso 1: Crear un nuevo proyecto en Proteus

#### Paso 2: Replicar el siguiente esquemático

**Componentes necesarios:**
- ATmega328P
- Potenciómetro (10kΩ)
- LED con resistencia limitadora (220Ω - 1kΩ)
- Capacitor de desacople en AREF (100nF - 1μF)
- Fuente de alimentación (5V)

**Conexiones importantes:**
- **AVCC:** Conectar a VCC (5V)
  - *Nota:* AVCC no debe diferir más de ±0.3V de VCC
- **AREF:** Conectar capacitor de desacople a GND para mejor rendimiento de ruido
- **PC0 (ADC0):** Conectar al cursor del potenciómetro
- **PD7:** Conectar al LED

#### Paso 3: Configurar los fusibles del ATmega328P

**Configuración para reloj de 1MHz:**

El fusible **CLKDIV8** tiene que estar **programado (0)** para que el reloj de operación del ATmega328P sea 1MHz.

- **Oscilador interno:** 8 MHz
- **Divisor CLKDIV8:** ÷8
- **Frecuencia resultante:** 1 MHz

**Cargar el archivo .hex:**
- Ruta: `ADC_Code_C\ADC_Code_C\Debug\ADC_Code_C.hex`

#### Paso 4: Generar evidencias

**Criterio de funcionamiento:**
- Si `Analog Signal < 4V` → LED D1 **APAGADO**
- Si `Analog Signal > 4V` → LED D1 **ENCENDIDO**

**CASO 1: Analog Signal < 4V → LED apagado ✓**
- Potenciómetro configurado a 3.5V
- LED D1 permanece apagado
- ✅ Cumple con la especificación

**CASO 2: Analog Signal > 4V → LED encendido ✓**
- Potenciómetro configurado a 4.5V
- LED D1 se enciende
- ✅ Cumple con la especificación

**Cálculo del umbral ADC:**
```
ADC_threshold = (4V × 1024) / 5V = 819.2 ≈ 819
```

---

## 2. Modulación manual de DutyCycle mediante un potenciómetro (ADC10Bit SAR + PWM) - ATmega328p

### Descripción del proyecto:

Este proyecto combina dos periféricos del ATmega328P:

1. **Timer/Counter1 (16 bits):** Generar una señal PWM de periodo 2ms por el pin PB1 (OC1A)
2. **ADC SAR 10 bits:** Leer el valor del potenciómetro cada 100ms (disparado por Timer/Counter0)
3. **Timer/Counter0 (8 bits):** Generar el periodo de muestreo de 100ms

**Objetivo:** El duty cycle de la señal PWM se modula según el valor del potenciómetro.

---

### 2.1. Código

[Ver código completo en GitHub](https://github.com/luisbarahona100/Mentorias/blob/main/Mentor%C3%ADa%207/ADC_PWM_ATmega328p/ADC_PWM_ATmega328p/main.c)

```c
#include <avr/io.h>
#include <avr/interrupt.h>

void PWM_Init(void);
void ADC_Init(void);
void Timer0_Init(void);

int main(void) {
    // Inicializar periféricos
    PWM_Init();
    ADC_Init();
    Timer0_Init();
    
    // Habilitar interrupciones globales
    sei();
    
    while(1) {
        // El duty cycle se actualiza automáticamente en la ISR del ADC
    }
}

void PWM_Init(void) {
    // Configurar PB1 (OC1A) como salida
    DDRB |= (1 << PB1);
    
    // Modo Fast PWM de 8 bits (WGM13:0 = 0101)
    // TOP = 0xFF (255)
    TCCR1A = (1 << COM1A1) | (1 << WGM10);  // Non-inverting mode, Fast PWM 8-bit
    TCCR1B = (1 << WGM12) | (1 << CS11);     // Fast PWM 8-bit, Prescaler 8
    
    // Inicializar duty cycle a 0%
    OCR1A = 0;
}

void ADC_Init(void) {
    // Referencia AVCC, canal ADC0
    ADMUX = (1 << REFS0);
    
    // Habilitar ADC, habilitar interrupción, Auto Trigger, Prescaler 128
    ADCSRA = (1 << ADEN) | (1 << ADIE) | (1 << ADATE) | 
             (1 << ADPS2) | (1 << ADPS1) | (1 << ADPS0);
    
    // Trigger source: Timer/Counter0 Compare Match A
    ADCSRB = (1 << ADTS1) | (1 << ADTS0);
}

void Timer0_Init(void) {
    // Modo CTC
    TCCR0A = (1 << WGM01);
    
    // Prescaler 1024
    TCCR0B = (1 << CS02) | (1 << CS00);
    
    // Para 100ms: OCR0A = 97
    OCR0A = 97;
}

// ISR del ADC - Actualizar duty cycle
ISR(ADC_vect) {
    uint16_t adc_value = ADC;  // Leer valor ADC (0-1023)
    
    // Mapear ADC (0-1023) a PWM (0-255)
    // OCR1A = (adc_value * 255) / 1023
    // Simplificado: OCR1A = adc_value >> 2
    OCR1A = adc_value >> 2;  // División por 4 (aproximadamente /4.01)
}
```

---

### 2.2. Resumen de configuración de registros y justificación de cálculos

#### 2.2.1. Configuración del Timer/Counter1 (16 bits) como Fast PWM de 8 bits

**Objetivo:** Generar una señal PWM con periodo de aproximadamente 2ms

**Parámetros:**
- **Modo:** Fast PWM de 8 bits
- **TOP:** 255 (0xFF)
- **Prescaler:** 8
- **Pin de salida:** PB1 (OC1A)
- **Modo de salida:** Non-inverting

**Cálculos:**

```
f_PWM = F_CPU / (N × (1 + TOP))
f_PWM = 1,000,000 / (8 × (1 + 255))
f_PWM = 1,000,000 / (8 × 256)
f_PWM = 1,000,000 / 2,048
f_PWM = 488.28 Hz ≈ 490 Hz
```

```
T_PWM = 1 / f_PWM
T_PWM = 1 / 488.28
T_PWM = 2.048 ms ≈ 2 ms
```

**Configuración de registros:**

| Registro | Bits | Valor | Función |
|----------|------|-------|---------|
| **TCCR1A** | COM1A1 | 1 | Non-inverting mode (clear on match) |
| | COM1A0 | 0 | |
| | WGM11 | 0 | Fast PWM 8-bit |
| | WGM10 | 1 | (WGM13:0 = 0101) |
| **TCCR1B** | WGM13 | 0 | Fast PWM 8-bit |
| | WGM12 | 1 | (WGM13:0 = 0101) |
| | CS12:10 | 010 | Prescaler = 8 |
| **OCR1A** | - | 0-255 | Duty cycle (actualizado por ADC) |

**Fórmula del Duty Cycle:**

```
Duty Cycle (%) = (OCR1A / 255) × 100%
```

---

#### 2.2.2. Configuración del Timer/Counter0 para interrupción cada 100ms

**Objetivo:** Generar un trigger cada 100ms para disparar automáticamente el ADC

**Parámetros:**
- **Modo:** CTC (Clear Timer on Compare)
- **Prescaler:** 1024
- **OCR0A:** 97

**Cálculo (ya realizado anteriormente):**

```
OCR0A = (F_CPU × T_deseado) / Prescaler - 1
OCR0A = (1,000,000 × 0.1) / 1024 - 1
OCR0A = 97
```

**Configuración de registros:**

| Registro | Bits | Función |
|----------|------|---------|
| **TCCR0A** | WGM01 = 1 | Modo CTC |
| **TCCR0B** | CS02 = 1, CS00 = 1 | Prescaler 1024 |
| **OCR0A** | 97 | Comparación para 100ms |

**Aprovechamiento de la interrupción:**  
Cada vez que `TCNT0 == OCR0A` (cada 100ms), el ADC toma **una sola muestra** automáticamente gracias al modo Auto Trigger configurado.

---

#### 2.2.3. Configuración del ADC SAR 10 bits en Single Mode (con Auto Trigger)

**Características:**
- **Modo:** Auto Trigger (disparo automático)
- **Fuente de trigger:** Timer0 Compare Match A
- **Referencia:** AVCC (5V)
- **Canal:** ADC0 (PC0)
- **Prescaler:** 128 (ADC clock ≈ 7.8 kHz)

**Configuración de registros:**

| Registro | Bits | Función |
|----------|------|---------|
| **ADMUX** | REFS0 = 1 | Referencia AVCC |
| | MUX3:0 = 0000 | Canal ADC0 |
| **ADCSRA** | ADEN = 1 | Habilitar ADC |
| | ADSC = 0 | (Se activa automáticamente por trigger) |
| | ADATE = 1 | **Auto Trigger Enable** |
| | ADIE = 1 | Interrupción habilitada |
| | ADPS2:0 = 111 | Prescaler 128 |
| **ADCSRB** | ADTS2:0 = 011 | Trigger: Timer0 Compare Match A |

**Nota importante:**  
Se toma **una muestra cada vez** que el Timer0 genera el match (cada 100ms). El bit ADSC no se pone manualmente en "1" porque el modo Auto Trigger lo hace automáticamente.

**Mapeo ADC → PWM:**

```
// Valor ADC: 0-1023 (10 bits)
// Valor PWM: 0-255 (8 bits)

OCR1A = ADC_value >> 2  // División por 4
// O alternativamente:
OCR1A = (ADC_value * 255) / 1023
```

---

### 2.3. Simulación y evidencias

#### Configuración del esquemático en Proteus:
- ATmega328P con fusibles configurados (CLKDIV8 = 0)
- Potenciómetro 10kΩ conectado a PC0 (ADC0)
- LED conectado a PB1 (OC1A) con resistencia limitadora
- Osciloscopio conectado a PB1 para medir la señal PWM

---

#### 2.3.1. CASO 1: Potenciómetro en 1.25V → Duty Cycle = 25%

**Cálculos teóricos:**

```
ADC_value = (1.25V × 1024) / 5V = 256

OCR1A = 256 >> 2 = 64

Duty Cycle = (64 / 255) × 100% = 25.1%
```

**Medición en osciloscopio:**
- T_high ≈ 0.5 ms
- T_low ≈ 1.5 ms
- T_total ≈ 2.0 ms
- **Duty Cycle medido ≈ 25%** ✅

---

#### 2.3.2. CASO 2: Potenciómetro en 2.5V → Duty Cycle = 50%

**Cálculos teóricos:**

```
ADC_value = (2.5V × 1024) / 5V = 512

OCR1A = 512 >> 2 = 128

Duty Cycle = (128 / 255) × 100% = 50.2%
```

**Medición en osciloscopio:**
- T_high ≈ 1.0 ms
- T_low ≈ 1.0 ms
- T_total ≈ 2.0 ms
- **Duty Cycle medido ≈ 50%** ✅

---

#### 2.3.3. CASO 3: Potenciómetro en 5V → Duty Cycle = 100%

**Cálculos teóricos:**

```
ADC_value = (5V × 1024) / 5V = 1023

OCR1A = 1023 >> 2 = 255

Duty Cycle = (255 / 255) × 100% = 100%
```

**Medición en osciloscopio:**
- T_high ≈ 2.0 ms
- T_low ≈ 0 ms
- T_total ≈ 2.0 ms
- **Duty Cycle medido ≈ 100%** ✅

---

## 3. ADCs en PSoC 5LP, Visualización en pantalla LCD 16x2, Envío de datos por UART a la PC

### 3.1. Retos

#### Reto 1: Configuración del ADC
Configurar el ADC Delta-Sigma del PSoC 5LP para leer una señal analógica con la mayor resolución posible.

#### Reto 2: Visualización en LCD
Mostrar el valor del ADC y el voltaje correspondiente en una pantalla LCD 16x2 en tiempo real.

#### Reto 3: Comunicación UART
Enviar los datos del ADC por UART a la PC cada 500ms para monitoreo en una terminal serial.

#### Reto 4: Formato de datos
Los datos enviados por UART deben tener el formato:
```
ADC: [valor] | Voltaje: [voltaje]V
```

---

### 3.2. Solución en lenguaje C

```c
#include "project.h"
#include <stdio.h>

#define VREF 5.0        // Voltaje de referencia en V
#define ADC_MAX 65535   // Valor máximo para ADC de 16 bits

char lcd_buffer[16];
char uart_buffer[50];

int main(void) {
    CyGlobalIntEnable; // Habilitar interrupciones globales
    
    // Inicializar componentes
    ADC_Start();
    LCD_Start();
    UART_Start();
    
    // Iniciar conversión ADC
    ADC_StartConvert();
    
    LCD_ClearDisplay();
    LCD_Position(0, 0);
    LCD_PrintString("ADC Monitor");
    CyDelay(1000);
    
    uint16_t adc_value;
    float voltage;
    
    while(1) {
        // Esperar a que la conversión esté lista
        if(ADC_IsEndConversion(ADC_WAIT_FOR_RESULT)) {
            adc_value = ADC_GetResult16();
            
            // Calcular voltaje
            voltage = (adc_value * VREF) / ADC_MAX;
            
            // Mostrar en LCD
            LCD_ClearDisplay();
            LCD_Position(0, 0);
            sprintf(lcd_buffer, "ADC: %u", adc_value);
            LCD_PrintString(lcd_buffer);
            
            LCD_Position(1, 0);
            sprintf(lcd_buffer, "V: %.3fV", voltage);
            LCD_PrintString(lcd_buffer);
            
            // Enviar por UART
            sprintf(uart_buffer, "ADC: %u | Voltaje: %.3fV\r\n", 
                    adc_value, voltage);
            UART_PutString(uart_buffer);
            
            CyDelay(500); // Esperar 500ms
        }
    }
}
```

---

### 3.3. Simulación o verificación del cumplimiento de los retos

#### 3.3.1. Evidencia del reto 1
- ✅ ADC Delta-Sigma configurado en modo de 16 bits
- ✅ Referencia de voltaje: VREF = 5.0V
- ✅ Modo de conversión continua habilitado

#### 3.3.2. Evidencia del reto 2
- ✅ LCD muestra el valor ADC en la primera línea
- ✅ LCD muestra el voltaje calculado en la segunda línea
- ✅ Actualización en tiempo real cada 500ms

**Ejemplo de visualización en LCD:**
```
ADC: 32768
V: 2.500V
```

#### 3.3.3. Evidencia del reto 3
- ✅ Datos enviados por UART cada 500ms
- ✅ Baudrate configurado: 9600 bps (o según especificación)
- ✅ Formato ASCII legible en terminal serial

**Ejemplo de salida en terminal:**
```
ADC: 0 | Voltaje: 0.000V
ADC: 16384 | Voltaje: 1.250V
ADC: 32768 | Voltaje: 2.500V
ADC: 49152 | Voltaje: 3.750V
ADC: 65535 | Voltaje: 5.000V
```

#### 3.3.4. Evidencia del reto 4
- ✅ Formato cumple con la especificación:
  ```
  ADC: [valor] | Voltaje: [voltaje]V
  ```
- ✅ Precisión de 3 decimales para el voltaje
- ✅ Separadores y unidades correctamente incluidos

---

## Conclusiones

Este documento cubre tres implementaciones fundamentales del uso de ADCs en microcontroladores:

1. **ATmega328P - ADC básico:** Configuración de ADC SAR de 10 bits con muestreo periódico controlado por timer, ideal para aplicaciones de monitoreo simple.

2. **ATmega328P - ADC + PWM:** Integración de ADC con generación de PWM para control de duty cycle, aplicable en control de motores, iluminación LED y otros actuadores.

3. **PSoC 5LP - Sistema completo:** Implementación de un sistema de adquisición de datos con visualización local (LCD) y remota (UART), común en instrumentación y sistemas embebidos.

### Conceptos clave aprendidos:
- Configuración de registros de ADC y Timers
- Sincronización entre periféricos usando Auto Trigger
- Mapeo de valores entre diferentes resoluciones
- Comunicación de datos y visualización
- Cálculo de parámetros temporales en sistemas embebidos

---

**Recursos adicionales:**
- [Datasheet ATmega328P](https://ww1.microchip.com/downloads/en/DeviceDoc/Atmel-7810-Automotive-Microcontrollers-ATmega328P_Datasheet.pdf)
- [PSoC 5LP Datasheet](https://www.infineon.com/dgdl/Infineon-CY8C58LP_Family_Datasheet_Programmable_System-on-Chip_(PSoC)-DataSheet-v16_00-EN.pdf?fileId=8ac78c8c7d0d8da4017d0ee7d03a70b1)

---

*Documento generado para fines educativos - Mentoría de Sistemas Embebidos*
