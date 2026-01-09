# 📡 Comunicación Serial PSoC-PC con Gráficas en Tiempo Real

[![PSoC Creator](https://img.shields.io/badge/PSoC_Creator-4.4-blue.svg)](https://www.cypress.com/products/psoc-creator-integrated-design-environment-ide)
[![Python](https://img.shields.io/badge/Python-3.x-green.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

> **Autor:** Luis David Barahona Valdivieso  
> **Fecha:** 08.07.2025

> **Documento Completo + Imágenes:** https://docs.google.com/document/d/140sGo1cNi-e_6_IxycE8Ba23KTE9SigqHvjHngmGAv4/edit?usp=drive_link

---

## 📋 Tabla de Contenidos

- [Resumen](#-resumen)
- [Características](#-características)
- [Requisitos](#-requisitos)
- [Ejemplo 1: Lectura con PuTTY](#-ejemplo-1-lectura-de-datos-analógicos-con-putty)
- [Ejemplo 2: Visualización con Python](#-ejemplo-2-interfaz-gráfica-con-python)
- [Frecuencia de Muestreo](#-frecuencia-de-muestreo)
- [Conversión ADC a Voltaje](#-conversión-adc-a-voltaje)
- [Solución de Problemas](#-solución-de-problemas)
- [Contribuciones](#-contribuciones)

---

## 🎯 Resumen

Este proyecto implementa un sistema completo de adquisición y visualización de datos analógicos utilizando:

- **PSoC 5LP (CY8C5888LTI-LP097)** como dispositivo de adquisición
- **ADC Delta-Sigma** en modo streaming/free running
- **Comunicación UART** sobre USB para transferencia de datos
- **Python + Tkinter** para interfaz gráfica robusta en tiempo real
- **Matplotlib** para visualización de datos

### Funcionalidades principales:

✅ Lectura continua de señales analógicas (0-5V)  
✅ Transmisión serial a PC vía UART  
✅ Visualización en tiempo real con múltiples modos de gráfica  
✅ Conversión de voltaje a distancia (sensor Sharp GP2Y0A41SK0F)  
✅ Configuración flexible de parámetros seriales  

---

## ⚡ Características

### Hardware
- **Microcontrolador:** PSoC 5LP (CY8C5888LTI-LP097)
- **ADC:** Delta-Sigma de 12 bits
- **Comunicación:** UART a 115200 baudios
- **Sensores compatibles:** Potenciómetro, Sharp GP2Y0A41SK0F

### Software
- **Firmware:** PSoC Creator 4.4 (C)
- **PC:** Python 3.x con librerías:
  - `pyserial` - Comunicación serial
  - `matplotlib` - Gráficas
  - `tkinter` - Interfaz gráfica

---

## 🛠️ Requisitos

### Hardware
- PSoC 5LP Development Kit
- Cable USB
- Sensor analógico (potenciómetro o Sharp IR)
- Fuente de alimentación 5V

### Software

**PSoC Creator 4.4:**
```bash
# Descargar desde:
https://www.cypress.com/products/psoc-creator-integrated-design-environment-ide
```

**Python 3.x y dependencias:**
```bash
# Crear ambiente virtual
python -m venv GUI_env

# Activar ambiente virtual
# Windows:
GUI_env\Scripts\activate
# Linux/Mac:
source GUI_env/bin/activate

# Instalar dependencias
pip install pyserial matplotlib
```

---

## 🔧 Ejemplo 1: Lectura de Datos Analógicos con PuTTY

### Paso 1: Configuración del PSoC Creator

#### 1.1 Crear nuevo proyecto
- **Device:** CY8C5888LTI-LP097
- **Template:** Empty PSoC5 Design

#### 1.2 Diseño esquemático (TopDesign.cysch)

**Bloques necesarios:**

| Bloque | Configuración |
|--------|---------------|
| **ADC_DelSig_1** | - Resolución: 12 bits<br>- Input Range: Vssa to Vdda (0-5V)<br>- Conversion Mode: Single Sample<br>- Sample Mode: Free Running |
| **UART_1** | - Baud Rate: 115200<br>- Data Bits: 8<br>- Parity: None<br>- Stop Bits: 1 |

#### 1.3 Configuración de pines (cydwr)
```
P0[3] → ADC_DelSig_1 (analog input)
P12[6] → UART_1_TX
P12[7] → UART_1_RX
```

#### 1.4 Habilitar soporte para `sprintf` con flotantes

**Build Settings → ARM GCC → Linker → Command Line:**
```
Custom Flags: -u _printf_float
```

### Paso 2: Código del Firmware

**main.c:**
```c
#include <project.h>
#include <stdio.h>

char buffer[32]; // Buffer para mensajes UART

int main(void)
{
    CyGlobalIntEnable; // Habilitar interrupciones globales

    // Inicializar ADC
    ADC_DelSig_1_Start();
    ADC_DelSig_1_StartConvert();

    // Inicializar UART
    UART_1_Start();
    UART_1_PutString("UART funcionando\r\n");

    for(;;)
    {
        // Esperar fin de conversión
        if (ADC_DelSig_1_IsEndConversion(ADC_DelSig_1_RETURN_STATUS))
        {
            // Leer valor del ADC (0-4095)
            int16 adcValue = ADC_DelSig_1_GetResult16();

            // Convertir a voltaje (0-5V)
            float voltaje = (float)adcValue * 5.0f / 4095.0f;

            // Separar parte entera y decimal
            int volt_entero = (int)voltaje;
            int volt_decimal = (int)((voltaje - volt_entero) * 100);

            // Formatear y enviar por UART
            sprintf(buffer, "VOLTAJE: %d.%02d V\r\n", volt_entero, volt_decimal);
            UART_1_PutString(buffer);

            CyDelay(200); // Periodo de muestreo: 200ms → 5Hz
        }
    }
}
```

### Paso 3: Verificación con PuTTY

1. **Compilar y programar** el PSoC
2. **Identificar puerto COM** (Administrador de dispositivos → Puertos COM)
3. **Configurar PuTTY:**
   - Connection type: `Serial`
   - Serial line: `COM5` (ajustar según tu sistema)
   - Speed: `115200`
4. **Verificar salida:**
   ```
   UART funcionando
   VOLTAJE: 2.34 V
   VOLTAJE: 2.36 V
   VOLTAJE: 2.33 V
   ...
   ```

---

## 📊 Ejemplo 2: Interfaz Gráfica con Python

### Paso 1: Modificar Firmware para Sensor Sharp

**main.c (con sensor de distancia):**
```c
#include <project.h>
#include <stdio.h>
#include <math.h>

char buffer[64];

// Conversión voltaje → distancia (Sharp GP2Y0A41SK0F)
float voltaje_a_distancia(float volt)
{
    return 12.08f * powf(volt, -1.058f); // Según datasheet
}

int main(void)
{
    CyGlobalIntEnable;

    ADC_DelSig_1_Start();
    ADC_DelSig_1_StartConvert();
    UART_1_Start();
    
    UART_1_PutString("UART funcionando\r\n");

    for(;;)
    {
        if (ADC_DelSig_1_IsEndConversion(ADC_DelSig_1_RETURN_STATUS))
        {
            int16 adcValue = ADC_DelSig_1_GetResult16();
            float voltaje = (float)adcValue * 5.0f / 4095.0f;
            float distancia = voltaje_a_distancia(voltaje);

            // Formatear partes enteras y decimales
            int volt_entero = (int)voltaje;
            int volt_decimal = (int)((voltaje - volt_entero) * 100);
            int dist_entero = (int)distancia;
            int dist_decimal = (int)((distancia - dist_entero) * 100);

            // Formato CSV: V:X.XXV D:Y.YYcm
            sprintf(buffer, "V:%d.%02dV D:%d.%02dcm\r\n", 
                    volt_entero, volt_decimal, dist_entero, dist_decimal);
            UART_1_PutString(buffer);

            CyDelay(200); // 5 Hz
        }
    }
}
```

**Formato de salida:**
```
V:2.45V D:12.34cm
V:2.48V D:11.98cm
V:2.43V D:12.67cm
```

### Paso 2: Aplicación Python

**Estructura del proyecto:**
```
proyecto/
├── main.py
├── GUI_env/          # Ambiente virtual
└── README.md
```

**main.py:**
```python
import tkinter as tk
from tkinter import ttk, messagebox
import serial
import serial.tools.list_ports
import threading
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import time


class SerialPlotterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Serial Plotter - Distancia y Voltaje")
       
        self.serial_port = None
        self.running = False
        self.data = {
            "tiempo": [],
            "voltaje": [],
            "distancia": []
        }

        self.start_time = None
        self.selected_plot = tk.StringVar(value="Distancia vs Tiempo")

        self.build_gui()

    def build_gui(self):
        frame_top = tk.Frame(self.root)
        frame_top.pack(padx=10, pady=5)

        # Selección de COM
        tk.Label(frame_top, text="Puerto:").grid(row=0, column=0)
        self.combo_port = ttk.Combobox(frame_top, values=self.list_serial_ports(), width=10)
        self.combo_port.grid(row=0, column=1)

        # Baudios
        tk.Label(frame_top, text="Baudios:").grid(row=0, column=2)
        self.combo_baud = ttk.Combobox(frame_top, values=["9600", "115200", "57600"], width=10)
        self.combo_baud.set("115200")
        self.combo_baud.grid(row=0, column=3)

        # Paridad
        tk.Label(frame_top, text="Paridad:").grid(row=0, column=4)
        self.combo_parity = ttk.Combobox(frame_top, values=["None", "Even", "Odd"], width=10)
        self.combo_parity.set("None")
        self.combo_parity.grid(row=0, column=5)

        # Stop Bits
        tk.Label(frame_top, text="Stop Bits:").grid(row=0, column=6)
        self.combo_stop = ttk.Combobox(frame_top, values=["1", "1.5", "2"], width=5)
        self.combo_stop.set("1")
        self.combo_stop.grid(row=0, column=7)

        # Botón conectar
        self.btn_toggle = tk.Button(frame_top, text="Iniciar", command=self.toggle_connection, bg="green", fg="white")
        self.btn_toggle.grid(row=0, column=8, padx=10)

        # Selección tipo de gráfica
        tk.Label(frame_top, text="Gráfica:").grid(row=1, column=0)
        self.combo_plot = ttk.Combobox(frame_top, values=[
            "Distancia vs Tiempo",
            "Voltaje vs Tiempo",
            "Distancia vs Voltaje"
        ], textvariable=self.selected_plot, width=25)
        self.combo_plot.grid(row=1, column=1, columnspan=3, sticky="w")

        # Gráfica
        self.fig, self.ax = plt.subplots()
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.root)
        self.canvas.get_tk_widget().pack()

        self.ani = animation.FuncAnimation(self.fig, self.update_plot, interval=500)

    def list_serial_ports(self):
        return [port.device for port in serial.tools.list_ports.comports()]

    def toggle_connection(self):
        if self.running:
            self.running = False
            self.btn_toggle.config(text="Iniciar", bg="green")
            if self.serial_port and self.serial_port.is_open:
                self.serial_port.close()
        else:
            try:
                port = self.combo_port.get()
                baud = int(self.combo_baud.get())
                parity = {"None": serial.PARITY_NONE, "Even": serial.PARITY_EVEN, "Odd": serial.PARITY_ODD}[self.combo_parity.get()]
                stop_bits = {"1": serial.STOPBITS_ONE, "1.5": serial.STOPBITS_ONE_POINT_FIVE, "2": serial.STOPBITS_TWO}[self.combo_stop.get()]

                self.serial_port = serial.Serial(port, baudrate=baud, parity=parity, stopbits=stop_bits, timeout=1)
                self.running = True
                self.btn_toggle.config(text="Detener", bg="red")
                self.start_time = time.time()
                self.data = {"tiempo": [], "voltaje": [], "distancia": []}
                threading.Thread(target=self.read_serial, daemon=True).start()
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo abrir el puerto: {e}")

    def read_serial(self):
        while self.running and self.serial_port and self.serial_port.is_open:
            try:
                line = self.serial_port.readline().decode().strip()
                if line.startswith("V:"):
                    # Formato esperado: V:1.23V D:14.67cm
                    parts = line.replace("V:", "").replace("V", "").replace("D:", "").replace("cm", "").split()
                    if len(parts) == 2:
                        voltaje = float(parts[0])
                        distancia = float(parts[1])
                        tiempo = time.time() - self.start_time
                        self.data["tiempo"].append(tiempo)
                        self.data["voltaje"].append(voltaje)
                        self.data["distancia"].append(distancia)
            except Exception:
                continue

    def update_plot(self, frame):
        self.ax.clear()
        if not self.data["tiempo"]:
            return

        plot_type = self.selected_plot.get()
        if plot_type == "Distancia vs Tiempo":
            self.ax.plot(self.data["tiempo"], self.data["distancia"], label="Distancia (cm)", color='blue')
            self.ax.set_ylabel("Distancia (cm)")
            self.ax.set_xlabel("Tiempo (s)")
        elif plot_type == "Voltaje vs Tiempo":
            self.ax.plot(self.data["tiempo"], self.data["voltaje"], label="Voltaje (V)", color='green')
            self.ax.set_ylabel("Voltaje (V)")
            self.ax.set_xlabel("Tiempo (s)")
        elif plot_type == "Distancia vs Voltaje":
            self.ax.plot(self.data["voltaje"], self.data["distancia"], label="D vs V", color='red')
            self.ax.set_xlabel("Voltaje (V)")
            self.ax.set_ylabel("Distancia (cm)")

        self.ax.set_title(plot_type)
        self.ax.grid(True)
        self.ax.legend()
        self.canvas.draw()


if __name__ == "__main__":
    root = tk.Tk()
    app = SerialPlotterApp(root)
    root.mainloop()
```

### Paso 3: Ejecución

```bash
# Activar ambiente virtual
GUI_env\Scripts\activate

# Ejecutar aplicación
python main.py
```

**Modos de visualización disponibles:**
1. 📈 **Distancia vs Tiempo** - Monitoreo temporal de distancia
2. ⚡ **Voltaje vs Tiempo** - Señal ADC en el tiempo
3. 🔗 **Distancia vs Voltaje** - Curva de calibración del sensor

---

## ⏱️ Frecuencia de Muestreo

### ¿Quién determina la Fs?

**Respuesta:** El firmware del PSoC (`main.c`), NO el ADC ni Python.

**Factores que afectan Fs:**
- ✅ `CyDelay()` explícito en el código
- ❌ Procesamiento adicional (filtros, cálculos)
- ❌ Overhead de comunicación UART
- ❌ Bucles ineficientes

### Cálculo de Fs Real

#### Método 1: Aproximación Simple

```c
// Ejemplo: Fs deseada = 10 Hz → Ts = 100 ms
for(;;) {
    // Lectura ADC (~1 ms)
    // Procesamiento (~5 ms)
    // UART transmisión (~2 ms)
    
    CyDelay(92); // 100ms - 8ms overhead = 92ms
}
```

#### Método 2: Medición Precisa (Ingeniería Inversa)

**Script Python para medir Fs:**
```python
import serial
import time

port = serial.Serial('COM5', 115200, timeout=1)
samples = []
start = time.time()

while time.time() - start < 20:  # 20 segundos
    if port.readline():
        samples.append(time.time())

Fs_real = len(samples) / 20
print(f"Frecuencia de muestreo real: {Fs_real:.2f} Hz")
```

### Teorema de Nyquist

Para señales periódicas:

```
Fs ≥ 2 × Fmax
```

**Ejemplo:**
- Señal cardíaca: Fmax ≈ 10 Hz → Fs ≥ 20 Hz
- Audio: Fmax = 20 kHz → Fs ≥ 40 kHz

⚠️ **Nota:** Señales DC (Fmax = 0) no requieren Fs específica.

---

## 🔢 Conversión ADC a Voltaje

### Fórmula General

```c
float voltaje = (float)adcValue * Vref / (2^n - 1);
```

Donde:
- `adcValue`: Resultado del ADC (0 a 4095 para 12 bits)
- `Vref`: Voltaje de referencia (configurado en ADC)
- `n`: Resolución en bits (12 bits → 4096 niveles)

### Tabla de Configuraciones

| Rango de Entrada | Config. ADC | Fórmula | Ejemplo |
|------------------|-------------|---------|---------|
| 0V - 5V | Vssa to Vdda | `(float)adc * 5.0f / 4095.0f` | adc=2048 → 2.5V |
| 0V - 3.3V | Vssa to Vdda (3.3V) | `(float)adc * 3.3f / 4095.0f` | adc=2048 → 1.65V |
| 0V - 2.048V | Vssa to 2.048V | `(float)adc * 2.048f / 4095.0f` | adc=2048 → 1.024V |
| -2.5V - +2.5V | Vssa ±2.5V | `(float)adc * 5.0f / 4095.0f - 2.5f` | adc=2048 → 0V |

### Código de Ejemplo

```c
// ADC configurado: Vssa to Vdda (5V), 12 bits
int16 adcValue = ADC_DelSig_1_GetResult16(); // 0-4095
float voltaje = (float)adcValue * 5.0f / 4095.0f;

// Uso de 'f' para operaciones en punto flotante (más eficiente que double)
```

---

## 🐛 Solución de Problemas

### Problema: No se reconoce el puerto COM

**Soluciones:**
1. Verificar driver USB-Serial (Cypress USB-UART):
   ```
   Administrador de dispositivos → Puertos (COM y LPT)
   ```
2. Reinstalar PSoC Programmer
3. Probar con otro cable USB

### Problema: Datos corruptos en UART

**Verificaciones:**
1. Baudrate coincidente (PSoC y PuTTY/Python):
   ```c
   // PSoC
   UART_1_BAUD = 115200
   
   # Python
   serial.Serial('COM5', 115200)
   ```
2. Configuración de bits:
   - Data bits: 8
   - Parity: None
   - Stop bits: 1

### Problema: `sprintf` no funciona con flotantes

**Solución:**
Agregar flag del compilador:
```
Build Settings → Linker → Custom Flags: -u _printf_float
```

### Problema: Gráficas no se actualizan

**Causa común:** Thread de lectura serial bloqueado

**Solución:**
```python
# Agregar timeout en serial.Serial()
self.serial_port = serial.Serial(port, baud, timeout=1)
```

---

## 📚 Referencias

- [PSoC 5LP Datasheet](https://www.cypress.com/file/45906/download)
- [Sharp GP2Y0A41SK0F Datasheet](https://www.pololu.com/file/0J845/GP2Y0A41SK0F.pdf)
- [PySerial Documentation](https://pyserial.readthedocs.io/)
- [Matplotlib Animation](https://matplotlib.org/stable/api/animation_api.html)

---

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Por favor:

1. Fork el proyecto
2. Crea una rama (`git checkout -b feature/mejora`)
3. Commit cambios (`git commit -m 'Agrega nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/mejora`)
5. Abre un Pull Request

---

## 📄 Licencia

Este proyecto está bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para detalles.

---

## 👨‍💻 Autor

**Luis David Barahona Valdivieso**

- 📧 Email: [Contacto]
- 🔗 LinkedIn: [Perfil]
- 🌐 GitHub: [Repositorio]

---

## 🙏 Agradecimientos

- Cypress Semiconductor por PSoC Creator
- Comunidad de Python por las excelentes librerías
- Sharp Corporation por la documentación detallada

---

**⭐ Si este proyecto te fue útil, considera darle una estrella en GitHub!**
