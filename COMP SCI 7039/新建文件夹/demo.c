#include <stdlib.h>     // 标准库头文件
#include <stdio.h>      // 输入输出函数
#include <stdbool.h>    // 布尔类型支持
#include "emulator.h"   // 模拟器接口头文件
#include "sr.h"         // 网络层相关定义
#include <string.h>     // 字符串操作函数

/* ​**​*​**​*​**​*​**​*​**​*​**​*​**​*​**​*​**​*​**​*​**​*​**​*​**​*​**​*​**​*​**​*​**​*​**​*​**​*​**​*​**​*​**​*
   Go Back N协议实现（基于J.F.Kurose的教材）
   修改说明：
   - 移除双向GBN代码和其他未使用的部分
   - 调整代码风格至当前规范
   - 添加GBN具体实现
​**​*​**​*​**​*​**​*​**​*​**​*​**​*​**​*​**​*​**​*​**​*​**​*​**​*​**​*​**​*​**​*​**​*​**​*​**​*​**​*​**​*​**​*​**​**/

// 定义网络参数
#define RTT  16.0       // 往返时间（单位：时间单元）
#define WINDOWSIZE 6    // 发送窗口最大容量（未确认包数量）
#define SEQSPACE 7      // 序列号空间大小（必须>=窗口大小+1）
#define NOTINUSE (-1)   // 表示头部字段未使用的特殊值

/* 计算数据包校验和的通用函数（发送方和接收方均使用）
   模拟器会覆盖部分数据为'z'，但不会修改原始校验和 */
static struct pkt recv_buffer[RECV_WINDOWSIZE];  // 接收缓冲区
static int recv_base = 0;                      // 接收窗口起始位置
static int received[RECV_WINDOWSIZE];          // 记录接收缓冲区各位置状态
static bool acked[SEQSPACE];                   // 记录已确认的发送包状态

int ComputeChecksum(struct pkt packet) {
  int checksum = 0;
  int i;
  
  // 校验和计算方法：序列号 + 确认号 + 所有数据载荷
  checksum = packet.seqnum;
  checksum += packet.acknum;
  for (i=0; i<20; i++) 
    checksum += (int)(packet.payload[i]);  // 将字符转换为整数累加

  return checksum;
}

// 判断数据包是否损坏
bool IsCorrupted(struct pkt packet) {
  return (packet.checksum != ComputeChecksum(packet));  // 校验和不匹配则损坏
}

// 发送方A的缓冲区和状态变量
static struct pkt buffer[SEQSPACE];       // 发送缓冲区
static int window_base = 0;               // 发送窗口起始位置
static int windowcount = 0;               // 当前窗口中未确认的包数量
static int A_nextseqnum = 0;              // 下一个要发送的序列号
static int current_timer_seq = -1;        // 当前正在计时的包序列号

/* 应用层调用此函数发送数据 */
void A_output(struct msg message) {
    struct pkt sendpkt;
    int i;

    // 窗口未满时发送新数据包
    if (windowcount < WINDOWSIZE) {
        if (TRACE > 1)
            printf("----A: 新消息到达，发送窗口未满，发送新消息到网络层！\n");

        // 构造数据包
        sendpkt.seqnum = A_nextseqnum;      // 设置序列号
        sendpkt.acknum = NOTINUSE;          // 发送方不使用确认号
        for (i=0; i<20; i++) 
            sendpkt.payload[i] = message.data[i];  // 复制数据
        sendpkt.checksum = ComputeChecksum(sendpkt);  // 计算校验和

        // 缓存数据包并标记为未确认
        buffer[sendpkt.seqnum] = sendpkt;
        acked[sendpkt.seqnum] = false;
        windowcount++;  // 窗口计数增加

        // 输出发送信息
        if (TRACE > 0)
            printf("向层3发送数据包 %d\n", sendpkt.seqnum);
        tolayer3(A, sendpkt);  // 传递给网络层

        // 启动第一个包的定时器
        if (windowcount == 1) {
            current_timer_seq = sendpkt.seqnum;
            starttimer(A, RTT);
        }
        A_nextseqnum = (A_nextseqnum + 1) % SEQSPACE;  // 更新下一个序列号
    } else {
        // 窗口已满时的处理
        if (TRACE > 0)
            printf("----A: 新消息到达，发送窗口已满\n");
        window_full++;
    }
}

// 启动下一个未确认包的定时器
void StartTimerForNextUnackedPacket() {
    int i;
    for (i = 0; i < SEQSPACE; i++) {
        int seq = (window_base + i) % SEQSPACE;
        if (!acked[seq] && i < windowcount) {
            current_timer_seq = seq;
            starttimer(A, RTT);
            if (TRACE > 2)
                printf("----A: 为数据包 %d 启动定时器\n", seq);
            break;
        }
    }
}

// 停止指定序列号的定时器并启动下一个
void StopTimerIfAcked(int acknum) {
    if (acknum == current_timer_seq) {
        if (TRACE > 2)
            printf("----A: 停止数据包 %d 的定时器\n", acknum);
        stoptimer(A);
        current_timer_seq = -1;
        StartTimerForNextUnackedPacket();  // 启动下一个定时器
    }
}

/* 处理来自层3的输入（本实验中只有ACK） */
void A_input(struct pkt packet) {
    int win_start, win_end;
    bool in_window;
    
    // 检查ACK是否损坏
    if (!IsCorrupted(packet)) {
        if (TRACE > 0)
            printf("----A: 收到未损坏的ACK %d\n", packet.acknum);
        total_ACKs_received++;

        // 计算当前窗口范围
        win_start = window_base;
        win_end = (window_base + WINDOWSIZE) % SEQSPACE;
        in_window = (win_start < win_end) ?
                     (packet.acknum >= win_start && packet.acknum < win_end) :
                     (packet.acknum >= win_start || packet.acknum < win_end);

        // 检查ACK是否在窗口内
        if (!in_window) {
            if (TRACE > 2)
                printf("----A: ACK %d 超出窗口范围 [%d, %d)，忽略\n", 
                       packet.acknum, win_start, win_end);
            return;
        }

        // 处理有效ACK
        if (!acked[packet.acknum]) {
            if (TRACE > 0)
                printf("----A: 收到新的ACK %d\n", packet.acknum);
            acked[packet.acknum] = true;  // 标记为已确认
            new_ACKs++;

            // 停止对应定时器
            StopTimerIfAcked(packet.acknum);

            // 滑动窗口
            while (windowcount > 0 && acked[window_base]) {
                acked[window_base] = false;
                window_base = (window_base + 1) % SEQSPACE;
                windowcount--;
            }
        } else {
            if (TRACE > 0)
                printf("----A: 收到重复ACK %d，不做处理\n", packet.acknum);
        }
    } else {
        if (TRACE > 0)
            printf("----A: 收到损坏的ACK，忽略\n");
    }
}

/* 处理定时器中断（超时重传） */
void A_timerinterrupt(void) {
    if (TRACE > 0)
        printf("----A: 超时，重新发送数据包！\n");

    // 重传当前定时器对应的包
    if (!acked[current_timer_seq]) {
        if (TRACE > 0)
            printf("---A: 重传数据包 %d\n", buffer[current_timer_seq].seqnum);
        tolayer3(A, buffer[current_timer_seq]);  // 重新发送
        packets_resent++;
    }
    StartTimerForNextUnackedPacket();  // 启动下一个定时器
}

/* 初始化发送方A */
void A_init(void) {
    int i;
    
    // 初始化窗口状态
    A_nextseqnum = 0;  // 发送方初始序列号为0
    windowcount = 0;

    // 初始化确认状态数组
    for (i = 0; i < SEQSPACE; i++) {
        acked[i] = false;
    }
}

/​**​*​**​*​**​* 接收方B的变量和过程 ​**​*​**​*​**​*​**​*/

// 接收方B的状态变量
// static int expectedseqnum;  // 注释掉的预期序列号变量
static int B_nextseqnum;      // 下一个期望的序列号

/* 处理来自层3的输入（本实验中只有数据包） */
void B_input(struct pkt packet) {
    struct pkt sendpkt;
    int i;
    int seqnum = packet.seqnum;
    int rel_pos = (seqnum - recv_base + SEQSPACE) % SEQSPACE;  // 相对接收窗口的位置

    // 构造ACK包
    sendpkt.seqnum = B_nextseqnum;
    B_nextseqnum = (B_nextseqnum + 1) % 2;  // 接收方使用0/1交替的ACK
    for (i = 0; i < 20; i++) 
        sendpkt.payload[i] = '0';  // 填充数据

    // 检查数据包有效性及是否在窗口内
    if (!IsCorrupted(packet) && rel_pos < RECV_WINDOWSIZE) {
        if (TRACE > 0)
            printf("----B: 正确接收到数据包 %d，发送ACK！\n", seqnum);
        packets_received++;

        // 缓存数据包到接收窗口
        if (!received[rel_pos]) {
            recv_buffer[rel_pos] = packet;
            received[rel_pos] = 1;
            if (TRACE > 2)
                printf("----B: 将数据包 %d 缓存到位置 %d\n", seqnum, rel_pos);
        }
        sendpkt.acknum = seqnum;  // ACK确认当前接收的包
    } else {
        if (TRACE > 0)
            printf("----B: 数据包损坏或序列号不符，重传ACK！\n");
        sendpkt.acknum = seqnum;  // 发送重复ACK
    }
    sendpkt.checksum = ComputeChecksum(sendpkt);  // 计算ACK校验和
    tolayer3(B, sendpkt);  // 发送ACK到网络层

    // 滑动接收窗口并交付数据
    while (received[0]) {
        tolayer5(B, recv_buffer[0].payload);  // 交付数据到应用层
        if (TRACE > 2)
            printf("----B: 将数据包 %d 交付到层5\n", recv_base);

        // 滑动窗口
        for (i = 0; i < RECV_WINDOWSIZE - 1; i++) {
            received[i] = received[i + 1];
            recv_buffer[i] = recv_buffer[i + 1];
        }
        received[RECV_WINDOWSIZE - 1] = 0;
        recv_base = (recv_base + 1) % SEQSPACE;
        
        if (TRACE > 2)
            printf("----B: 接收窗口滑动到基地址 %d\n", recv_base);
    }
}

/* 初始化接收方B */
void B_init(void) {
    recv_base = 0;  // 接收窗口起始位置
    memset(received, 0, sizeof(received));  // 初始化接收状态数组
    B_nextseqnum = 1;  // 接收方初始ACK序列号设为1
}

/​**​*​**​*​**​*​**​*​**​*​**​*​**​*​**​*​**​*​**​*​**​*​**​*​**​*​**​*​**​*​**​*​**​*​**​*​**​*​**​*​**​*​**​*​**​*​**​*​**​*​**​*
 * 双向通信相关函数（本实验未使用） *
 ​**​*​**​*​**​*​**​*​**​*​**​*​**​*​**​*​**​*​**​*​**​*​**​*​**​*​**​*​**​*​**​*​**​*​**​*​**​*​**​*​**​*​**​*​**​*​**​*​**​*​**​/

// 注释掉的双向通信函数
void B_output(struct msg message)  { /* 空实现 */ }
void B_timerinterrupt(void)        { /* 空实现 */ }