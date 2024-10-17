*
 * FILE: lab13-2.c
 *
 * Replace the "<-YOUR CODE HERE->" comment lines with your code.
 *
 * A seven segment display is connected to port A, with the CC
 * (digit select) pin connected to port D, pin 0.
 * A push button will be connected to pin T0.
 * We will count the number of times that the push button 
 * is pressed using timer/counter 0. We will display this value on 
 * the seven segment display as a two digit number 00 -> 99. We
 * will alternate the digit display 1000 times per second so that
 * we can see both digits together.
 */

#include <avr/io.h>

// Seven segment display - segment values for digits 0 to 9
uint8_t seven_seg[10] = { 63,6,91,79,102,109,125,7,127,111};

/* Display digit function. Arguments are the digit number (0 to 9)
 * and the digit to display it on (0 = right, 1 = left). The function 
 * outputs the correct seven segment display value to port A and the 
 * correct digit select value to port D, pin 0.
 * See Lecture 14 example code for some code to base this on.
 */
 // 10
 
void display_digit(uint8_t number, uint8_t digit) 
{
	PORTD = digit;
	PORTA = seven_seg[number];	// We assume digit is in range 0 to 9
}

/*
 * main -- Main program
 */
int main(void)
{
	uint8_t digit; /* 0 = right, 1 = left */
	uint8_t value;

	/* Set port A (all pins) to be outputs */
	DDRA = 0xFF;

    /* Set port D, pin 0 to be an output */
    DDRD = 1;

	/* Set up timer/counter 0 to count the number of rising
	** edges on pin T0.
	*/
	TCCR0A = 0;
	TCCR0B = (1<<CS02) | (1<<CS01) | (1<<CS00);

	/* Set up timer/counter 1 so that it reaches an output compare
	** match every 1 millisecond (1000 times per second) and then
	** resets to 0.
	** We divide the clock by 8 and count 1000 cycles (0 to 999)
	*/
	OCR1A = 999;
	TCCR1A = (0 << COM1A1) | (1 << COM1A0)  // Toggle OC1A on compare match
		| (0 << WGM11) | (0 << WGM10); // Least two significant WGM bits
	TCCR1B = (0 << WGM13) | (1 << WGM12) // Two most significant WGM bits
		| (0 << CS12) | (1 << CS11) | (0 <<CS10); // Divide clock by 8


	/* Repeatedly output the di
	
	
	
	
	
	//
	/*
 * FILE: lab14-2-solution.c
 *
 * Push buttons B0 to B3 are connected to port C, pins 0 to 3.
 * Button B0 (pin C0) increases the frequency
 * Button B1 (pin C1) decreases the frequency
 * Button B2 (pin C2) increases the duty cycle
 * Button B3 (pin C3) decreases the duty cycle
 *
 * A piezo buzzer and an LED should both be connected to the OC1B pin
 * (port D, pin 4). (The other end of the piezo buzzer should be connected
 * to ground (0V).)
 */

#include <avr/io.h>
#define F_CPU 8000000UL	// 8MHz
#include <util/delay.h>
#include <stdint.h>

// For a given frequency (Hz), return the clock period (in terms of the
// number of clock cycles of a 1MHz clock)
uint16_t freq_to_clock_period(uint16_t freq) {
	return (1000000UL / freq);	// UL makes the constant an unsigned long (32 bits)
								// and ensures we do 32 bit arithmetic, not 16
}

// Return the width of a pulse (in clock cycles) given a duty cycle (%) and
// the period of the clock (measured in clock cycles)
uint16_t duty_cycle_to_pulse_width(float dutycycle, uint16_t clockperiod) {
	return (dutycycle * clockperiod) / 100;
}

int main() {
	uint16_t freq = 200;	// Hz
	float dutycycle = 2;	// %
	uint16_t clockperiod = freq_to_clock_period(freq);
	uint16_t pulsewidth = duty_cycle_to_pulse_width(dutycycle, clockperiod);
	
	// Make pin OC1B be an output (port D, pin 4)
	DDRD = (1<<4);
	
	// Set the maximum count value for timer/counter 1 to be one less than the clockperiod
	OCR1A = clockperiod - 1;
	
	// Set the count compare value based on the pulse width. The value will be 1 less
	// than the pulse width - unless the pulse width is 0.
	if(pulsewidth == 0) {
		OCR1B = 0;
	} else {
		OCR1B = pulsewidth - 1;
	}
	
	// Set up timer/counter 1 for Fast PWM, counting from 0 to the value in OCR1A
	// before reseting to 0. Count at 1MHz (CLK/8).
	// Configure output OC1B to be clear on compare match and set on timer/counter
	// overflow (non-inverting mode).
	TCCR1A = (1 << COM1B1) | (0 <<COM1B0) | (1 <<WGM11) | (1 << WGM10);
	TCCR1B = (1 << WGM13) | (1 << WGM12) | (1 << CS11);