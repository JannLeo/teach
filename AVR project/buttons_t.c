/*
 * buttons.c
 *
 * 作者: Peter Sutton
 *
 * 这个文件包含了按钮的初始化和相关函数，用于处理按钮输入以及生成相应的中断。
 */

#include "buttons.h"
#include <stdint.h>
#include <stdbool.h>
#include <avr/io.h>
#include <avr/interrupt.h>

// 全局变量用于跟踪上次的按钮状态，以便在中断触发时检测变化。
// 低4位（0到3）对应于端口B的0到3号引脚的上次状态。
static volatile uint8_t last_button_state;

// 按钮队列。button_queue[0]始终是队列的头部。
// 如果从队列中取出一个元素，我们会将其他所有元素向前移动。
// 由于通常队列的长度很短，我们没有使用循环缓冲区。在大多数情况下，队列的长度不会超过1。
// 这个按钮队列可能会被下面的中断处理程序修改，因此在处理程序外修改队列时应该关闭中断。
#define BUTTON_QUEUE_SIZE 4
static volatile uint8_t button_queue[BUTTON_QUEUE_SIZE];
static volatile uint8_t queue_length;

void init_buttons(void)
{
	// 设置中断，如果引脚B0到B3中的任何一个发生变化。
	// 我们使用引脚变化中断来实现。这些引脚对应于引脚变化中断PCINT8到PCINT11，
	// 它们由引脚变化中断1覆盖。

	// 清空按钮推送队列并重置上次状态。
	queue_length = 0;
	last_button_state = 0;

	// 启用中断（参见数据手册第77页）。
	PCICR |= (1 << PCIE1);
	
	// 确保中断标志被清除（通过写1来实现）（参见数据手册第78页）。
	PCIFR |= (1 << PCIF1);
	
	// 选择我们感兴趣的引脚，设置掩码寄存器中的相应位（参见数据手册第78页）。
	PCMSK1 |= (1 << PCINT8) | (1 << PCINT9) | (1 << PCINT10) |
		(1 << PCINT11);
}

ButtonState button_pushed(void)
{
	ButtonState result = NO_BUTTON_PUSHED; // 默认结果。

	if (queue_length > 0)
	{
		// 从队列中移除第一个元素，并将其他条目向队列前端移动。
		// 在对队列进行任何更改之前，我们先关闭中断（如果中断已打开）。
		// 如果中断已打开，完成后再重新打开。
		result = button_queue[0];

		// 保存中断是否已启用，并将其关闭。
		bool interrupts_were_enabled = bit_is_set(SREG, SREG_I);
		cli();
		
		for (uint8_t i = 1; i < queue_length; i++)
		{
			button_queue[i - 1] = button_queue[i];
		}
		queue_length--;

		if (interrupts_were_enabled)
		{
			// 再次打开中断。
			sei();
		}
	}
	return result;
}

void clear_button_presses(void)
{
	// 保存中断是否已启用，并将其关闭。
	bool interrupts_were_enabled = bit_is_set(SREG, SREG_I);
	cli();
	queue_length = 0;
	last_button_state = 0;
	if (interrupts_were_enabled)
	{
		// 再次打开中断。
		sei();
	}
}

// 按钮变化中断处理程序。
ISR(PCINT1_vect)
{
	// 获取当前按钮的状态。我们将其与上次状态进行比较，以查看哪些发生了变化。
	uint8_t button_state = PINB & 0x0F;

	// 遍历所有按钮，查看哪些发生了变化。
	// 任何按钮按下都会被添加到按钮队列中（如果有空间）。
	// 我们忽略按钮的释放，因此只关注从上次状态为0到按钮状态为1的转换。
	for (uint8_t pin = 0; pin < NUM_BUTTONS; pin++)
	{
		if (queue_length < BUTTON_QUEUE_SIZE
				&& (button_state & (1 << pin))
				&& !(last_button_state & (1 << pin)))
				{
			// 将按钮按下加入队列（并更新队列长度）。
			button_queue[queue_length++] = pin;
		}
	}
	
	// 记住当前按钮状态。
	last_button_state = button_state;
}