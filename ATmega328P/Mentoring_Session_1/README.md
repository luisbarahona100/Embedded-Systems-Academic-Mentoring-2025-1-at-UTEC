# DOCUMENTACIÓN 1: Instalación de IDEs y DRIVERS para el manejo adecuado del ATmega328P

**Autor:** Luis David Barahona Valdivieso  
**Fecha:** 11/04/2025

---

## 📌 ÍNDICE
1. [Instalación de SW para manejar el ATmega328P](#1-instalación-de-sw-para-manejar-el-atmega328p)
   - [1.1. Drivers USBasp con Zadig](#11-descargar-drivers-del-programador-usbasp-usando-el-sw-zadig)
   - [1.2. Instalar AVRDUDE](#12-instalar-avrdude)
   - [1.3. Instalar Microchip Studio](#13-instalar-microchip-studio-antes-atmel-studio)
   - [1.4. Instalar AVRDUDESS](#14-instalar-avrdudess)
   - [1.5. Instalar Proteus](#15-instalar-proteus-para-las-simulaciones)
2. [Anexos](#2-anexos)
   - [2.1. Diagrama de conexión](#21-anexo-1---diagrama-de-conexión-del-programador-usbasp-al-atmega328p)
3. [Otros](#3-otros)

---

## 1. Instalación de SW para manejar el ATmega328P

### 1.1. Descargar drivers del programador “USBasp” usando el SW Zadig
**Pasos para la instalación:**
1. **PASO 1:** Visitar [fischl.de/usbasp/](https://www.fischl.de/usbasp/).
2. **PASO 2:** En la sección de drivers, descargar **Zadig** desde [zadig.akeo.ie](https://zadig.akeo.ie/).
3. **PASO 3:** Ejecutar Zadig.
4. **PASO 4:** Conectar el programador USBasp a la laptop.
5. **PASO 5:** Seleccionar el dispositivo y hacer clic en **Install Driver**.

*Documentación oficial:* [USBasp Driver Docs](https://www.fischl.de/usbasp/)

### 1.2. Instalar AVRDUDE
Herramienta para manipular la memoria ROM o EEPROM de microcontroladores AVR usando ISP.

**Pasos para descargar y configurar:**
1. **PASO 1:** Ir a [nongnu.org/avrdude/](https://www.nongnu.org/avrdude/).
2. **PASO 2:** Clic en **“download area”**.
3. **PASO 3:** Descargar la última versión disponible.
4. **PASO 4:** Extraer y guardar en la ruta:
   `C:\Users\luisdavidbarahona\Documents\barahona_2025_marzo\installers\Installers_ISE\avrdude-6.3-mingw32`
5. **PASO 5: Configuración de Variables de Entorno (PATH):**
   * Abrir Explorador de archivos -> Clic derecho en **Este equipo (This PC)** -> **Propiedades**.
   * Ir a **Advanced System Settings** -> **Environment variables**.
   * En Variables del sistema, buscar **PATH** -> **Edit** -> **New**.
   * Pegar la ruta mencionada en el Paso 4.
   * Aceptar todos los cambios.
   * *Referencia en video:* [Configurar AVRDUDE en el Path](https://www.youtube.com/watch?v=B7KQ3W4RxcA)
6. **PASO 6:** Abrir CMD (`Win + R`, escribir `cmd`) y teclear `avrdude`. Debe mostrar la versión y descripción.

### 1.3. Instalar Microchip Studio (antes Atmel Studio)
**Pasos para la instalación en Windows 10:**
1. **PASO 1:** Descargar desde [Microchip Studio](https://www.microchip.com/en-us/tools-resources/develop/microchip-studio).
2. **PASO 2:** Ejecutar instalador.
   * **Ruta de instalación:** `C:\Program Files (x86)\Atmel\Studio\`
   * **Arquitectura:** Seleccionar únicamente **AVR**.
   * **Datos de licencia/sistema:** - XC8 Path: `C:\Program Files\Microchip\xc8\v2.36`
     - Host ID: `0a0027000005`
3. **PASO 3: Configurar el programador USBasp:**
   * Abrir Microchip Studio -> `Tools` -> `External Tools`.
   * Agregar nueva herramienta llamada `USBASP_prog`.
   * Una vez configurado, aparecerá en el menú **Tools**.
  
### Configuración del Programador USBasp en Microchip Studio (Autoría: Christopher Eduardo Briceño Carbajal)

Para integrar el programador **USBasp** como una herramienta externa, utilice la siguiente estructura de comando base:

`avrdude -p [uC] -c [interfazProgramacion] -P [PuertoCOM] -b [BaudRate] -U [memoria]:[operacion]:"[file.hex]":i`

#### Parámetros de Configuración (External Tools)
Debe completar los campos en el menú `Tools` -> `External Tools` de la siguiente manera:

| Campo | Valor Sugerido |
| :--- | :--- |
| **Command** | `D:\AVR_DUDE\avrdude.exe` |
| **Arguments** | `-c USBasp -p atmega328p -P usb -B 8.0 -U flash:w:"$(OutDir)Debug\$(TargetName).hex":i` |
| **Initial directory** | `$(ProjectDir)` |

> [!IMPORTANT]
> **Nota sobre Microcontroladores Nuevos:**
> Si el ATmega328P es nuevo, es estrictamente necesario programar los **fuses** (fusibles) del microcontrolador. Para realizar esta tarea, se debe descargar y utilizar el software **AVRDUDESS** o **Khazama**.


### 1.4. Instalar AVRDUDESS
Utilizado principalmente para programar fusibles en chips nuevos.

**Pasos para instalar v2.17 v 7.3:**
1. **PASO 1:** Ir al [Blog de Zak Kemble](https://blog.zakkemble.net/avrdudess-a-gui-for-avrdude/).
2. **PASO 2:** Clic en "DOWNLOAD HERE", redirigirá a GitHub.
3. **PASO 3:** Entrar en **Releases** y buscar la versión **v2.17**.
4. **PASO 4:** Instalar en la ruta: `C:\Program Files (x86)\AVRDUDESS`.
5. **PASO 5:** Conectar USBasp al ATmega328P mediante adaptador JTAG/USB. (Ver Anexo 1).
7. **PASO 6: Configuración Inicial:**
   * Elegir **ATmega328P**.
   * Configurar fusibles en **Bit Selector**.
   * **Configuración de reloj (1MHz):** Asegurar que `CLKDIV8` esté programado (valor 0).
   * **Regla de oro:** Fusible programado = 0 | Fusible NO programado = 1.
8. **PASO 7:** Programar fusibles.

### 1.5. Instalar Proteus para las simulaciones
1. **PASO 1:** Referencia de instalación: [Video Tutorial](https://www.youtube.com/watch?v=22dPDU_sQjw).
2. **PASO 2:** Descargar archivo: [Proteus 8.13 Mediafire](https://www.mediafire.com/file/9c14vzjuvsx38oz/Proteus_8.13.rar/file).
3. **PASO 4:** Ejecutar instalador **Proteus 8.13 SP0 Pro**.
   * **Ruta:** `C:\Program Files (x86)\Labcenter Electronics\Proteus 8 Professional`
4. **PASO 5: Librerías de Arduino:**
   * Copiar carpeta `Data` de las librerías.
   * Clic derecho en acceso directo de Proteus -> **Abrir ubicación del archivo**.
   * Pegar la carpeta `Data` dentro de `Proteus 8 Professional`.
5. **PASO 6:** Probar ejecución.

---

## 2. ANEXOS

### 2.1. Anexo 1 - Diagrama de conexión del programador USBasp al ATmega328P
A continuación, se detalla la conexión para programación ISP en protoboard.



| Pin USBasp | Pin ATmega328P | Nombre del Pin |
| :--- | :--- | :--- |
| MOSI | 17 | PB3 |
| MISO | 18 | PB4 |
| SCK  | 19 | PB5 |
| RESET| 1  | PC6 |
| VCC  | 7  | VCC |
| GND  | 8  | GND |
<img width="449" height="204" alt="image" src="https://github.com/user-attachments/assets/30451054-10f7-40e0-b423-eb3d78662044" />

<img width="517" height="324" alt="image" src="https://github.com/user-attachments/assets/1e9168c8-2eb0-48d8-b286-7fba2f29022a" />

---

## 3. OTROS
* **Altium Designer:** Herramienta recomendada para el diseño profesional de PCBs.
