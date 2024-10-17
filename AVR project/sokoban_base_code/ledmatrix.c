/*
 * ledmatrix.c
 *
 * 作者: Peter Sutton
 */

#include "ledmatrix.h" // 包含 LED 矩阵的头文件
#include <stdint.h>    // 包含标准整数类型的定义
#include "spi.h"       // 包含 SPI 通信的头文件
#include "pixel_colour.h" // 包含像素颜色定义的头文件

// 定义用于 LED 矩阵操作的指令
#define CMD_UPDATE_ALL		(0x00) // 更新整个显示
#define CMD_UPDATE_PIXEL	(0x01) // 更新单个像素
#define CMD_UPDATE_ROW		(0x02) // 更新一行
#define CMD_UPDATE_COL		(0x03) // 更新一列
#define CMD_SHIFT_DISPLAY	(0x04) // 移动整个显示内容
#define CMD_CLEAR_SCREEN	(0x0F) // 清除屏幕

// 初始化 LED 矩阵
void init_ledmatrix(void)
{
	// 设置 SPI，使用 128 的时钟分频器。该速度保证了 LED 矩阵上的 SPI 缓冲区不会溢出。
	spi_setup_master(128);
}

// 更新整个 LED 矩阵的显示
void ledmatrix_update_all(MatrixData data)
{
	(void)spi_send_byte(CMD_UPDATE_ALL); // 发送指令以更新所有像素
	for (uint8_t row = 0; row < MATRIX_NUM_ROWS; row++) // 遍历每一行
	{
		for (uint8_t col = 0; col < MATRIX_NUM_COLUMNS; col++) // 遍历每一列
		{
			(void)spi_send_byte(data[row][col]); // 发送每个像素的颜色数据
		}
	}
}

// 更新 LED 矩阵中特定的像素
void ledmatrix_update_pixel(uint8_t row, uint8_t col, PixelColour pixel)
{
	if (col >= MATRIX_NUM_COLUMNS || row >= MATRIX_NUM_ROWS) // 检查行列是否超出矩阵范围
	{
		// 无效的位置，忽略请求
		return;
	}
	(void)spi_send_byte(CMD_UPDATE_PIXEL); // 发送指令以更新单个像素
	(void)spi_send_byte(((row & 0x07) << 4) | (col & 0x0F)); // 发送行和列的编码信息
	(void)spi_send_byte(pixel); // 发送像素颜色数据
}

// 更新 LED 矩阵中的某一行
void ledmatrix_update_row(uint8_t row, MatrixRow data)
{
	if (row >= MATRIX_NUM_ROWS) // 检查行号是否超出范围
	{
		// 无效的行号，忽略请求
		return;
	}
	(void)spi_send_byte(CMD_UPDATE_ROW); // 发送指令以更新一行
	(void)spi_send_byte(row & 0x07); // 发送行号
	for (uint8_t col = 0; col < MATRIX_NUM_COLUMNS; col++) // 遍历每一列
	{
		(void)spi_send_byte(data[col]); // 发送每列的颜色数据
	}
}

// 更新 LED 矩阵中的某一列
void ledmatrix_update_column(uint8_t col, MatrixColumn data)
{
	if (col >= MATRIX_NUM_COLUMNS) // 检查列号是否超出范围
	{
		// 无效的列号，忽略请求
		return;
	}
	(void)spi_send_byte(CMD_UPDATE_COL); // 发送指令以更新一列
	(void)spi_send_byte(col & 0x0F); // 发送列号
	for (uint8_t row = 0; row < MATRIX_NUM_ROWS; row++) // 遍历每一行
	{
		(void)spi_send_byte(data[row]); // 发送每行的颜色数据
	}
}

// 向左移动 LED 矩阵上的显示内容
void ledmatrix_shift_display_left(void)
{
	(void)spi_send_byte(CMD_SHIFT_DISPLAY); // 发送指令以移动显示
	(void)spi_send_byte(0x02); // 指定移动方向为左
}

// 向右移动 LED 矩阵上的显示内容
void ledmatrix_shift_display_right(void)
{
	(void)spi_send_byte(CMD_SHIFT_DISPLAY); // 发送指令以移动显示
	(void)spi_send_byte(0x01); // 指定移动方向为右
}

// 向上移动 LED 矩阵上的显示内容
void ledmatrix_shift_display_up(void)
{
	(void)spi_send_byte(CMD_SHIFT_DISPLAY); // 发送指令以移动显示
	(void)spi_send_byte(0x08); // 指定移动方向为上
}

// 向下移动 LED 矩阵上的显示内容
void ledmatrix_shift_display_down(void)
{
	(void)spi_send_byte(CMD_SHIFT_DISPLAY); // 发送指令以移动显示
	(void)spi_send_byte(0x04); // 指定移动方向为下
}

// 清除 LED 矩阵上的显示内容
void ledmatrix_clear(void)
{
	(void)spi_send_byte(CMD_CLEAR_SCREEN); // 发送指令以清除屏幕
}

// 将一个矩阵列的内容复制到另一个矩阵列
void copy_matrix_column(MatrixColumn from, MatrixColumn to)
{
	for (uint8_t row = 0; row < MATRIX_NUM_ROWS; row++) // 遍历每一行
	{
		to[row] = from[row]; // 复制每行的数据
	}
}

// 将一个矩阵行的内容复制到另一个矩阵行
void copy_matrix_row(MatrixRow from, MatrixRow to)
{
	for (uint8_t col = 0; col < MATRIX_NUM_COLUMNS; col++) // 遍历每一列
	{
		to[col] = from[col]; // 复制每列的数据
	}
}

// 将矩阵列中的所有像素设置为指定颜色
void set_matrix_column_to_colour(MatrixColumn matrix_column,
	PixelColour colour)
{
	for (uint8_t row = 0; row < MATRIX_NUM_ROWS; row++) // 遍历每一行
	{
		matrix_column[row] = colour; // 设置每行的颜色为指定颜色
	}
}

// 将矩阵行中的所有像素设置为指定颜色
void set_matrix_row_to_colour(MatrixRow matrix_row, PixelColour colour)
{
	for (uint8_t column = 0; column < MATRIX_NUM_COLUMNS; column++) // 遍历每一列
	{
		matrix_row[column] = colour; // 设置每列的颜色为指定颜色
	}
}
