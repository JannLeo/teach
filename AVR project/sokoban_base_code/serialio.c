// /*
//  * serialio.c
//  *
//  * Author: Peter Sutton
//  */

// // The init_serial_stdio() function must be called before any standard IO
// // functions (e.g., printf). We use interrupt-based output and a circular
// // buffer to store output messages, this allows us to print many characters at
// // once to the buffer and have them output by the UART as speed permits.
// // If the buffer fills up, the put method will either:
// //   1. Block until there is room in it, if interrupts are enabled, or
// //   2. Discard the character, if interrupts are disabled.
// // Input is blocking - requesting input from stdin will block until a
// // character is available. If interrupts are disabled when input is sought,
// // then this will block forever. The function input_available() can be used to
// // test whether there is input available to read from stdin.

// #include "serialio.h"
// #include <stdio.h>
// #include <stdint.h>
// #include <stdbool.h>
// #include <avr/io.h>
// #include <avr/interrupt.h>

// // System clock rate in Hz. L at the end indicates this is a long constant.
// #define SYSCLK 8000000L

// // Circular buffer to hold outgoing characters. The insert_pos variable keeps
// // track of the position (0 to OUTPUT_BUFFER_SIZE-1) that the next outgoing
// // character should be written to. bytes_in_buffer keeps count of the number
// // of characters currently stored in the buffer (ranging from 0 to
// // OUTPUT_BUFFER_SIZE). This number of bytes immediately prior to the current
// // insert_pos are the bytes waiting to be output. If the insert_pos reaches
// // the end of the buffer it will wrap around to the beginning (assuming those
// // bytes have been output). NOTE: OUTPUT_BUFFER_SIZE can not be larger than
// // 255 without changing the type of the variables below (currently defined as
// // 8-bit unsigned ints).
// #define OUTPUT_BUFFER_SIZE 255
// volatile char out_buffer[OUTPUT_BUFFER_SIZE];
// volatile uint8_t out_insert_pos;
// volatile uint8_t bytes_in_out_buffer;

// // Circular buffer to hold incoming characters. Works on same principle
// // as output buffer.
// #define INPUT_BUFFER_SIZE 16
// volatile char input_buffer[INPUT_BUFFER_SIZE];
// volatile uint8_t input_insert_pos;
// volatile uint8_t bytes_in_input_buffer;
// volatile uint8_t input_overrun;

// // Variable to keep track of whether incoming characters are to be echoed
// // back or not.
// static bool do_echo;

// static int uart_put_char(char c, FILE *stream)
// {
// 	// Add the character to the buffer for transmission (if there is space
// 	// to do so). If not we wait until the buffer has space.

// 	// If the character is linefeed, we output carriage return.
// 	if (c == '\n')
// 	{
// 		uart_put_char('\r', stream);
// 	}

// 	// If the buffer is full and interrupts are disabled then we abort -
// 	// we don't output the character since the buffer will never be
// 	// emptied if interrupts are disabled. If the buffer is full and
// 	// interrupts are enabled, then we loop until the buffer has enough
// 	// space. The bytes_in_buffer variable will get modified by the ISR
// 	// which extracts bytes from the buffer.
// 	bool interrupts_enabled = bit_is_set(SREG, SREG_I);
// 	while (bytes_in_out_buffer >= OUTPUT_BUFFER_SIZE)
// 	{
// 		if (!interrupts_enabled)
// 		{
// 			return 1;
// 		}
// 	}

// 	// Add the character to the buffer for transmission if there is space
// 	// to do so. We advance the insert_pos to the next character position.
// 	// If this is beyond the end of the buffer, we wrap around back to the
// 	// beginning of the buffer. NOTE: We disable interrupts before
// 	// modifying the buffer. This prevents the ISR from modifying the
// 	// buffer at the same time. We reenable them if they were enabled when
// 	// we entered the function.
// 	cli();
// 	out_buffer[out_insert_pos++] = c;
// 	bytes_in_out_buffer++;
// 	if (out_insert_pos == OUTPUT_BUFFER_SIZE)
// 	{
// 		// Wrap around buffer pointer if necessary.
// 		out_insert_pos = 0;
// 	}

// 	// Reenable interrupts (UDR Empty interrupt may have been disabled) -
// 	// we ensure it is now enabled so that it will fire and deal with the
// 	// next character in the buffer.
// 	UCSR0B |= (1 << UDRIE0);
// 	if (interrupts_enabled)
// 	{
// 		sei();
// 	}
// 	return 0;
// }

// static int uart_get_char(FILE *stream)
// {
// 	// Wait until we've received a character.
// 	while (bytes_in_input_buffer == 0)
// 	{
// 		// Do nothing.
// 	}

// 	// Turn interrupts off and remove a character from the input buffer.
// 	// We reenable interrupts if they were on. The pending character is
// 	// the one which is byte_in_input_buffer characters before the insert
// 	// position (taking into account that we may need to wrap around).
// 	uint8_t interrupts_enabled = bit_is_set(SREG, SREG_I);
// 	cli();
// 	char c;
// 	if (input_insert_pos - bytes_in_input_buffer < 0)
// 	{
// 		// Need to wrap around.
// 		c = input_buffer[input_insert_pos - bytes_in_input_buffer +
// 			INPUT_BUFFER_SIZE];
// 	}
// 	else
// 	{
// 		c = input_buffer[input_insert_pos - bytes_in_input_buffer];
// 	}

// 	// Decrement our count of bytes in the input buffer.
// 	bytes_in_input_buffer--;
// 	if (interrupts_enabled)
// 	{
// 		sei();
// 	}

// 	// Secretly map the arrows keys to WASD. We essentially replace the
// 	// last char of the arrow key escape sequences with WASD. This will
// 	// render them invalid/wrong, but since students aren't expected to
// 	// handle escape sequences in their code, they would simply see them
// 	// as WASD. If you're a student reading this, pretend you didn't see
// 	// it XD. Honestly, you cannot rely on the arrow keys to work like
// 	// WASD, this is what we call undocumented behaviour.
// 	static char first = 0;
// 	static char second = 0;
// 	if (first == 0x1B && second == '[')
// 	{
// 		switch (c)
// 		{
// 			case 'A':
// 				c = 'w';
// 				break;
// 			case 'B':
// 				c = 's';
// 				break;
// 			case 'C':
// 				c = 'd';
// 				break;
// 			case 'D':
// 				c = 'a';
// 				break;
// 			default:
// 				break;
// 		}
// 	}
// 	first = second;
// 	second = c;

// 	return c;
// }

// // File stream which performs I/O using the UART. Used as stdio and stdout.
// static FILE serialio = FDEV_SETUP_STREAM(uart_put_char, uart_get_char,
// 	_FDEV_SETUP_RW);

// // Interrupt handler for UART Data Register Empty (i.e., another character
// // can be taken from our buffer and written out).
// ISR(USART0_UDRE_vect)
// {
// 	// Check if we have data in our buffer.
// 	if (bytes_in_out_buffer > 0)
// 	{
// 		// Yes we do - remove the pending byte and output it via the
// 		// UART. The pending byte (character) is the one which is
// 		// bytes_in_buffer characters before the insert_pos (taking
// 		// into account that we may need to wrap around to the end of
// 		// the buffer).
// 		char c;
// 		if (out_insert_pos - bytes_in_out_buffer < 0)
// 		{
// 			// Need to wrap around.
// 			c = out_buffer[out_insert_pos - bytes_in_out_buffer +
// 				OUTPUT_BUFFER_SIZE];
// 		}
// 		else
// 		{
// 			c = out_buffer[out_insert_pos - bytes_in_out_buffer];
// 		}

// 		// Decrement our count of the number of bytes in the buffer.
// 		bytes_in_out_buffer--;

// 		// Output the character via the UART.
// 		UDR0 = c;
// 	}
// 	else
// 	{
// 		// No data in the buffer. We disable the UART Data Register
// 		// Empty interrupt because otherwise it will trigger again
// 		// immediately when this ISR exits. The interrupt is reenabled
// 		// when a character is placed in the buffer.
// 		UCSR0B &= ~(1 << UDRIE0);
// 	}
// }

// // Interrupt handler for UART Receive Complete (i.e., can read a character).
// // The character is read and placed in the input buffer.
// ISR(USART0_RX_vect)
// {
// 	// Read the character - we ignore the possibility of overrun.
// 	char c = UDR0;

// 	if (do_echo && bytes_in_out_buffer < OUTPUT_BUFFER_SIZE)
// 	{
// 		// If echoing is enabled and there is output buffer space,
// 		// echo the received character back to the UART. If there
// 		// is no output buffer space, characters will be lost.
// 		uart_put_char(c, 0);
// 	}

// 	// Check if we have space in our buffer. If not, set the overrun flag
// 	// and throw away the character. We never clear the overrun flag -
// 	// it's up to the programmer to check/clear this flag if desired.
// 	if (bytes_in_input_buffer >= INPUT_BUFFER_SIZE)
// 	{
// 		input_overrun = 1;
// 	}
// 	else
// 	{
// 		// If the character is carriage return, turn it into linefeed.
// 		if (c == '\r')
// 		{
// 			c = '\n';
// 		}

// 		// There is room in the input buffer.
// 		input_buffer[input_insert_pos++] = c;
// 		bytes_in_input_buffer++;
// 		if (input_insert_pos == INPUT_BUFFER_SIZE)
// 		{
// 			// Wrap around buffer pointer if necessary.
// 			input_insert_pos = 0;
// 		}
// 	}
// }

// void init_serial_stdio(long baudrate, bool echo)
// {
// 	// Initialise our buffers.
// 	out_insert_pos = 0;
// 	bytes_in_out_buffer = 0;
// 	input_insert_pos = 0;
// 	bytes_in_input_buffer = 0;
// 	input_overrun = 0;

// 	// Record whether we're going to echo characters or not.
// 	do_echo = echo;

// 	// Configure the baud rate. This differs from the datasheet formula so
// 	// that we get rounding to the nearest integer while using integer
// 	// division (which truncates).
// 	UBRR0 = (uint16_t)((((SYSCLK / (8 * baudrate)) + 1) / 2) - 1);

// 	// Enable transmission and receiving via UART. We don't enable the UDR
// 	// empty interrupt here (we wait until we've got a character to
// 	// transmit). NOTE: Interrupts must be enabled globally for this
// 	// module to work, but we do not do this here.
// 	UCSR0B = (1 << RXEN0) | (1 << TXEN0);

// 	// Enable receive complete interrupt.
// 	UCSR0B |= (1 << RXCIE0);

// 	// Set up our stream so the get and put functions are used to
// 	// read/write characters via the serial port when we use stdio
// 	// functions.
// 	stdout = &serialio;
// 	stdin = &serialio;
// }

// bool serial_input_available(void)
// {
// 	return bytes_in_input_buffer != 0;
// }

// void clear_serial_input_buffer(void)
// {
// 	// Just adjust our buffer data so it looks empty.
// 	input_insert_pos = 0;
// 	bytes_in_input_buffer = 0;
// }
/*
 * serialio.c
 *
 * 作者: Peter Sutton
 */

// 在调用任何标准 IO 函数前，必须先调用 init_serial_stdio() 函数
// (e.g., printf)。举例来说，我们使用了事件中断输出和循环缓冲区来存储输出的消息
// 这样我们可以快速输入不少字符到缓冲区，然后 UART 可以按照实际速度输出。
// 如果缓冲区满了，那么 put 方法会：
//   1. 强制阻塞直到有空间，如果中断事件是启用的，或者
//   2. 忽略该字符，如果中断事件是禁止的。
// 输入是阻塞的，从 stdin 请求输入时会阻塞，直到有可用的字符。
// 如果当请求输入时禁止中断，就会一直阻塞。可以使用 input_available() 函数来检查是否有可用输入。

#include "serialio.h" // 包含与串行 I/O 相关的头文件
#include <stdio.h> // 包含标准输入输出的头文件
#include <stdint.h> // 包含标准整数类型定义的头文件
#include <stdbool.h> // 包含标准布局数类型定义的头文件
#include <avr/io.h> // 包含 AVR 平台的 I/O 设置
#include <avr/interrupt.h> // 包含 AVR 平台与中断相关的头文件

// 系统的时钟频率，单位为 Hz。L 表示这是长整数常量
#define SYSCLK 8000000L

// 环形缓冲区用于存储待输出的字符。insert_pos 变量用于记录下一个应将写入的位置（从 0 到 OUTPUT_BUFFER_SIZE-1）
// bytes_in_buffer 计数当前存储的字符数量（范围从 0 到 OUTPUT_BUFFER_SIZE）
// 这些位置的字符等待被输出。如果 insert_pos 达到缓冲区的末尾，它会回到开头。
// 注意：OUTPUT_BUFFER_SIZE 不能超过 255，否则应该修改下面的变量类型（当前定义为 8 位无符数。
#define OUTPUT_BUFFER_SIZE 255
volatile char out_buffer[OUTPUT_BUFFER_SIZE]; // 用于存储待输出的字符的缓冲区
volatile uint8_t out_insert_pos; // 应该写入缓冲区的位置
volatile uint8_t bytes_in_out_buffer; // 当前缓冲区中的字符数量

// 环形缓冲区用于存储输入的字符，原理与输出缓冲区相同
#define INPUT_BUFFER_SIZE 16
volatile char input_buffer[INPUT_BUFFER_SIZE]; // 用于存储待输入的字符的缓冲区
volatile uint8_t input_insert_pos; // 应该写入缓冲区的位置
volatile uint8_t bytes_in_input_buffer; // 当前缓冲区中的字符数量
volatile uint8_t input_overrun; // 输入缓冲区满过的标志

// 用于记录是否要将输入的字符反返到输出缓冲区
static bool do_echo;

// 用于 UART 输出字符的函数
static int uart_put_char(char c, FILE *stream)
{
	// 将字符添加到缓冲区中以进行传输（如果有空间的话）
	// 如果没有空间，我们将等待直到缓冲区有空间

	// 如果字符是\n，输出\r
	if (c == '\n')
	{
		uart_put_char('\r', stream);
	}

	// 如果缓冲区满了并且中断是禁止的，我们将中断，不输出字符
	// 因为如果中断禁止，缓冲区中的内容无法清空
	// 如果中断是启用的，那么我们不停循环直到缓冲区有空间
	bool interrupts_enabled = bit_is_set(SREG, SREG_I);
	while (bytes_in_out_buffer >= OUTPUT_BUFFER_SIZE)
	{
		if (!interrupts_enabled)
		{
			return 1;
		}
	}

	// 将字符添加到缓冲区中，如果有空间的话
	// 我们前进 insert_pos 位置，如果超出了缓冲区的终端，我们将返回到开头
	// 注意：我们在修改缓冲区前禁止中断，这样以避免事件中断和缓冲区同时修改
	// 如果进入时中断是启用的，我们将重新启用它
	cli();
	out_buffer[out_insert_pos++] = c; // 添加字符到缓冲区
	bytes_in_out_buffer++; // 缓冲区字符数增加
	if (out_insert_pos == OUTPUT_BUFFER_SIZE)
	{
		// 如有必要，缓冲区指针回到开头
		out_insert_pos = 0;
	}

	// 重新启用中断（UDR 空中事件也许已被禁止），
	// 我们确保它已经启用，这样它就会发灯和处理下一个字符
	UCSR0B |= (1 << UDRIE0);
	if (interrupts_enabled)
	{
		sei();
	}
	return 0;
}

// 从 UART 进行字符输入的函数
static int uart_get_char(FILE *stream)
{
	// 等待，直到收到一个字符
	while (bytes_in_input_buffer == 0)
	{
		// 什么也不做
	}

	// 关闭中断并从输入缓冲区中取出一个字符
	// 如果进入时中断是启用的，我们会重新启用它
	uint8_t interrupts_enabled = bit_is_set(SREG, SREG_I);
	cli();
	char c;
	if (input_insert_pos - bytes_in_input_buffer < 0)
	{
		// 必须进行滚回
		c = input_buffer[input_insert_pos - bytes_in_input_buffer +
			INPUT_BUFFER_SIZE];
	}
	else
	{
		c = input_buffer[input_insert_pos - bytes_in_input_buffer];
	}

	// 减少输入缓冲区中的字符数
	bytes_in_input_buffer--;
	if (interrupts_enabled)
	{
		sei();
	}

	// 秘密地将箭头键转换为 WASD
	// 我们实际上替换了箭头键的透过字符，这样将使它们为 WASD，可能将它们运行为无效/错误，因为学生不需要处理透过字符。
	// 如果你是学生在读这个，就形式地忽略它
	// 不赏面责，你无法依赖箭头键像 WASD 一样工作，这是非文档的习惯
	static char first = 0;
	static char second = 0;
	if (first == 0x1B && second == '[')
	{
		switch (c)
		{
			case 'A':
				c = 'w';
				break;
			case 'B':
				c = 's';
				break;
			case 'C':
				c = 'd';
				break;
			case 'D':
				c = 'a';
				break;
			default:
				break;
		}
	}
	first = second;
	second = c;

	return c;
}

// 用 UART 输出进行标准 I/O 和 stdout 的文件流
static FILE serialio = FDEV_SETUP_STREAM(uart_put_char, uart_get_char,
	_FDEV_SETUP_RW);

// UART 数据筒为空下的事件处理器（即可以从缓冲区中取出另一个字符并输出）
ISR(USART0_UDRE_vect)
{
	// 检查缓冲区是否有数据
	if (bytes_in_out_buffer > 0)
	{
		// 有数据，从缓冲区中移除待处理的字符，并通过 UART 输出它
		// 待处理的字符是位于 insert_pos 前 bytes_in_out_buffer 的字符
		char c;
		if (out_insert_pos - bytes_in_out_buffer < 0)
		{
			// 必须进行滚回
			c = out_buffer[out_insert_pos - bytes_in_out_buffer +
				OUTPUT_BUFFER_SIZE];
		}
		else
		{
			c = out_buffer[out_insert_pos - bytes_in_out_buffer];
		}

		// 减少缓冲区中的字符数
		bytes_in_out_buffer--;

		// 通过 UART 输出字符
		UDR0 = c;
	}
	else
	{
		// 缓冲区中没有数据
		// 我们禁止 UART 数据筒为空事件，因为否则它会在 ISR 退出时立即触发
		// 当字符添加到缓冲区时，会重新启用上述事件
		UCSR0B &= ~(1 << UDRIE0);
	}
}

// UART 接收完成事件处理器（即可以读取一个字符）
// 该字符会被放置到输入缓冲区。
ISR(USART0_RX_vect)
{
	// 读取字符，我们忽略满程的可能性
	char c = UDR0;

	if (do_echo && bytes_in_out_buffer < OUTPUT_BUFFER_SIZE)
	{
		// 如果反返启用并且有缓冲区空间，
		// 将收到的字符反返到 UART
		// 如果缓冲区没有空间，字符会丢失
		uart_put_char(c, 0);
	}

	// 检查缓冲区是否有空间
	// 如果没有，设置满程标志，并丢弃字符
	// 我们从不会清除满程标志，是否检查/清除这个标志由程序员决定
	if (bytes_in_input_buffer >= INPUT_BUFFER_SIZE)
	{
		input_overrun = 1;
	}
	else
	{
		// 如果字符是\r，将其转换为\n
		if (c == '\r')
		{
			c = '\n';
		}

		// 输入缓冲区中有空间
		input_buffer[input_insert_pos++] = c;
		bytes_in_input_buffer++;
		if (input_insert_pos == INPUT_BUFFER_SIZE)
		{
			// 如有必要，缓冲区指针回到开头
			input_insert_pos = 0;
		}
	}
}

// 初始化 UART 输入输出，设置传速和反返设置
void init_serial_stdio(long baudrate, bool echo)
{
	// 初始化缓冲区
	out_insert_pos = 0;
	bytes_in_out_buffer = 0;
	input_insert_pos = 0;
	bytes_in_input_buffer = 0;
	input_overrun = 0;

	// 记录是否反返字符
	do_echo = echo;

	// 配置传速
	// 这与数据表中的公式有手调，以设置为最接近整数，通过整数除比较实用
	UBRR0 = (uint16_t)((((SYSCLK / (8 * baudrate)) + 1) / 2) - 1);

	// 启用 UART 的传输和接收，但我们不在这里启用 UDR 空中事件，
	// 我们会等到我们有要传输的字符时再启用它
	// 注意：必须在全局上启用中断，这样模块才能工作，但我们不会在这里进行这种操作
	UCSR0B = (1 << RXEN0) | (1 << TXEN0);

	// 启用接收完成事件
	UCSR0B |= (1 << RXCIE0);

	// 设置流，这样当使用 stdio 时，可以通过串行子输入/输出字符
	stdout = &serialio;
	stdin = &serialio;
}

// 检查是否有输入可用
bool serial_input_available(void)
{
	return bytes_in_input_buffer != 0;
}

// 清除输入缓冲区
void clear_serial_input_buffer(void)
{
	// 就是调整缓冲区数据，使它看起来是空的
	input_insert_pos = 0;
	bytes_in_input_buffer = 0;
}