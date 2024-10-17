/*
 * timer0.c
 *
 * 作者: Peter Sutton
 *
 * 这个文件包含了Timer 0的初始化和相关函数，用于生成每毫秒的时钟中断。
 */

#include "timer0.h"
#include <stdint.h>
#include <avr/io.h>
#include <avr/interrupt.h>

// 我们的内部时钟计数器 - 每毫秒递增一次。大约每49天会溢出一次。
static volatile uint32_t clock_ticks_ms;

void init_timer0(void)
{
	// 重置时钟计数器。L表示这是一个长整型（32位）常量。
	clock_ticks_ms = 0L;

	// 设置Timer 0生成每1毫秒的中断。我们将时钟除以64并计数到124。
	// 因此，我们将在64 x 125个时钟周期后得到一个中断，即每1毫秒中断一次（使用8MHz时钟）。
	// 计数器将在达到输出比较值时重置为0。

	// 清除计数器。
	TCNT0 = 0;

	// 设置输出比较值为124。
	OCR0A = 124;

	// 设置计数器在比较匹配时清零（CTC模式），并将时钟除以64。这会启动计时器。
	TCCR0A = (1 << WGM01);
	TCCR0B = (1 << CS01) | (1 << CS00);

	// 使能输出比较匹配的中断。注意，全局中断必须启用后，才能触发中断。
	TIMSK0 |= (1 << OCIE0A);

	// 通过写1来确保中断标志被清除。
	TIFR0 = (1 << OCF0A);
}

uint32_t get_current_time(void)
{
	// 禁用中断，以确保在复制值的部分字节时中断不会触发。
	// 如果开始时中断已启用，则重新启用中断。
	uint8_t interrupts_were_enabled = bit_is_set(SREG, SREG_I);
	cli();
	uint32_t result = clock_ticks_ms;
	if (interrupts_were_enabled)
	{
		sei();
	}
	return result;
}

// 时钟滴答中断处理程序。
ISR(TIMER0_COMPA_vect)
{
	// 递增我们的时钟计数器。
	clock_ticks_ms++;
}