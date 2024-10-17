/*
 * project.c
 *
 * Authors: Peter Sutton, Luke Kamols, Jarrod Bennett, Cody Burnett,
 *          Bradley Stone, Yufeng Gao
 * Modified by: <YOUR NAME HERE>
 *
 * Main project event loop and entry point.
 * 主项目事件循环和程序入口。
 */

#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <ctype.h>
#include <avr/io.h>
#include <avr/interrupt.h>
#include <avr/pgmspace.h>

#define F_CPU 8000000UL
#include <util/delay.h>

#include "game.h"
#include "startscrn.h"
#include "ledmatrix.h"
#include "buttons.h"
#include "serialio.h"
#include "terminalio.h"
#include "timer0.h"
#include "timer1.h"
#include "timer2.h"


// Function prototypes - these are defined below (after main()) in the order
// given here.
// 函数原型 - 这些函数在 main() 之后定义，并按以下顺序给出。
void initialise_hardware(void);
void start_screen(void);
void new_game(void);
void play_game(void);
void handle_game_over(void);

/////////////////////////////// main //////////////////////////////////
int main(void)
{
    // Setup hardware and callbacks. This will turn on interrupts.
    // 设置硬件和回调函数。这将开启中断，使系统进入准备状态。
    initialise_hardware();

    // Show the start screen. Returns when the player starts the game.
    // 显示开始界面。当玩家启动游戏时返回。
    start_screen();

    // Loop forever and continuously play the game.
    // 无限循环，不断进行游戏流程。
    while (1)
    {
        new_game(); // 初始化新游戏
        play_game(); // 运行游戏主逻辑
        handle_game_over(); // 游戏结束后的处理
    }
}

void initialise_hardware(void)
{
    init_ledmatrix();  // 初始化 LED 矩阵显示
    init_buttons();    // 初始化按键输入
    init_serial_stdio(19200, false);  // 初始化串行通信（波特率为19200）
    init_timer0();     // 初始化计时器0
    init_timer1();     // 初始化计时器1
    init_timer2();     // 初始化计时器2

    // Turn on global interrupts.
    // 开启全局中断，使系统可以响应硬件事件。
    sei();
}

void start_screen(void)
{
    // Hide terminal cursor and set display mode to default.
    // 隐藏终端光标，并将显示模式设置为默认模式。
    hide_cursor();
    normal_display_mode();

    // Clear terminal screen and output the title ASCII art.
    // 清空终端屏幕并输出标题 ASCII 艺术字。
    clear_terminal();
    display_terminal_title(3, 5);  // 在指定位置显示游戏标题
    move_terminal_cursor(11, 5);   // 将光标移动到指定位置
    // Change this to your name and student number. Remember to remove the
    // chevrons - "<" and ">"!
    // 将其更改为你的姓名和学号。记得删除尖括号 "<" 和 ">"！
    printf_P(PSTR("CSSE2010/7201 Project by <YOUR NAME> - <YOUR STUDENT NUMBER>"));

    // Setup the start screen on the LED matrix.
    // 在 LED 矩阵上设置开始界面，显示欢迎动画或图案。
    setup_start_screen();

    // Clear button presses registered as the result of powering on the
    // I/O board. This is just to work around a minor limitation of the
    // hardware, and is only done here to ensure that the start screen is
    // not skipped when you power cycle the I/O board.
    // 清除由于上电 I/O 板而注册的按钮按下状态。这只是为了规避硬件的一个小限制，
    // 在这里这样做是为了确保在重新上电时不会跳过开始界面。
    clear_button_presses();

    // Wait until a button is pushed, or 's'/'S' is entered.
    // 等待直到有按钮被按下，或者在终端输入了 's'/'S'。
    while (1)
    {
        // Check for button presses. If any button is pressed, exit
        // the start screen by breaking out of this infinite loop.
        // 检查按钮按下状态。如果有任意按钮被按下，通过跳出这个无限循环来退出开始界面。
        if (button_pushed() != NO_BUTTON_PUSHED)
        {
            break;
        }

        // No button was pressed, check if we have terminal inputs.
        // 如果没有按钮按下，检查是否有来自终端的输入。
        if (serial_input_available())
        {
            // Terminal input is available, get the character.
            // 如果有终端输入，获取输入的字符。
            int serial_input = fgetc(stdin);

            // If the input is 's'/'S', exit the start screen by
            // breaking out of this loop.
            // 如果输入的是 's' 或 'S'，通过跳出循环退出开始界面。
            if (serial_input == 's' || serial_input == 'S')
            {
                break;
            }
        }

        // No button presses and no 's'/'S' typed into the terminal,
        // we will loop back and do the checks again. We also update
        // the start screen animation on the LED matrix here.
        // 如果没有按钮按下，也没有在终端输入 's' 或 'S'，我们会继续循环。
        // 同时，我们在这里更新 LED 矩阵上的开始界面动画。
        update_start_screen();
    }
}

void new_game(void)
{
    // Clear the serial terminal.
    // 清除串行终端内容。
    hide_cursor();
    clear_terminal();

    // Initialise the game and display.
    // 初始化游戏逻辑和显示。
    initialise_game();

    // Clear all button presses and serial inputs, so that potentially
    // buffered inputs aren't going to make it to the new game.
    // 清除所有按钮按下状态和串行输入，防止之前缓冲的输入影响新游戏的进行。
    clear_button_presses();
    clear_serial_input_buffer();
}

void play_game(void)
{
    uint32_t last_flash_time = get_current_time();  // 记录上一次闪烁的时间

    // We play the game until it's over.
    // 游戏主循环，直到游戏结束。
    while (!is_game_over())
    {
        // We need to check if any buttons have been pushed, this will
        // be NO_BUTTON_PUSHED if no button has been pushed. If button
        // 0 has been pushed, we get BUTTON0_PUSHED, and likewise, if
        // button 1 has been pushed, we get BUTTON1_PUSHED, and so on.
        // 检查是否有按钮被按下。如果没有按钮按下，将返回 NO_BUTTON_PUSHED。
        // 如果按钮 0 被按下，将返回 BUTTON0_PUSHED，依此类推。
        ButtonState btn = button_pushed();

        if (btn == BUTTON0_PUSHED)
        {
            // Move the player, see move_player(...) in game.c.
            // Also remember to reset the flash cycle here.
            // 移动玩家，具体逻辑参见 game.c 中的 move_player(...) 函数。
            // 另外，记得在这里重置玩家图标的闪烁循环。
            move_player(0, 1);
        }
        // Now, repeat for the other buttons, and combine with serial
        // inputs.
        // 现在，对其他按钮进行相同的处理，并结合串行输入。

        uint32_t current_time = get_current_time();
        if (current_time >= last_flash_time + 200)
        {
            // 200ms (0.2 seconds) has passed since the last time
            // we flashed the player icon, flash it now.
            // 自上次玩家图标闪烁以来已经过去了 200 毫秒，现在进行闪烁。
            flash_player();

            // Update the most recent icon flash time.
            // 更新最近一次闪烁的时间。
            last_flash_time = current_time;
        }
    }
    // We get here if the game is over.
    // 如果游戏结束，我们会到达这里。
}

void handle_game_over(void)
{
    // 在终端光标移动到指定位置，显示“游戏结束”。
    move_terminal_cursor(14, 10);
    printf_P(PSTR("GAME OVER"));
    move_terminal_cursor(15, 10);
    printf_P(PSTR("Press 'r'/'R' to restart, or 'e'/'E' to exit"));

    // Do nothing until a valid input is made.
    // 等待有效输入，不做任何其他操作。
    while (1)
    {
        // Get serial input. If no serial input is ready, serial_input
        // would be -1 (not a valid character).
        // 获取串行输入。如果没有输入可用，serial_input 将为 -1（表示无效字符）。
        int serial_input = -1;
        if (serial_input_available())
        {
            serial_input = fgetc(stdin);
        }

        // Check serial input.
        // 检查串行输入。
        if (toupper(serial_input) == 'R')
        {
            // <YOUR CODE HERE>
            // <在这里填写你的代码>
        }
        // Now check for other possible inputs.
        // 现在检查其他可能的输入。
    }
}
