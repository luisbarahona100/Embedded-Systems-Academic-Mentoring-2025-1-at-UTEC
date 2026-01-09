;
; AssemblerApplication1.asm

; Created: 24/04/2025 23:23:23
; Author : luisdavidbarahona
;

;PASO 1: DEFINIR VARIABLES Y PUERTOS
;PASO 2: DEFINIR STACK POINTER
LDI R16, LOW(RAMEND)
OUT SPL, R16
LDI R16, HIGH(RAMEND)
OUT SPH, R16

;PASO 3: PROGRAMA MAIN

; Entradas:
MAIN:
LDI R17, 0b01100000 ;   R17:R16 -> número de 16 bits con signo a desplazar
LDI R16, 0b00010000
LDI R18, 0b00000010 ;   R18     -> número de desplazamientos (n)
; Llamar a la RUTINA ASR_16BITS
RCALL RUTINA_ASR16Bits

LDI R19, 0x01
RJMP MAIN


;PASO 4: RUTINAS (Arithmetic Shift Right)
RUTINA_ASR16Bits:
	;INPUT: R17:R16 número de 16 bits con signo a desplazar
	;INPUT: R18  número de desplazamientos (n)
	;OUTPUT: R17:R16 ROTADOS A LA DERECHA EN n BITS
    cp      R18, R1          ; Compara contador con cero (R1 = 0)
    breq    FinDesplaza      ; Si es 0, termina
LoopDesplaza:
    RCALL   RUTINA_ASR8Bits  ; Desplaza aritméticamente byte alto del R17
    ror     R16              ; Rota byte bajo con el carry del ASR
    dec     R18              ; Decrementa el contador
    brne    LoopDesplaza     ; Repite si R18 ? 0
FinDesplaza:
    ret


RUTINA_ASR8Bits:
	; R17 contiene el valor que deseas desplazar
	; Se conserva el bit de signo (MSB)
	;INPUT: R17
	;OUTPU; R17 DESPLAZADO EN 1 BIT A LA DERECHA, MANTENIENDO EL BIT MSB

	bst R17, 7      ; Copia el bit 7 (MSB) en el T (bit temporal del SREG)
	lsr R17         ; Desplazamiento lógico a la derecha (rellena con 0)
	bld R17, 7      ; Carga el bit T en el bit 7 (restaurando el signo)

RET
