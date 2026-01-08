# DOCUMENTACIÓN 1: Instalación de IDEs y Drivers para ATmega328P

**Autor:** Luis David Barahona Valdivieso  
**Fecha:** 11/04/2025  
**Dispositivo:** Microcontrolador ATmega328P

---

## 📌 Índice
1. [Instalación de SW para manejar el ATmega328P](#1-instalación-de-sw-para-manejar-el-atmega328p)
   - [1.1. Drivers USBasp (Zadig)](#11-descargar-drivers-del-programador-usbasp-usando-el-sw-zadig)
   - [1.2. AVRDUDE](#12-instalar-avrdude)
   - [1.3. Microchip Studio](#13-instalar-microchip-studio-antes-atmel-studio)
   - [1.4. AVRDUDESS](#14-instalar-avrdudess)
   - [1.5. Proteus](#15-instalar-proteus-para-las-simulaciones)
2. [Anexos](#2-anexos)
   - [2.1. Diagrama de conexión](#21-anexo-1---diagrama-de-conexión-del-programador-usbasp-al-atmega328p)

---

## 1. Instalación de SW para manejar el ATmega328P

### 1.1. Descargar drivers del programador “USBasp” usando el SW Zadig

* **Paso 1:** Visitar [fischl.de/usbasp/](https://www.fischl.de/usbasp/) para información técnica.
* **Paso 2:** Descargar **Zadig** desde su [sitio oficial](https://zadig.akeo.ie/).
* **Paso 3:** Conectar el programador USBasp a la laptop.
* **Paso 4:** Ejecutar Zadig, seleccionar el dispositivo y hacer clic en **Install Driver**.

> **Nota:** Asegúrese de seleccionar el driver `libusb-win32` o el recomendado por la documentación de USBasp en Zadig.

### 1.2. Instalar AVRDUDE
Herramienta de consola para manipular la memoria ROM/EEPROM vía ISP.

1.  **Descarga:** Ir al [área de descarga de AVRDUDE](https://www.nongnu.org/avrdude/).
2.  **Ubicación:** Extraer en una ruta corta, por ejemplo:
    `C:\avrdude\`
3.  **Variables de Entorno (PATH):**
    * Clic derecho en **Este Equipo** -> Propiedades -> Configuración avanzada del sistema.
    * Variables de entorno -> Seleccionar **Path** -> Editar -> Nuevo.
    * Pegar la ruta: `C:\avrdude-6.3-mingw32` (o la que corresponda).
4.  **Verificación:** Abrir CMD y escribir:
    ```bash
    avrdude
    ```

### 1.3. Instalar Microchip Studio (antes Atmel Studio)

* **Instalación:** Descargar desde el [sitio de Microchip](https://www.microchip.com/en-us/tools-resources/develop/microchip-studio).
* **Arquitectura:** Seleccionar únicamente **AVR** durante el proceso para ahorrar espacio.
* **Configuración USBasp:** * Ir a `Tools` -> `External Tools`.
    * **Title:** `USBASP_prog`
    * **Command:** (Ruta al archivo avrdude.exe)
    * **Arguments:** `-c usbasp -p m328p -U flash:w:"$(ProjectDir)Debug\$(TargetName).hex":i`

### 1.4. Instalar AVRDUDESS
Interfaz gráfica (GUI) para AVRDUDE, ideal para configurar **Fuses**.

1.  **Descarga:** [Blog de Zak Kemble](https://blog.zakkemble.net/avrdudess-a-gui-for-avrdude/).
2.  **Configuración de Fusibles:**
    * Elegir MCU: `ATmega328P`.
    * Programador: `USBasp`.
    * *Importante:* Un bit programado en AVR se representa con un `0`.

### 1.5. Instalar Proteus para las simulaciones

1.  **Instalación:** Ejecutar el instalador de Proteus 8.13.
2.  **Librerías Arduino:** * Copiar la carpeta `Data`.
    * Pegar en la ruta raíz de instalación:
        `C:\Program Files (x86)\Labcenter Electronics\Proteus 8 Professional`

---

## 2. Anexos

### 2.1. Anexo 1 - Diagrama de conexión del programador USBasp al ATmega328P

Para programar el chip en protoboard, siga el siguiente esquema de pines (ISP):

| Pin USBasp | Pin ATmega328P |
| :--- | :--- |
| MOSI | 17 (PB3) |
| MISO | 18 (PB4) |
| SCK  | 19 (PB5) |
| RST  | 1 (PC6)  |
| VCC  | 7 (VCC)  |
| GND  | 8 (GND)  |

---

## 3. Otros
* Diseño de PCBs recomendado: **Altium Designer**.
* Simulación de circuitos analógicos/digitales: **Proteus**.
