/*
 * RetardoAVR_CodeC.c
 *
 * Created: 2/05/2025 12:50:18
 * Author : luisdavidbarahona
 */ 

#define F_CPU 1000000UL  // Frecuencia de reloj de 16 MHz
#include <avr/io.h>
#include <util/delay.h>

// Subrutina para cambiar el estado del LED
void toggle_led(void) {
	PIND = ^(1 << PD1);  // Alterna el bit PD1 (toggle)
}

// Subrutina de delay de ~1 segundo
void delay_1s(void) {
	for (uint8_t i = 0; i < 100; i++) {
		_delay_ms(10);  // 100 * 10 ms = 1000 ms = 1s
	}
}

int main(void) {
	// Configurar PB1 como entrada sin pull-up
	DDRB &= ~(1 << PB1);   // DDRB[1] = 0 => PB1 como entrada
	PORTB &= ~(1 << PB1);  // Sin pull-up => requiere pull-down físico

	// Configurar PD1 como salida
	DDRD |= (1 << PD1);    // PD1 como salida
	PORTD &= ~(1 << PD1);  // Apaga el LED inicialmente

	while (1) {
		// Si se presiona el botón (PB1 == 0)
		if (PINB & (1 << PB1)) {
			toggle_led();    // Cambiar estado del LED
			delay_1s();      // Espera 1 segundo
			} else {
			PORTD &= ~(1 << PD1);  // Si no está presionado, apaga el LED
		}
	}
}
