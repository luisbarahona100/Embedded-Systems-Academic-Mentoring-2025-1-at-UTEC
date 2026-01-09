# Embedded Systems – Academic Mentoring 2025-1 (UTEC)

This repository contains the academic material, examples, and practical exercises developed for the **Embedded Systems Academic Mentoring Program (2025-1)** at the **University of Engineering and Technology (UTEC)**.

The course focuses on **fundamental and applied concepts of embedded systems**, covering both **8-bit AVR microcontrollers** and **ARM Cortex-M–based Systems-on-Chip**, with an emphasis on **low-level programming, hardware–software integration, and peripheral management**.

---

## 🎯 Course Objectives

- Understand the **concepts, metrics, and development flow** of embedded systems.
- Develop embedded applications using **low-level programming (C and Assembly)**.
- Analyze and program **AVR 8-bit microcontrollers** and **ARM Cortex-M–based SoCs**.
- Configure and integrate **internal peripherals and communication protocols**.
- Design embedded solutions that interact with **analog, digital, and power systems**.

---

## 🧠 Course Syllabus

### 1. Embedded Systems Concepts, Metrics, and Development Flow
- Definition of embedded systems concepts  
- Reliability in embedded systems  
- Embedded systems development methodologies  

### 2. Architecture and Programming of an 8-bit AVR Microcontroller
- Microcontroller architecture  
- Memory organization and management  
- Logical and arithmetic operations  
- Conditional branching and program flow  
- Subroutine usage  
- Internal and external interrupts  

### 3. Embedded System Development on an ARM Cortex-M3–Based SoC
- System-on-Chip (SoC) architecture  
- ARM Cortex-M3 processor architecture  
- Configuration and usage of **PSoC 5LP internal peripherals**  
- Peripheral and interrupt management on the **PSoC 5LP**  

### 4. Basic Peripherals and System Integration Criteria
- Communication protocols: **UART, SPI, I²C**  
- Timer architecture and usage  
- **PWM signal generation**  
- **ADC and DAC architecture and applications**  
- Operational amplifiers (OPAMPs) in embedded systems  
- Integration of embedded systems with **power electronics systems**

---

## 🛠️ Development Platforms and Tools

### Hardware

#### **ATmega328P** (8-bit AVR microcontroller)
- 📄 [Official Datasheet (Microchip)](https://ww1.microchip.com/downloads/en/DeviceDoc/Atmel-7810-Automotive-Microcontrollers-ATmega328P_Datasheet.pdf)
- 📚 [ATmega328P Product Page](https://www.microchip.com/en-us/product/ATmega328P)
- 🎓 [AVR Instruction Set Manual](https://ww1.microchip.com/downloads/en/DeviceDoc/AVR-InstructionSet-Manual-DS40002198.pdf)
- 📖 [Arduino Uno Hardware Reference](https://docs.arduino.cc/hardware/uno-rev3/) (usa ATmega328P)

#### **PSoC 5LP** (ARM Cortex-M3–based SoC)
- 📄 [PSoC 5LP Datasheet (Infineon)](https://www.infineon.com/dgdl/Infineon-CY8C58LP_Family_Datasheet_Programmable_System-on-Chip_(PSoC)-DataSheet-v16_00-EN.pdf?fileId=8ac78c8c7d0d8da4017d0ee7d03a70b1)
- 📚 [PSoC 5LP Product Family Page](https://www.infineon.com/cms/en/product/microcontroller/32-bit-psoc-arm-cortex-microcontroller/psoc-5-lp/)
- 📖 [PSoC 5LP Architecture TRM](https://www.infineon.com/dgdl/Infineon-PSoC_5LP_Architecture_TRM-AdditionalTechnicalInformation-v11_00-EN.pdf?fileId=8ac78c8c7d0d8da4017d0f946dbf01a0)
- 🎓 [CY8CKIT-059 Development Kit](https://www.infineon.com/cms/en/product/evaluation-boards/cy8ckit-059/)

### Software

#### **Microchip Studio** (AVR development)
- 💿 [Download Microchip Studio](https://www.microchip.com/en-us/tools-resources/develop/microchip-studio)
- 📖 [User Guide](https://www.microchip.com/en-us/tools-resources/develop/microchip-studio#Documentation)
- 🎥 [Getting Started Video Tutorial](https://www.youtube.com/watch?v=xqXmdirt6Xs)
- 📚 [Microchip Studio Help & Tutorials](https://microchipdeveloper.com/8avr:avrstart)

#### **AVRDUDESS** (AVR programming and flashing)
- 💿 [Download AVRDUDESS (GUI for AVRDUDE)](https://blog.zakkemble.net/avrdudess-a-gui-for-avrdude/)
- 📖 [AVRDUDE Documentation](https://github.com/avrdudes/avrdude/wiki)
- 🔧 [AVRDUDE GitHub Repository](https://github.com/avrdudes/avrdude)
- 📚 [AVRDUDE Command Reference](https://www.nongnu.org/avrdude/user-manual/avrdude.html)

#### **PSoC Creator 4.4** (PSoC development)
- 💿 [Download PSoC Creator](https://www.infineon.com/cms/en/design-support/tools/sdk/psoc-software/psoc-creator/)
- 📖 [PSoC Creator User Guide](https://www.infineon.com/dgdl/Infineon-PSoC_Creator_User_Guide-UserManual-v02_00-EN.pdf?fileId=8ac78c8c7d718a49017d9953c1a80c93)
- 🎓 [PSoC Creator Video Tutorials](https://www.infineon.com/cms/en/design-support/tools/sdk/psoc-software/psoc-creator/#!trainings)
- 📚 [PSoC Creator Component Datasheet](https://www.infineon.com/dgdl/Infineon-PSoC_Creator_Component_Datasheet-DataSheet-v02_00-EN.pdf?fileId=8ac78c8c7d718a49017d99537f150c94)

### Programming Languages

#### **C Programming for Embedded Systems**
- 📖 [Embedded C Tutorial (Microchip)](https://microchipdeveloper.com/8avr:avrlibc)
- 📚 [AVR Libc Reference Manual](https://www.nongnu.org/avr-libc/user-manual/index.html)
- 🎓 [C Programming for Embedded Systems Course](https://www.coursera.org/learn/introduction-embedded-systems)
- 📘 [Embedded C Coding Standard](https://barrgroup.com/embedded-systems/books/embedded-c-coding-standard)

#### **Assembly (AVR)**
- 📖 [AVR Assembly Language Programming](http://www.avr-asm-tutorial.net/)
- 📚 [AVR Assembler User Guide](https://ww1.microchip.com/downloads/en/DeviceDoc/40001917A.pdf)
- 🎓 [AVR Assembly Tutorial Series](https://www.youtube.com/playlist?list=PLtQdQmNK_0DRzELjJlLlKTq_85T7iIU4Z)

### Simulation and Testing

#### **Proteus Design Suite**
- 💿 [Proteus Professional](https://www.labcenter.com/)
- 📖 [Proteus VSM for AVR](https://www.labcenter.com/simulation/avr/)
- 🎥 [Proteus Simulation Tutorials](https://www.youtube.com/c/TheEngineeringProjects/search?query=proteus)

---

## 📁 Repository Structure


*(Structure may evolve as new mentoring materials are added.)*

---

## 👨‍🏫 Academic Context

This repository was developed as part of an **academic mentoring initiative**, aimed at supporting undergraduate students in strengthening their **practical and theoretical foundations in embedded systems**, with a strong focus on **hardware-level understanding and real-world system integration**.

---

## 📜 License

This repository is intended for **educational and academic use**.

---

## 📬 Contact

For academic or technical inquiries related to this mentoring material, please feel free to reach out through GitHub.


