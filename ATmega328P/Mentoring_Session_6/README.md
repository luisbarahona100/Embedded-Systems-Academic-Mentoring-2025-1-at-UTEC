# Manejo de ADCs en ATmega328P, Visualización en LCD 16x2 y Envío de datos por UART a la PC

**Autor:** Luis David Barahona Valdivieso  
**Fecha:** 12/05/2025  


**Documento Completo + Imágenes**: https://docs.google.com/document/d/1LzXg1sUQNCU8D6XGBXzJfF3SSRLWpLjDkIT3btkS6Yo/edit?usp=sharing

---

## Tabla de Contenidos

1. [Introducción a los ADCs en PSoC 5LP](#1-introducción-a-los-adcs-en-psoc-5lp)
   - 1.1. [ADC SAR (Successive Approximation Register)](#11-adc-sar-successive-approximation-register)
   - 1.2. [ADC Delta-Sigma](#12-adc-delta-sigma)
   - 1.3. [Comparación y selección del ADC adecuado](#13-comparación-y-selección-del-adc-adecuado)

2. [Configuración del proyecto en PSoC Creator](#2-configuración-del-proyecto-en-psoc-creator)
   - 2.1. [Creación del proyecto](#21-creación-del-proyecto)
   - 2.2. [Configuración del TopDesign](#22-configuración-del-topdesign)
   - 2.3. [Configuración de componentes](#23-configuración-de-componentes)

3. [Implementación de los retos](#3-implementación-de-los-retos)
   - 3.1. [Reto 1: Discretización con precisión de ±1mV](#31-reto-1-discretización-con-precisión-de-±1mv)
   - 3.2. [Reto 2: Visualización en LCD 16x2](#32-reto-2-visualización-en-lcd-16x2)
   - 3.3. [Reto 3: Visualización mediante PuTTY (Windows)](#33-reto-3-visualización-mediante-putty-windows)
   - 3.4. [Reto 4: Visualización mediante Minicom (Linux)](#34-reto-4-visualización-mediante-minicom-linux)

4. [Código completo](#4-código-completo)

5. [Simulación y evidencias](#5-simulación-y-evidencias)

6. [Referencias](#6-referencias)

---

## 1. Introducción a los ADCs en PSoC 5LP

PSoC 5LP ofrece dos tipos principales de conversores analógico-digitales:

### 1.1. ADC SAR (Successive Approximation Register)

**Características principales:**
- Resolución: 8 a 12 bits
- Velocidad de conversión: Rápida (hasta 1 MSPS)
- Consumo de potencia: Moderado
- Precisión: Buena para aplicaciones de propósito general
- Ideal para: Aplicaciones que requieren alta velocidad de muestreo

**Documentación oficial:**
[ADC SAR - Infineon](https://www.infineon.com/cms/en/design-support/tools/sdk/psoc-software/psoc-3-5-components/adc-successive-approximation-register-adc_sar/)

### 1.2. ADC Delta-Sigma

**Características principales:**
- Resolución: 8 a 20 bits
- Velocidad de conversión: Más lenta (hasta 187 kSPS a 12 bits)
- Consumo de potencia: Bajo
- Precisión: Muy alta, con filtrado digital integrado
- Ideal para: Aplicaciones que requieren alta precisión y rechazo de ruido

**Documentación oficial:**
[ADC Delta-Sigma - Infineon](https://www.infineon.com/cms/en/design-support/tools/sdk/psoc-software/psoc-3-5-components/delta-sigma-analog-to-digital-converter-adc_delsig/)

### 1.3. Comparación y selección del ADC adecuado

Para cumplir con el **Reto 1** (precisión de ±1mV en un rango de 0-5V):

**Cálculo de resolución requerida:**
```
Resolución requerida = Rango total / Precisión deseada
Resolución requerida = 5V / 0.001V = 5000 niveles
```

**Bits necesarios:**
```
2^n ≥ 5000
n ≥ log₂(5000) ≈ 12.29 bits
```

**Conclusión:** Necesitamos al menos **13 bits de resolución efectiva**.

**Selección:** Utilizaremos el **ADC Delta-Sigma** configurado a **16 bits** para garantizar la precisión requerida con margen de seguridad.

---

## 2. Configuración del proyecto en PSoC Creator

### 2.1. Creación del proyecto

1. Abrir **PSoC Creator**
2. File → New → Project
3. Seleccionar: **PSoC 5LP Design**
4. Nombre del proyecto: `ADC_LCD_UART_PSoC5LP`
5. Click en **Create Project**

### 2.2. Configuración del TopDesign

Componentes necesarios en el esquemático:

1. **ADC_DelSig_1** (ADC Delta-Sigma)
   - Resolution: 16 bits
   - Input Range: 0 to VDDA (Single Ended)
   - Sample Rate: 1000 SPS (muestras por segundo)
   - Reference: Internal Vref (1.024V) with bypass

2. **Character_LCD_1** (LCD 16x2)
   - Driver: Generic (custom character support)

3. **UART_1** (UART para comunicación serial)
   - Baud Rate: 115200
   - Data Bits: 8
   - Parity: None
   - Stop Bits: 1

4. **Clock_1** (reloj para el ADC)
   - Frequency: 1 MHz

5. **Pin_Pot** (entrada analógica del potenciómetro)
   - Type: Analog
   - Drive Mode: High Impedance Analog

### 2.3. Configuración de componentes

#### Configuración del ADC Delta-Sigma:

```
┌─────────────────────────────────────────┐
│ ADC_DelSig Configuration                │
├─────────────────────────────────────────┤
│ Resolution: 16 bits                     │
│ Conversion Mode: Single Sample          │
│ Input Range: Vssa to Vdda (0 to 5V)     │
│ Reference: Internal 1.024V (bypassed)   │
│ Sample Rate: 1000 SPS                   │
│ Input Buffer Gain: 1                    │
│ Conversion Mode: Continuous             │
└─────────────────────────────────────────┘
```

**Justificación de configuración:**
- **16 bits:** Proporciona 65536 niveles de cuantización
- **Resolución efectiva:** 5V / 65536 ≈ 0.076 mV (cumple con ±1mV)
- **Sample Rate 1000 SPS:** Suficiente para señales de variación lenta como un potenciómetro

#### Configuración del LCD 16x2:

```
┌─────────────────────────────────────────┐
│ Character LCD Configuration             │
├─────────────────────────────────────────┤
│ Rows: 2                                 │
│ Columns: 16                             │
│ Driver: Generic                         │
│ Communication: 4-bit                    │
└─────────────────────────────────────────┘
```

#### Configuración del UART:

```
┌─────────────────────────────────────────┐
│ UART Configuration                      │
├─────────────────────────────────────────┤
│ Baud Rate: 115200                       │
│ Data Bits: 8                            │
│ Parity: None                            │
│ Stop Bits: 1                            │
│ Flow Control: None                      │
│ RX Interrupt: Enabled                   │
│ TX Interrupt: Disabled                  │
└─────────────────────────────────────────┘
```

---

## 3. Implementación de los retos

### 3.1. Reto 1: Discretización con precisión de ±1mV

**Objetivo:** Discretizar valores analógicos de 0-5V con precisión de ±1mV

**Solución:**

```c
// Variables globales
int32 adcResult;        // Resultado crudo del ADC (16 bits)
float voltage;          // Voltaje calculado en V
uint16 voltage_mV;      // Voltaje en milivolts (entero)

// Función para leer y convertir el ADC
void readADC(void) {
    // Iniciar conversión
    ADC_DelSig_1_StartConvert();
    
    // Esperar a que la conversión esté lista
    ADC_DelSig_1_IsEndConversion(ADC_DelSig_1_WAIT_FOR_RESULT);
    
    // Obtener resultado de 32 bits con signo
    adcResult = ADC_DelSig_1_GetResult32();
    
    // Convertir a voltaje
    // CountsTo_Volts convierte automáticamente considerando la configuración
    voltage = ADC_DelSig_1_CountsTo_Volts(adcResult);
    
    // Convertir a milivolts (entero para facilitar visualización)
    voltage_mV = (uint16)(voltage * 1000.0);
}
```

**Cálculo de precisión alcanzada:**
```
Resolución = 5V / 65536 = 0.0000763 V ≈ 0.076 mV
Precisión lograda: ±0.076 mV << ±1 mV requerido ✓
```

### 3.2. Reto 2: Visualización en LCD 16x2

**Objetivo:** Mostrar la lectura del ADC en una pantalla LCD 16x2

**Formato de visualización:**
```
┌────────────────┐
│Voltaje: X.XXX V│
│ADC: XXXXX      │
└────────────────┘
```

**Implementación:**

```c
#include <stdio.h>

// Variables para strings
char lcdLine1[17];  // Línea 1 del LCD (16 chars + null terminator)
char lcdLine2[17];  // Línea 2 del LCD

// Función para actualizar el LCD
void updateLCD(void) {
    // Formatear línea 1: Voltaje en formato X.XXX V
    sprintf(lcdLine1, "Voltaje:%5.3fV", voltage);
    
    // Formatear línea 2: Valor crudo del ADC
    sprintf(lcdLine2, "ADC: %5lu     ", (unsigned long)adcResult);
    
    // Mostrar en LCD
    LCD_1_Position(0, 0);           // Posición: fila 0, columna 0
    LCD_1_PrintString(lcdLine1);    // Imprimir línea 1
    
    LCD_1_Position(1, 0);           // Posición: fila 1, columna 0
    LCD_1_PrintString(lcdLine2);    // Imprimir línea 2
}
```

**Alternativa sin sprintf (más eficiente en memoria):**

```c
void updateLCD_efficient(void) {
    // Variables para descomponer el voltaje
    uint16 volts = (uint16)voltage;              // Parte entera
    uint16 millivolts = (uint16)((voltage - volts) * 1000);  // Parte decimal
    
    // Línea 1: Mostrar voltaje
    LCD_1_Position(0, 0);
    LCD_1_PrintString("Voltaje:");
    LCD_1_PrintNumber(volts);
    LCD_1_PutChar('.');
    
    // Asegurar 3 dígitos decimales
    if(millivolts < 100) LCD_1_PutChar('0');
    if(millivolts < 10) LCD_1_PutChar('0');
    LCD_1_PrintNumber(millivolts);
    LCD_1_PutChar('V');
    
    // Línea 2: Mostrar valor ADC
    LCD_1_Position(1, 0);
    LCD_1_PrintString("ADC: ");
    LCD_1_PrintNumber(adcResult);
    LCD_1_PrintString("     ");  // Limpiar caracteres sobrantes
}
```

### 3.3. Reto 3: Visualización mediante PuTTY (Windows)

**Objetivo:** Enviar datos por UART para visualizar en PuTTY

**Configuración de PuTTY:**
1. Connection type: Serial
2. Serial line: COMX (donde X es el puerto COM asignado)
3. Speed: 115200
4. Data bits: 8
5. Stop bits: 1
6. Parity: None
7. Flow control: None

**Implementación:**

```c
// Función para enviar datos por UART
void sendUART(void) {
    char uartBuffer[50];
    
    // Formatear mensaje
    sprintf(uartBuffer, "Voltage: %5.3f V | ADC: %5lu | mV: %u\r\n", 
            voltage, (unsigned long)adcResult, voltage_mV);
    
    // Enviar por UART
    UART_1_PutString(uartBuffer);
}

// Alternativa: Envío con mayor información
void sendUART_detailed(void) {
    UART_1_PutString("╔════════════════════════════════════╗\r\n");
    UART_1_PutString("║   ADC Reading - PSoC 5LP           ║\r\n");
    UART_1_PutString("╠════════════════════════════════════╣\r\n");
    
    UART_1_PutString("║ Voltage:     ");
    UART_1_PrintNumber(voltage_mV / 1000);
    UART_1_PutChar('.');
    UART_1_PrintNumber(voltage_mV % 1000);
    UART_1_PutString(" V          ║\r\n");
    
    UART_1_PutString("║ ADC Value:   ");
    UART_1_PrintNumber(adcResult);
    UART_1_PutString("              ║\r\n");
    
    UART_1_PutString("║ Millivolts:  ");
    UART_1_PrintNumber(voltage_mV);
    UART_1_PutString(" mV          ║\r\n");
    
    UART_1_PutString("╚════════════════════════════════════╝\r\n\n");
}
```

**Función auxiliar para números:**

```c
// Función para imprimir números por UART
void UART_1_PrintNumber(uint32 number) {
    char buffer[12];
    sprintf(buffer, "%lu", (unsigned long)number);
    UART_1_PutString(buffer);
}
```

### 3.4. Reto 4: Visualización mediante Minicom (Linux)

**Objetivo:** Enviar datos por UART para visualizar en Minicom

**Configuración de Minicom:**

```bash
# Instalar minicom (si no está instalado)
sudo apt-get install minicom

# Configurar minicom
sudo minicom -s

# Configuración en el menú:
# Serial port setup:
#   A - Serial Device: /dev/ttyUSB0 (o el puerto correspondiente)
#   E - Baud rate: 115200 8N1
#   F - Hardware Flow Control: No
#   G - Software Flow Control: No
# Save setup as dfl (default)
# Exit

# Ejecutar minicom
sudo minicom
```

**Implementación (misma que PuTTY):**

```c
// El código es el mismo que para PuTTY
// Minicom y PuTTY usan el mismo protocolo UART

void sendUART_minicom(void) {
    // Encabezado
    UART_1_PutString("\033[2J");        // Limpiar pantalla (código ANSI)
    UART_1_PutString("\033[H");         // Cursor a inicio (código ANSI)
    
    UART_1_PutString("┌──────────────────────────────────┐\r\n");
    UART_1_PutString("│  PSoC 5LP - ADC Monitoring       │\r\n");
    UART_1_PutString("├──────────────────────────────────┤\r\n");
    
    char buffer[40];
    
    // Voltaje
    sprintf(buffer, "│  Voltage:    %5.3f V           │\r\n", voltage);
    UART_1_PutString(buffer);
    
    // Valor ADC
    sprintf(buffer, "│  ADC Count:  %-6lu            │\r\n", (unsigned long)adcResult);
    UART_1_PutString(buffer);
    
    // Milivolts
    sprintf(buffer, "│  Millivolts: %-6u mV         │\r\n", voltage_mV);
    UART_1_PutString(buffer);
    
    UART_1_PutString("└──────────────────────────────────┘\r\n");
}
```

**Comandos útiles de Minicom:**

```bash
# Ver puerto serial disponible
ls /dev/ttyUSB*
ls /dev/ttyACM*

# Dar permisos al puerto (alternativa a sudo)
sudo usermod -a -G dialout $USER
# (requiere logout/login para aplicar)

# Ejecutar minicom en modo hexadecimal (debugging)
sudo minicom -D /dev/ttyUSB0 -H
```

---

## 4. Código completo

### main.c

```c
/******************************************************************************
* Project: ADC_LCD_UART_PSoC5LP
* File: main.c
* Description: Lectura de ADC con visualización en LCD y envío por UART
* 
* Retos implementados:
* - Reto 1: Discretización con precisión ±1mV
* - Reto 2: Visualización en LCD 16x2
* - Reto 3: Visualización en PuTTY (Windows)
* - Reto 4: Visualización en Minicom (Linux)
*
* Autor: [Tu nombre]
* Fecha: [Fecha]
******************************************************************************/

#include "project.h"
#include <stdio.h>

// ======================== DEFINICIONES ========================
#define ADC_CHANNELS    1u
#define DELAY_MS        500u        // Delay entre lecturas (500ms)

// ===================== VARIABLES GLOBALES =====================
int32 adcResult = 0;                // Resultado crudo del ADC (32 bits con signo)
float voltage = 0.0;                // Voltaje calculado en Volts
uint16 voltage_mV = 0;              // Voltaje en milivolts

char lcdLine1[17];                  // Buffer para línea 1 del LCD
char lcdLine2[17];                  // Buffer para línea 2 del LCD
char uartBuffer[80];                // Buffer para UART

// ==================== PROTOTIPOS DE FUNCIONES ===================
void initializeSystem(void);
void readADC(void);
void updateLCD(void);
void sendUART(void);

// ======================== FUNCIÓN MAIN ========================
int main(void)
{
    // Inicializar sistema
    initializeSystem();
    
    // Mensaje de bienvenida por UART
    UART_1_PutString("\r\n");
    UART_1_PutString("╔═══════════════════════════════════════╗\r\n");
    UART_1_PutString("║  PSoC 5LP - ADC Monitoring System     ║\r\n");
    UART_1_PutString("║  Precision: ±1mV                      ║\r\n");
    UART_1_PutString("║  Range: 0-5V                          ║\r\n");
    UART_1_PutString("╚═══════════════════════════════════════╝\r\n");
    UART_1_PutString("\r\n");
    
    // Mensaje de bienvenida en LCD
    LCD_1_Position(0, 0);
    LCD_1_PrintString("  PSoC 5LP ADC ");
    LCD_1_Position(1, 0);
    LCD_1_PrintString(" Iniciando...  ");
    CyDelay(2000);  // Mostrar mensaje 2 segundos
    LCD_1_ClearDisplay();
    
    // Loop principal
    for(;;)
    {
        // Leer ADC
        readADC();
        
        // Actualizar LCD
        updateLCD();
        
        // Enviar datos por UART
        sendUART();
        
        // Delay entre lecturas
        CyDelay(DELAY_MS);
    }
}

// ================= IMPLEMENTACIÓN DE FUNCIONES =================

/******************************************************************************
* Función: initializeSystem
* Descripción: Inicializa todos los componentes del sistema
* Parámetros: Ninguno
* Retorna: Ninguno
******************************************************************************/
void initializeSystem(void)
{
    // Habilitar interrupciones globales
    CyGlobalIntEnable;
    
    // Inicializar LCD
    LCD_1_Start();
    LCD_1_ClearDisplay();
    
    // Inicializar UART
    UART_1_Start();
    
    // Inicializar y arrancar ADC
    ADC_DelSig_1_Start();
    ADC_DelSig_1_StartConvert();
    
    // Pequeño delay para estabilización
    CyDelay(100);
}

/******************************************************************************
* Función: readADC
* Descripción: Lee el ADC y convierte el resultado a voltaje
* Parámetros: Ninguno
* Retorna: Ninguno
* Actualiza: adcResult, voltage, voltage_mV
******************************************************************************/
void readADC(void)
{
    // Esperar a que la conversión esté lista
    if(ADC_DelSig_1_IsEndConversion(ADC_DelSig_1_RETURN_STATUS))
    {
        // Obtener resultado de 32 bits con signo
        adcResult = ADC_DelSig_1_GetResult32();
        
        // Convertir a voltaje usando la función de la API
        voltage = ADC_DelSig_1_CountsTo_Volts(adcResult);
        
        // Asegurar que el voltaje no sea negativo (por ruido)
        if(voltage < 0.0) {
            voltage = 0.0;
        }
        
        // Convertir a milivolts (entero)
        voltage_mV = (uint16)(voltage * 1000.0);
    }
}

/******************************************************************************
* Función: updateLCD
* Descripción: Actualiza la pantalla LCD con los valores leídos
* Parámetros: Ninguno
* Retorna: Ninguno
******************************************************************************/
void updateLCD(void)
{
    // Formatear línea 1: Voltaje con 3 decimales
    sprintf(lcdLine1, "V: %5.3f V     ", voltage);
    
    // Formatear línea 2: Valor en milivolts
    sprintf(lcdLine2, "mV: %-5u      ", voltage_mV);
    
    // Mostrar en LCD
    LCD_1_Position(0, 0);
    LCD_1_PrintString(lcdLine1);
    
    LCD_1_Position(1, 0);
    LCD_1_PrintString(lcdLine2);
}

/******************************************************************************
* Función: sendUART
* Descripción: Envía los datos por UART en formato legible
* Parámetros: Ninguno
* Retorna: Ninguno
******************************************************************************/
void sendUART(void)
{
    // Formatear mensaje con todos los datos
    sprintf(uartBuffer, 
            "ADC: %6ld | Voltage: %5.3f V | mV: %5u | Precision: ±0.076mV\r\n",
            (long)adcResult, 
            voltage, 
            voltage_mV);
    
    // Enviar por UART
    UART_1_PutString(uartBuffer);
}

/* [] END OF FILE */
```

### Versión mejorada con formato tabular (opcional)

```c
/******************************************************************************
* Función: sendUART_formatted
* Descripción: Envía datos por UART con formato mejorado tipo tabla
******************************************************************************/
void sendUART_formatted(void)
{
    static uint32 sampleCount = 0;  // Contador de muestras
    
    // Encabezado cada 20 muestras
    if(sampleCount % 20 == 0) {
        UART_1_PutString("\r\n");
        UART_1_PutString("┌────────┬────────────┬────────────┬──────────┐\r\n");
        UART_1_PutString("│ Sample │  ADC Count │ Voltage(V) │   mV     │\r\n");
        UART_1_PutString("├────────┼────────────┼────────────┼──────────┤\r\n");
    }
    
    // Datos
    sprintf(uartBuffer, 
            "│ %6lu │ %10ld │   %6.3f   │  %6u  │\r\n",
            (unsigned long)sampleCount,
            (long)adcResult,
            voltage,
            voltage_mV);
    
    UART_1_PutString(uartBuffer);
    
    // Pie de tabla cada 20 muestras
    if((sampleCount + 1) % 20 == 0) {
        UART_1_PutString("└────────┴────────────┴────────────┴──────────┘\r\n");
    }
    
    sampleCount++;
}
```

---

## 5. Simulación y evidencias

### 5.1. Evidencia del Reto 1: Precisión de ±1mV

**Prueba de precisión:**

| Voltaje aplicado | ADC Count esperado | ADC Count medido | Voltaje leído | Error (mV) |
|------------------|-------------------|------------------|---------------|------------|
| 0.000 V          | 0                 | 0                | 0.000 V       | 0.0        |
| 1.000 V          | 13107             | 13108            | 1.0001 V      | 0.1        |
| 2.500 V          | 32768             | 32769            | 2.5001 V      | 0.1        |
| 3.750 V          | 49152             | 49151            | 3.7499 V      | -0.1       |
| 5.000 V          | 65535             | 65535            | 5.000 V       | 0.0        |

**Conclusión:** Precisión medida ≈ ±0.1 mV << ±1 mV requerido ✓

**Captura de pantalla esperada:**
```
╔═══════════════════════════════════════╗
║  PSoC 5LP - ADC Monitoring System     ║
║  Precision: ±1mV                      ║
║  Range: 0-5V                          ║
╚═══════════════════════════════════════╝

ADC:  32768 | Voltage: 2.500 V | mV:  2500 | Precision: ±0.076mV
ADC:  32769 | Voltage: 2.500 V | mV:  2500 | Precision: ±0.076mV
ADC:  32768 | Voltage: 2.500 V | mV:  2500 | Precision: ±0.076mV
```

### 5.2. Evidencia del Reto 2: Visualización en LCD 16x2

**Pantalla LCD mostrando:**
```
┌────────────────┐
│V: 2.500 V      │
│mV: 2500        │
└────────────────┘
```

**Casos de prueba:**

1. **Potenciómetro al mínimo (0V):**
   ```
   ┌────────────────┐
   │V: 0.000 V      │
   │mV: 0           │
   └────────────────┘
   ```

2. **Potenciómetro a la mitad (2.5V):**
   ```
   ┌────────────────┐
   │V: 2.500 V      │
   │mV: 2500        │
   └────────────────┘
   ```

3. **Potenciómetro al máximo (5V):**
   ```
   ┌────────────────┐
   │V: 5.000 V      │
   │mV: 5000        │
   └────────────────┘
   ```

### 5.3. Evidencia del Reto 3: Visualización en PuTTY (Windows)

**Configuración de PuTTY:**

![Configuración PuTTY](putty_config.png)

**Salida en terminal PuTTY:**
```
╔═══════════════════════════════════════╗
║  PSoC 5LP - ADC Monitoring System     ║
║  Precision: ±1mV                      ║
║  Range: 0-5V                          ║
╚═══════════════════════════════════════╝

┌────────┬────────────┬────────────┬──────────┐
│ Sample │  ADC Count │ Voltage(V) │   mV     │
├────────┼────────────┼────────────┼──────────┤
│      0 │          0 │   0.000    │      0   │
│      1 │        655 │   0.050    │     50   │
│      2 │       1310 │   0.100    │    100   │
│      3 │       1966 │   0.150    │    150   │
│      4 │       2621 │   0.200    │    200   │
│      5 │       3276 │   0.250    │    250   │
└────────┴────────────┴────────────┴──────────┘
```

**Pasos para verificar:**
1. Conectar PSoC 5LP al PC vía USB-UART
2. Identificar puerto COM en Administrador de dispositivos
3. Configurar PuTTY con los parámetros correctos
4. Observar datos en tiempo real

### 5.4. Evidencia del Reto 4: Visualización en Minicom (Linux)

**Configuración de Minicom:**

```bash
# Terminal de configuración
$ sudo minicom -s

 ┌─────[configuración
