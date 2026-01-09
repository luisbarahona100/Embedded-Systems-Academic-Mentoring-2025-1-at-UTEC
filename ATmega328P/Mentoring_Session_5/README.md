# Manejo del Display de 7 Segmentos

**Autor:** Luis David Barahona Valdivieso  
**Fecha:** 12/05/2025  
**GitHub Mentoría 5:** [https://github.com/luisbarahona100/Mentorias/tree/main/Mentoría%205](https://github.com/luisbarahona100/Mentorias/tree/main/Mentor%C3%ADa%205)

**Documento Completo + Imágenes**: https://docs.google.com/document/d/1LzXg1sUQNCU8D6XGBXzJfF3SSRLWpLjDkIT3btkS6Yo/edit?usp=sharing
---

## Tabla de Contenidos

1. [Reto 3](#1-reto-3)
   - [1.1. Planteamiento](#11-planteamiento)
   - [1.2. Identificación de requerimientos](#12-identificación-de-requerimientos)
   - [1.3. Funcionamiento de los componentes usados](#13-funcionamiento-de-los-componentes-usados)
2. [CASO 1: Display de 7 segmentos Ánodo Común con Transistores NPN ❌](#2-caso-1-display-de-7-segmentos-ánodo-común-con-transistores-npn-)
3. [CASO 2: Display de 7 segmentos Ánodo Común con Transistores PNP ✅](#3-caso-2-display-de-7-segmentos-ánodo-común-con-transistores-pnp-)
4. [CASO 3: Display de 7 segmentos Cátodo Común con Transistores NPN ✅](#4-caso-3-display-de-7-segmentos-cátodo-común-con-transistores-npn-)
5. [CASO 4: Display de 7 segmentos Cátodo Común con Transistores PNP ❌](#5-caso-4-display-de-7-segmentos-cátodo-común-con-transistores-pnp-)

---

## 1. Reto 3

### 1.1. Planteamiento

Implementar un programa que realice la suma y resta de una cuenta que empieza en 0:

- Con una de las interrupciones debe **sumar** el valor de los Switch (SW3-SW0) de la tarjeta y la cuenta general: `Cuenta + Switches`
- Cuando se pulse la otra interrupción debe **restar** el valor de los Switch (SW3-SW0) a la cuenta general: `Cuenta - Switches`
- Configurar la interrupción **INT0** con **flanco de bajada**
- Configurar la interrupción **INT1** con **flanco de subida**

**Requisitos de visualización:**

- El resultado de la operación suma/resta se visualizará en el **display de 7 segmentos** conectado al puerto B con sus debidas resistencias para no dañar los leds del display
- Si el resultado es **negativo**, se debe visualizar en el display de 7 segmentos el resultado de la operación con el **signo menos "-"**
- Cuando el resultado es **cero**, en paralelo al resultado del display, encender el **Led7 o Led6** de la tarjeta de prototipos para indicar valor 0

### 1.2. Identificación de requerimientos

#### INPUTS

| Componente | Pin | Configuración |
|------------|-----|---------------|
| **SW3:SW0** | PC3:PC0 | Pull down externo |
| **Pulsador 1** | INT0 → PD2 | Pull down externo y Flanco de bajada |
| **Pulsador 2** | INT1 → PD3 | Pull up interno y Flanco de subida |

#### OUTPUTS

| Componente | Pin |
|------------|-----|
| **Millar** | PB5 |
| **Centena** | PB4 |
| **Decena** | PB1 |
| **Unidad** | PB0 |
| **DP** | PD7 |
| **A** | PD6 |
| **B** | PD5 |
| **C** | PD4 |
| **D** | PB3 |
| **E** | PB2 |
| **F** | PD1 |
| **G** | PD0 |
| **LED6** | PC4 |
| **LED7** | PC5 |

#### VARIABLES

```
Cuenta = 0 = f(INT0, INT1, SW3:SW0)
```

#### Preguntas de análisis

**¿Si me piden que el pulsador 1 (INT0) detecte una interrupción por flanco de bajada, dicho pulsador debería tener una configuración física en pull down o pull up?**

**Respuesta:** Pull down

---

**¿Si me piden que el pulsador 2 (INT1) detecte una interrupción por flanco de subida, dicho pulsador debería tener una configuración física en pull down o pull up?**

**Respuesta:** Pull down

---

### 1.3. Funcionamiento de los componentes usados

#### 1.3.1. Display de 7 segmentos de tipo Ánodo Común

[📺 Video explicativo](https://drive.google.com/file/d/1W187QHCy5Nfb9dV2UwGBkHdCD86ffsM-/view?usp=drive_link)

**Orden de dígitos:** De izquierda a derecha: Millar, Centena, Decena, Unidad

**Características:**

- **Habilitar un dígito** significa conectar a **"1" (Vcc)** el ánodo común del dígito deseado
  - Ejemplo: Si quieres habilitar el dígito DIG1, el pin 12 del display tiene que conectarse a "1" (Vcc)
- **Escribir un número** en el display significa mandar un arreglo de 8 valores binarios a los pines 11, 7, 4, 2, 1, 10, 5, 3
  - Los leds se **prenden** mandando **"ceros"** en dicho arreglo
  - Los leds se **apagan** mandando **"unos"** en dicho arreglo

#### 1.3.2. Display de 7 segmentos de tipo Cátodo Común

[📺 Video explicativo](https://drive.google.com/file/d/1TxFLivVVnvjbLKmFzvjr18_TALr4NqfS/view?usp=drive_link)

**Orden de dígitos:** De izquierda a derecha: Millar, Centena, Decena, Unidad

**Características:**

- **Habilitar un dígito** significa conectar a **"0" (GND)** el cátodo común del dígito deseado
  - Ejemplo: Si quieres habilitar el dígito DIG1, el pin 12 del display tiene que conectarse a "0" (GND)
- **Escribir un número** en el display significa mandar un arreglo de 8 valores binarios a los pines 11, 7, 4, 2, 1, 10, 5, 3
  - Los leds se **prenden** mandando **"unos"** en dicho arreglo
  - Los leds se **apagan** mandando **"ceros"** en dicho arreglo

#### 1.3.3. Transistor BJT de tipo NPN

**Funcionamiento:**

- Al mandar un **"1"** desde el µC a la base del transistor NPN → **saturamos el transistor** → la carga es alimentada o activada
  - Si la carga es un dígito del display, esta sería activada
- Al mandar un **"0"** desde el µC a la base del transistor NPN → ocurre lo contrario (corte)

#### 1.3.4. Transistor BJT de tipo PNP

**Funcionamiento:**

- Al mandar un **"0"** desde el µC a la base del transistor PNP → **saturamos el transistor** → la carga es alimentada o activada
  - Si la carga es un dígito del display, esta sería activada
- Al mandar un **"1"** desde el µC a la base del transistor PNP → ocurre lo contrario (corte)

#### 1.3.5. Posicionamiento incorrecto de la carga (dígito del display)

⚠️ **Advertencia importante sobre el posicionamiento de la carga:**

- **Transistor NPN:** El emisor debe ir conectado a **GND**
- **Transistor PNP:** El emisor debe ir conectado a **VCC**

Esto es fundamental para que el estado corte/saturación se desarrolle de forma adecuada.

**Fuente:** [MadPCB - Switching Transistor](https://madpcb.com/glossary/switching-transistor/#:~:text=Un%20transistor%20puede%20operar%20en%20tres%20modos:,regi%C3%B3n%20de%20saturaci%C3%B3n%20y%20regi%C3%B3n%20de%20corte.&text=La%20definici%C3%B3n%20de%20%22regi%C3%B3n%20de%20saturaci%C3%B3n%22%20o,=%20M%C3%A1ximo%20y%20VB%20%3E%200%2C7%20V)

---

## 2. CASO 1: Display de 7 segmentos Ánodo Común con Transistores NPN ❌

### 2.1. Esquemático

*(Esquemático del circuito con display de ánodo común y transistores NPN)*

### 2.2. Error

❌ **Esta configuración NO es válida**

**Razón:** El emisor del transistor NPN debería ir conectado a **GND**, para que el estado corte/saturación se desarrolle de forma adecuada. Más detalles en la sección 1.3.5.

---

## 3. CASO 2: Display de 7 segmentos Ánodo Común con Transistores PNP ✅

### 3.1. Esquemático

#### EJEMPLO CON ATmega328P

*(Esquemático del circuito con ATmega328P)*

#### EJEMPLO CON Arduino Nano

*(Esquemático del circuito con Arduino Nano)*

#### EJEMPLO Con PIC16F628A

*(Esquemático del circuito con PIC16F628A)*

### 3.2. Lógica de control

#### 3.2.1. Activación de segmentos

Se activa un segmento determinado escribiendo un **"0"** desde el µC.

El display de 7 segmentos exige por lo menos **8 pines** que controlen los 8 leds (7 segmentos + el punto). Podrías asignar todos los bits del puerto D, ¿Pero qué tal si el bit3 y bit2 están siendo usados para otra tarea? En ese caso tenemos que pedirle prestado 2 bits a otro puerto.

El registro **R16** muestra un ejemplo del formato de codificación pactado. El formato u orden podría ser otro, sin ningún problema, pero recuerda que este formato tiene influencia directa sobre el orden de conexión entre el µC y el Display.

**Distribución de pines:**

| bit7 | bit6 | bit5 | bit4 | bit3 | bit2 | bit1 | bit0 |
|------|------|------|------|------|------|------|------|
| **R16** | DP | A | B | C | D | E | F | G |
| **PORTB** | x | x | x | x | D | E | x | x |
| **PORTD** | DP | A | B | C | x | x | F | G |

**Tabla de codificación - ÁNODO COMÚN:**

| Número | DP | A | B | C | D | E | F | G | Hex |
|--------|----|----|----|----|----|----|----|----|-----|
| **0** | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0x81 |
| **1** | 1 | 1 | 0 | 0 | 1 | 1 | 1 | 1 | 0xCF |
| **2** | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 | 0x92 |
| **3** | 1 | 0 | 0 | 0 | 0 | 1 | 1 | 0 | 0x86 |
| **4** | 1 | 1 | 0 | 0 | 1 | 1 | 0 | 0 | 0xCC |
| **5** | 1 | 0 | 1 | 0 | 0 | 1 | 0 | 0 | 0xA4 |
| **6** | 1 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0xA0 |
| **7** | 1 | 0 | 0 | 0 | 1 | 1 | 1 | 1 | 0x8F |
| **8** | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0x80 |
| **9** | 1 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0x84 |
| **-** | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 0 | 0xFE |

#### 3.2.2. Activar Dígitos

Un dígito (carga) es activado cuando se manda un **"0"** desde el µC a la base del transistor PNP. Al mandar un **"1"** este se apaga o no se activa.

### 3.3. Diagrama de flujo

```
INICIO
  ↓
Configuración de puertos
Configuración de interrupciones
Cuenta = 0
  ↓
LOOP PRINCIPAL
  ↓
Llamar rutina DISPLAY
  ↓
Volver al loop
  ↓
───────────────────────
ISR INT0 (Flanco bajada)
  ↓
Cuenta = Cuenta + Switch
  ↓
RETI
───────────────────────
ISR INT1 (Flanco subida)
  ↓
Cuenta = Cuenta - Switch
  ↓
RETI
───────────────────────
RUTINA DISPLAY
  ↓
Separar dígitos (unidad, decena, centena, millar)
  ↓
Convertir a código 7 segmentos (DEC2DISPLAY)
  ↓
Multiplexar dígitos
  ↓
RET
```

### 3.4. Código en C

*(Referencia al código en C en el repositorio)*

### 3.5. Código AVR Ensamblador

[AVR_Display7SegmentosAC_PNP/main.asm](https://github.com/luisbarahona100/Mentorias/blob/main/Mentor%C3%ADa%205/AVR_Display7SegmentosAC_PNP/AVR_Display7SegmentosAC_PNP/main.asm)

### 3.6. Simulación

#### CASO 1 - Se presiona y se suelta una vez el pulsador 1 (INT0) cuando Cuenta = 0 y Switch = 1

**Resultado:** Se genera adecuadamente `(cuenta + switch) = (0 + 1) = 1 = 0xCF`

#### CASO 2 - Se presiona y se suelta una vez el pulsador 2 (INT1) cuando Cuenta = 0 y Switch = 1

**Resultado:** El resultado de operar `(cuenta - switch) = -1 = 0xFE`. Es correcto el resultado codificado.

---

## 4. CASO 3: Display de 7 segmentos Cátodo Común con Transistores NPN ✅

### 4.1. Esquemático

#### EJEMPLO CON ATmega328P

*(Esquemático del circuito con ATmega328P)*

#### EJEMPLO CON Arduino Nano

*(Esquemático del circuito con Arduino Nano)*

#### EJEMPLO CON PIC16F84

*(Esquemático del circuito con PIC16F84)*

### 4.2. Lógica de control

#### 4.2.1. Activación de segmentos

Se activa un segmento determinado escribiendo un **"1"** desde el µC.

El display de 7 segmentos exige por lo menos **8 pines** que controlen los 8 leds (7 segmentos + el punto). Podrían asignar todos los bits del puerto D, ¿Pero qué tal si el bit3 y bit2 están siendo usados para otra tarea? En ese caso tenemos que pedirle prestado 2 bits a otro puerto.

El registro **R16** muestra un ejemplo del formato de codificación pactado. El formato u orden podría ser otro, sin ningún problema, pero recuerda que este formato tiene influencia directa sobre el orden de conexión entre el µC y el Display.

**Distribución de pines:**

| bit7 | bit6 | bit5 | bit4 | bit3 | bit2 | bit1 | bit0 |
|------|------|------|------|------|------|------|------|
| **R16** | DP | A | B | C | D | E | F | G |
| **PORTB** | x | x | x | x | D | E | x | x |
| **PORTD** | DP | A | B | C | x | x | F | G |

**Tabla de codificación - CÁTODO COMÚN:**

| Número | DP | A | B | C | D | E | F | G | Hex |
|--------|----|----|----|----|----|----|----|----|-----|
| **0** | 0 | 1 | 1 | 1 | 1 | 1 | 1 | 0 | 0x7E |
| **1** | 0 | 0 | 1 | 1 | 0 | 0 | 0 | 0 | 0x30 |
| **2** | 0 | 1 | 1 | 0 | 1 | 1 | 0 | 1 | 0x6D |
| **3** | 0 | 1 | 1 | 1 | 1 | 0 | 0 | 1 | 0x79 |
| **4** | 0 | 0 | 1 | 1 | 0 | 0 | 1 | 1 | 0x33 |
| **5** | 0 | 1 | 0 | 1 | 1 | 0 | 1 | 1 | 0x5B |
| **6** | 0 | 1 | 0 | 1 | 1 | 1 | 1 | 1 | 0x5F |
| **7** | 0 | 1 | 1 | 1 | 0 | 0 | 0 | 0 | 0x70 |
| **8** | 0 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 0x7F |
| **9** | 0 | 1 | 1 | 1 | 1 | 0 | 1 | 1 | 0x7B |
| **–** | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0x01 |

#### 4.2.2. Activar Dígitos

Un dígito (carga) es activado cuando se manda un **"1"** desde el µC a la base del transistor NPN. Al mandar un **"0"** este se apaga o no se activa.

### 4.3. Diagrama de flujo

Es el mismo diagrama que usa el CASO 2 (sección 3.3). Lo único que cambia es la **codificación de las salidas** de la rutina **DEC2DISPLAY**. Ajustarla usando la tabla de codificación del display de tipo **Cátodo Común**.

### 4.4. Código en C

*(Referencia al código en C en el repositorio)*

### 4.5. Código en AVR Ensamblador

[AVR_Display7SegmentosCC_NPN/main.asm](https://github.com/luisbarahona100/Mentorias/blob/main/Mentor%C3%ADa%205/AVR_Display7SegmentosCC_NPN/AVR_Display7SegmentosCC_NPN/main.asm)

### 4.6. Simulación

*(Resultados de simulación similares al CASO 2, con la diferencia en la codificación)*

---

## 5. CASO 4: Display de 7 segmentos Cátodo Común con Transistores PNP ❌

### 5.1. Esquemático

*(Esquemático del circuito con display de cátodo común y transistores PNP)*

### 5.2. Error

❌ **Esta configuración NO es válida**

**Razón:** El emisor del transistor PNP debería ir conectado a **VCC**, para que el estado corte/saturación se desarrolle de forma adecuada. Más detalles en la sección 1.3.5.

---

## Resumen de Configuraciones Válidas

| Tipo de Display | Tipo de Transistor | ¿Válida? | Observaciones |
|-----------------|-------------------|----------|---------------|
| Ánodo Común | NPN | ❌ | Emisor debe ir a GND |
| Ánodo Común | PNP | ✅ | Configuración correcta |
| Cátodo Común | NPN | ✅ | Configuración correcta |
| Cátodo Común | PNP | ❌ | Emisor debe ir a VCC |

---

## Recursos Adicionales

- [Repositorio completo de la Mentoría 5](https://github.com/luisbarahona100/Mentorias/tree/main/Mentor%C3%ADa%205)
- Video explicativo - Display Ánodo Común
- Video explicativo - Display Cátodo Común
- Documentación de transistores BJT
- Microchip Studio
- Proteus Design Suite

---

## Conclusiones

1. La correcta selección del tipo de transistor (NPN o PNP) depende del tipo de display (Ánodo o Cátodo Común)
2. El posicionamiento del emisor del transistor es crítico para el funcionamiento adecuado del circuito
3. La codificación de los segmentos es inversa entre displays de Ánodo Común y Cátodo Común
4. El uso de interrupciones permite una respuesta rápida a eventos externos
5. La técnica de multiplexación permite controlar múltiples dígitos con un número limitado de pines

---

**© 2025 Luis David Barahona Valdivieso**
