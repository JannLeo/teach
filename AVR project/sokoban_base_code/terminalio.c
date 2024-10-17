// /*
//  * terminalio.c
//  *
//  * Author: Peter Sutton
//  */

// #include "terminalio.h"
// #include <stdio.h>
// #include <stdint.h>
// #include <string.h>
// #include <avr/pgmspace.h>

// void move_terminal_cursor(int row, int col)
// {
//     printf_P(PSTR("\x1b[%d;%dH"), row + 1, col + 1);
// }

// void normal_display_mode(void)
// {
// 	printf_P(PSTR("\x1b[0m"));
// }

// void reverse_video(void)
// {
// 	printf_P(PSTR("\x1b[7m"));
// }

// void clear_terminal(void)
// {
// 	printf_P(PSTR("\x1b[2J"));
// }

// void clear_to_end_of_line(void)
// {
// 	printf_P(PSTR("\x1b[K"));
// }

// void set_display_attribute(DisplayParameter parameter)
// {
// 	printf_P(PSTR("\x1b[%dm"), parameter);
// }

// void hide_cursor(void)
// {
// 	printf_P(PSTR("\x1b[?25l"));
// }

// void show_cursor(void)
// {
// 	printf_P(PSTR("\x1b[?25h"));
// }

// void enable_scrolling_for_whole_display(void)
// {
// 	printf_P(PSTR("\x1b[r"));
// }

// void set_scroll_region(int row1, int row2)
// {
// 	printf_P(PSTR("\x1b[%d;%dr"), row1 + 1, row2 + 1);
// }

// void scroll_down(void)
// {
// 	printf_P(PSTR("\x1bM")); // ESC-M
// }

// void scroll_up(void)
// {
// 	printf_P(PSTR("\x1b\x44")); // ESC-D
// }

// void draw_horizontal_line(int row, int start_col, int end_col)
// {
// 	// Place cursor at starting position.
// 	move_terminal_cursor(row, start_col);
// 	// Reverse the video - black on white.
// 	reverse_video();
// 	// Print spaces until the end column. Since spaces are blank,
// 	// and we're in reverse video mode, a fat white line gets drawn.
// 	for (int i = start_col; i <= end_col; i++)
// 	{
// 		putchar(' '); // Print space.
// 	}
// 	// Reset the mode to normal.
// 	normal_display_mode();
// }

// void draw_vertical_line(int col, int start_row, int end_row)
// {
// 	// Place cursor at starting position.
// 	move_terminal_cursor(start_row, col);
// 	// Reverse the video - black on white.
// 	reverse_video();
// 	// Print spaces until the row above end row. Since spaces are blank,
// 	// and we're in reverse video mode, a fat white line gets drawn.
// 	for (int i = start_row; i < end_row; i++)
// 	{
// 		putchar(' '); // Print space.
// 		// Move down a row and step back to previous column (because
// 		// printing the space caused the cursor to be advanced by one
// 		// column).
// 		printf_P(PSTR("\x1b[B\x1b[D"));
// 	}
// 	// Print the space for the end row, and do not move the cursor down.
// 	putchar(' ');
// 	// Reset the mode to normal.
// 	normal_display_mode();
// }
/*
 * terminalio.c
 *
 * 作者: Peter Sutton
 *
 * 此文件包含用于控制终端输入/输出的函数，特别是用于操作终端光标、显示属性和绘制简单图形。
 */

#include "terminalio.h"
#include <stdio.h>
#include <stdint.h>
#include <string.h>
#include <avr/pgmspace.h>

// 将光标移动到终端中的指定行和列位置。
// (终端中的行和列是从1开始的，因此参数加1)。
void move_terminal_cursor(int row, int col)
{
    printf_P(PSTR("\x1b[%d;%dH"), row + 1, col + 1);
}

// 将终端显示模式设置为正常（重置所有文本属性）。
void normal_display_mode(void)
{
	printf_P(PSTR("\x1b[0m"));
}

// 将终端显示模式设置为反色显示（颜色反转）。
void reverse_video(void)
{
	printf_P(PSTR("\x1b[7m"));
}

// 清除整个终端屏幕。
void clear_terminal(void)
{
	printf_P(PSTR("\x1b[2J"));
}

// 清除从当前光标位置到行末的内容。
void clear_to_end_of_line(void)
{
	printf_P(PSTR("\x1b[K"));
}

// 根据提供的参数设置显示属性（例如文本颜色或样式）。
void set_display_attribute(DisplayParameter parameter)
{
	printf_P(PSTR("\x1b[%dm"), parameter);
}

// 隐藏终端中的光标。
void hide_cursor(void)
{
	printf_P(PSTR("\x1b[?25l"));
}

// 显示终端中的光标。
void show_cursor(void)
{
	printf_P(PSTR("\x1b[?25h"));
}

// 启用整个终端显示的滚动功能。
void enable_scrolling_for_whole_display(void)
{
	printf_P(PSTR("\x1b[r"));
}

// 在终端中设置指定行之间的滚动区域。
void set_scroll_region(int row1, int row2)
{
	printf_P(PSTR("\x1b[%d;%dr"), row1 + 1, row2 + 1);
}

// 将终端显示内容向下滚动一行。
void scroll_down(void)
{
	printf_P(PSTR("\x1bM")); // ESC-M
}

// 将终端显示内容向上滚动一行。
void scroll_up(void)
{
	printf_P(PSTR("\x1b\x44")); // ESC-D
}

// 通过使用反显模式打印空格来绘制水平线，以模拟一条线。
void draw_horizontal_line(int row, int start_col, int end_col)
{
	// 将光标放置在起始位置。
	move_terminal_cursor(row, start_col);
	// 反显 - 黑底白字。
	reverse_video();
	// 打印空格直到结束列。由于空格是空白的，
	// 并且我们处于反显模式，因此绘制出了一条粗白线。
	for (int i = start_col; i <= end_col; i++)
	{
		putchar(' '); // 打印空格。
	}
	// 重置为正常模式。
	normal_display_mode();
}

// 通过使用反显模式打印空格来绘制垂直线，以模拟一条线。
void draw_vertical_line(int col, int start_row, int end_row)
{
	// 将光标放置在起始位置。
	move_terminal_cursor(start_row, col);
	// 反显 - 黑底白字。
	reverse_video();
	// 打印空格直到结束行上方。由于空格是空白的，
	// 并且我们处于反显模式，因此绘制出了一条粗白线。
	for (int i = start_row; i < end_row; i++)
	{
		putchar(' '); // 打印空格。
		// 向下移动一行并返回到前一列（因为打印空格导致光标前进了一列）。
		printf_P(PSTR("\x1b[B\x1b[D"));
	}
	// 为结束行打印空格，并且不向下移动光标。
	putchar(' ');
	// 重置为正常模式。
	normal_display_mode();
}