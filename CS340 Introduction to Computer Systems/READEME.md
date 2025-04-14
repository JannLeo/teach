202504010011
后台姓名：谈源
用户ID：102424
用户1V1昵称：102424
学生需求类型：考前辅导
学生基础：一般
期望上课时间：美中周二上午10点开始有时间，除了12;30-13:50没时间，其他都OK
学生DUE时间：美中周三下午
用户类型：1v1新用户
院校：UIUC
年级：大三
专业：数学
科目代码：CS340
科目名称：Introduction to Computer Systems”
备注：学生代码这块需要重点讲讲，主要是举一反三这一块有点差，怕到时候考试遇到的题目不会做，辛苦老师也可以帮忙找找相关题目带着做一下，

![image-20250402101036232](READEME.assets/image-20250402101036232.png)

你上传的图片似乎是与计算机科学课程（CS 340）相关的幻灯片或海报。标题“Daemons, Zombies, and Deadlocks (The spooky side of CS)”表明，这部分内容讲解的是计算机科学中的一些概念，并使用了“恐怖”一词来进行有趣或主题化的表达。

以下是这些术语在计算机科学中的含义：

1. **Daemon（守护进程）**：在计算机中，守护进程是一个在后台运行的程序，通常不与用户直接交互。这些进程负责执行系统维护、处理网络请求或定期任务。守护进程的名称来源于“精灵”的概念，意味着它们像幽灵一样在后台默默运行。
2. **Zombie（僵尸进程）**：在计算机中，僵尸进程指的是已经执行完毕但仍然在进程表中占据一个条目的进程。它是一个“死”掉的进程，但并没有完全从系统中清除。这个概念类似于“死而复生”的僵尸。
3. **Deadlock（死锁）**：死锁是指在计算机系统中，两个或多个进程在等待对方释放资源时，导致系统进入无法继续执行的状态。这种情况会导致所有相关进程都无法继续，系统陷入“死锁”状态。

这张图片通过这些“恐怖”的主题，使得原本比较枯燥的计算机科学概念更加生动有趣，特别适合初学者学习。

![image-20250402101106582](READEME.assets/image-20250402101106582.png)

这张图片展示了与学习目标相关的内容，具体来说是计算机科学课程中有关线程（threads）和多线程（multithreading）方面的学习目标。以下是对每个目标的详细解释：

1. **Improve understanding of threads and other related vocabulary**（提高对线程及相关术语的理解）：
    这个目标旨在帮助学习者更好地理解“线程”这个概念以及与其相关的术语。线程是计算机程序中执行的最小单位，理解线程的基本概念和如何管理线程对于开发并发程序至关重要。
2. **Understanding thread safety concerns**（理解线程安全问题）：
    线程安全是指多个线程并发执行时，程序仍能保持正确性和稳定性的问题。学习者将学习如何避免和解决由于线程并发执行导致的数据竞争、资源共享冲突等问题。线程安全是编写高效、多线程程序的关键。
3. **Be able to analyze multithreading situations**（能够分析多线程场景）：
    该目标着重培养学习者在面对多线程编程时，能够分析程序的执行情况，识别潜在的问题，如死锁、竞态条件等，并提出有效的解决方案。

这些目标共同帮助学习者掌握多线程编程的基本概念及其应用，重点在于提升对并发和并行执行的理解，以及如何确保程序在多线程环境下的正确性。

![image-20250402101247967](READEME.assets/image-20250402101247967.png)

这张图片讲解了与线程相关的基本概念，具体内容如下：

1. **Thread（线程）**：
   - 定义：线程是指在同一个虚拟机（VM）中，具有独立程序计数器（PC）和寄存器的执行单元。每个线程可以在独立的程序计数器和寄存器中运行，允许多个线程共享同一虚拟机的内存空间。这意味着多个线程可以在同一个程序中并发执行，但每个线程有自己的执行路径。
   - 注释：图片中的“Same VM”与“separate PC and registers”是对线程的基本描述，表明线程共享虚拟机的内存空间，但每个线程有独立的程序计数器（PC）和寄存器。
2. **Concurrency（并发）**：
   - 定义：并发指的是两个或多个任务都已经开始执行，但并不意味着它们在同一时刻执行完毕。即多个任务在时间上重叠执行，但并不一定是同时进行的。
   - 注释：这段文字强调了并发任务的特点：它们开始执行了，但不一定在同一时刻完成。
3. **Parallel（并行）**：
   - 定义：并行指的是两个或多个任务在同一时刻都在执行，即它们都在同一时间内进行计算或处理。
   - 注释：这里强调了并行计算的特征：多个任务在同一时刻进展，通常需要多核或多处理器系统来同时处理多个任务。

这些概念是计算机科学中并发和多线程编程的基础，帮助理解如何在多任务环境中有效地组织和管理计算资源。

线程和进程是计算机操作系统中用于管理和调度执行任务的两种重要概念。它们有许多不同的特点，以下是它们的主要区别：

1. **基本定义**：
   - **进程**：进程是操作系统分配资源的基本单位，每个进程都有自己的内存空间、文件描述符、堆栈等资源。进程是操作系统中运行的一个程序的实例，可以包含一个或多个线程。
   - **线程**：线程是进程中的一个执行单元，多个线程可以共享同一个进程的内存空间。线程是 CPU 调度的基本单位。
2. **资源分配**：
   - **进程**：每个进程都有独立的内存空间和资源（如 CPU 时间、文件描述符等）。不同进程之间的资源是隔离的，进程之间的通信需要通过进程间通信（IPC）机制，如管道、消息队列、共享内存等。
   - **线程**：同一进程中的所有线程共享该进程的资源（如内存、文件描述符等），但每个线程有自己独立的寄存器、堆栈和程序计数器。线程之间的通信相对简单，可以通过共享内存等方式实现。
3. **开销**：
   - **进程**：由于进程具有独立的内存空间和资源，因此创建进程的开销较大，需要操作系统为其分配新的内存、资源等。
   - **线程**：线程创建和销毁的开销较小，因为它们共享进程的资源，不需要操作系统为其分配独立的内存空间。
4. **执行方式**：
   - **进程**：进程是操作系统分配和调度的基本单位，可以在不同的处理器上并行执行。在多核处理器的系统中，操作系统可以通过多进程来实现并行计算。
   - **线程**：线程是比进程更轻量的执行单位，一个进程内可以有多个线程，这些线程可以在同一时刻执行不同的任务，也可以通过时间片轮转在一个处理器上交替执行。
5. **通信方式**：
   - **进程**：进程之间的通信相对复杂，需要通过进程间通信（IPC）机制。
   - **线程**：同一进程内的线程可以直接共享内存和资源，因此线程之间的通信更为简单和高效。
6. **故障隔离**：
   - **进程**：由于进程间资源独立，一个进程的崩溃不会直接影响其他进程。
   - **线程**：由于线程共享进程的资源，一个线程的崩溃可能会导致整个进程崩溃，因为它可能破坏了进程的共享资源（如内存）。

**总结**：

- 进程是一个独立的资源分配单位，每个进程拥有独立的内存和资源，开销较大，适用于需要独立执行的任务。
- 线程是进程内的执行单元，多个线程共享同一进程的资源，创建和销毁开销较小，适用于需要并发执行的任务。

在现代操作系统中，进程和线程通常是并行工作，共同完成复杂的任务。

### allocator.c

这段代码实现了一个简单的内存池分配器，通过手动管理内存块来模拟 `malloc`、`free` 和 `realloc` 等标准内存分配功能。它使用一个链表 `free_list` 来管理空闲内存块，通过内存合并和拆分来优化内存的使用和避免内存碎片问题。

```c
#include <stdio.h>
#include <string.h>
#include <stdlib.h>

// 定义内存块的结构体
typedef struct Block {
  size_t size;         // 当前块的大小
  struct Block *next;  // 指向下一个块的指针
  int free_data;       // 标志块是否空闲（1为空闲，0为已分配）
} Block;

// 定义内存对齐的常量
#define ALIGNMENT 8

// 定义内存对齐的宏，确保大小是ALIGNMENT的倍数
#define ALIGN(size) (((size) + (ALIGNMENT - 1)) & ~(ALIGNMENT - 1))

// 定义Block结构体的大小
#define BLOCK_SIZE sizeof(Block)

// 定义内存池的大小（10MB）
#define POOL_SIZE (1024*1024*10)

// 全局变量定义
static void *base = NULL;  // 指向内存池的基地址
static Block *free_list = NULL;  // 空闲块链表的头指针
static size_t used = 0;  // 已分配的内存大小

// 初始化内存池，传入的newbase是内存池的起始地址
void allocator_init(void *newbase) {
  base = newbase;
  free_list = NULL;  // 空闲链表为空
  used = 0;  // 已使用的内存大小为0
}

// 重置内存池，清空空闲链表和已用内存
void allocator_reset() {
  free_list = NULL;
  used = 0;
}

// 将空闲块插入到空闲链表，并按地址升序排序
static void insert_block_sorted(Block *block) {
  if (!free_list) {  // 如果空闲链表为空
    free_list = block;
    block->next = NULL;
    return;
  }
  if (block < free_list) {  // 如果块地址小于链表头部
    block->next = free_list;
    free_list = block;
    return;
  }
  Block *cur = free_list;
  // 遍历链表，找到插入的位置
  while (cur->next && cur->next < block) {
    cur = cur->next;
  }
  block->next = cur->next;
  cur->next = block;
}

// 合并与下一个相邻的空闲块
static void merge_with_next(Block *block) {
    Block *next = block->next;
    if (!next) {
      return;  // 如果没有下一个块，直接返回
    }
    // 判断当前块与下一个块是否相邻
    char *block_end = (char*)block + BLOCK_SIZE + block->size;
    if ((char*)next == block_end) {
        // 合并当前块与下一个块
        block->size += BLOCK_SIZE + next->size;
        block->next = next->next;
    }
}

// 尝试合并当前块与前后的空闲块
static void try_merge(Block *block) {
    merge_with_next(block);  // 合并当前块与下一个空闲块
    if (block != free_list) {  // 如果当前块不是链表的头部
      Block *prev = free_list;
      // 遍历链表，找到当前块的前一个块
      while (prev && prev->next && prev->next < block) {
        prev = prev->next;
      }
      if (prev && prev->next == block) {
        // 合并当前块与前一个块
        merge_with_next(prev);
      }
    }
}

// 查找一个合适的空闲块，满足给定的大小
Block* find_free_block(size_t size) {
  Block *prev = NULL;
  Block *cur  = free_list;
  // 遍历空闲链表，查找符合要求的空闲块
  while (cur) {
    if (cur->size >= size && cur->free_data) {
      // 如果找到的块足够大，且是空闲的
      if (cur->size >= size + BLOCK_SIZE + ALIGNMENT) {
        // 如果当前块的大小大于所需大小，进行拆分
        Block *new_block = (Block *)((char*)cur + BLOCK_SIZE + size);
        new_block->size = cur->size - size - BLOCK_SIZE;
        new_block->free_data = 1;
        new_block->next = cur->next;
        cur->next = new_block;
        cur->size = size;
      }
      // 移除当前块，并标记为已分配
      if (prev) {
        prev->next = cur->next;
      } else {
        free_list = cur->next;
      }
      cur->free_data = 0;
      cur->next = NULL;
      return cur;
    }
    prev = cur;
    cur = cur->next;
  }
  return NULL;
}

// 自定义的malloc函数，分配指定大小的内存
void *mymalloc(size_t size) {
    if (!base || size == 0) {
      return NULL;  // 如果内存池未初始化或请求大小为0，返回NULL
    }
    size = ALIGN(size);  // 确保内存对齐
    Block *block = find_free_block(size);  // 查找空闲块
    if (block) {
        return (block + 1);  // 返回分配的内存地址
    }
    if (used + BLOCK_SIZE + size > POOL_SIZE) {
        return NULL;  // 如果内存池空间不足，返回NULL
    }
    block = (Block*)((char*)base + used);  // 在内存池末尾分配新块
    block->size = size;
    block->free_data = 0;
    block->next = NULL;
    used += BLOCK_SIZE + size;  // 更新已使用的内存大小
    return (void*)(block + 1);  // 返回内存块的实际数据地址
}

// 自定义的free函数，释放指定内存块
void myfree(void *ptr) {
    if (!ptr) {
      return;  // 如果指针为空，什么都不做
    }
    Block *block = (Block*)ptr - 1;  // 获取块的头部
    block->free_data = 1;  // 标记为已空闲
    insert_block_sorted(block);  // 插入到空闲链表
    try_merge(block);  // 尝试合并相邻的空闲块
}

// 自定义的realloc函数，重新分配内存
void *myrealloc(void *ptr, size_t size) {
    if (ptr == NULL) {
        return mymalloc(size);  // 如果原指针为空，直接分配新内存
    }
    if (size == 0) {
        myfree(ptr);  // 如果新大小为0，释放原内存并返回NULL
        return NULL;
    }
    Block *block = (Block*)ptr - 1;  // 获取块的头部
    size = ALIGN(size);  // 确保内存对齐
    char *block_end = (char*)block + BLOCK_SIZE + block->size;
    char *heap_end  = (char*)base + used;  // 获取内存池末尾地址
    // 如果原块在内存池的末尾，直接调整其大小
    if (block_end == heap_end) {
      size_t diff = block->size - size;
      block->size = size;
      used -= diff;  // 更新已使用的内存大小
    }
    void *new_ptr = mymalloc(size);  // 分配新内存
    if (new_ptr) {
        memcpy(new_ptr, ptr, block->size < size ? block->size : size);  // 拷贝数据
        myfree(ptr);  // 释放原内存
    }
    return new_ptr;  // 返回新分配的内存
}

```

这段代码是一个简单的 HTTP 请求解析器的实现。它主要的功能是从网络连接中读取 HTTP 请求数据，并解析出请求头、请求方法、路径、版本以及请求体（如果有的话）。代码定义了一些函数和结构体来处理 HTTP 请求的各个方面，包括读取数据、解析请求头和处理请求的各个部分。

以下是您提供的 C 语言代码，已经用中文注释详细说明了每个函数和代码块的作用：

```c
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <stdio.h>

#include "http.h"

// 辅助函数：去除字符串前面的空格或制表符
static char *trim_leading_spaces(char *str) {
    while (*str == ' ' || *str == '\t') {
        str++;  // 跳过前面的空格或制表符
    }
    return str;
}

/**
 * httprequest_parse_headers
 * 
 * 解析 HTTP 请求的头部并将解析后的数据填充到 `req` 结构中。
 * 返回值是从 `buffer` 中读取并解析的字节数。
 */
ssize_t httprequest_parse_headers(HTTPRequest *req, char *buffer, ssize_t buffer_len) {
    // 创建一个缓冲区副本，以免修改原始缓冲区
    char *buf_copy = malloc(buffer_len + 1);
    if (!buf_copy) {
        return -1;  // 内存分配失败，返回错误
    }
    memcpy(buf_copy, buffer, buffer_len);
    buf_copy[buffer_len] = '\0';  // 为缓冲区副本添加结尾的空字符

    // 查找 HTTP 请求头的结束标志 "\r\n\r\n"
    char *header_end = strstr(buf_copy, "\r\n\r\n");
    if (!header_end) {
        free(buf_copy);
        return -1;  // 如果没有找到请求头的结束标志，返回错误
    }

    // 计算请求头的长度，并获取请求体的位置
    ssize_t headers_len = header_end - buf_copy + 4;
    char *payload_ptr = buf_copy + headers_len;

    // 为请求头部分分配内存
    char *headers_section = malloc(headers_len + 1);
    if (!headers_section) {
        free(buf_copy);
        return -1;
    }
    memcpy(headers_section, buf_copy, headers_len);
    headers_section[headers_len] = '\0';  // 为请求头部分添加结尾的空字符

    // 解析请求头的每一行
    char *saveptr;
    char *line = strtok_r(headers_section, "\r\n", &saveptr);
    if (!line) {
        free(buf_copy);
        free(headers_section);
        return -1;
    }

    // 解析请求行：方法、路径和版本
    char *method = strtok(line, " ");
    char *path = strtok(NULL, " ");
    char *version = strtok(NULL, " ");
    if (!method || !path || !version) {
        free(buf_copy);
        free(headers_section);
        return -1;
    }

    // 将解析后的方法、路径和版本存储到 req 结构中
    req->action = strdup(method);
    req->path = strdup(path);
    req->version = strdup(version);
    req->payload = NULL;
    req->headers = NULL;

    // 确保所有 strdup() 调用成功
    if (!req->action || !req->path || !req->version) {
        free(buf_copy);
        free(headers_section);
        httprequest_destroy(req);  // 释放已经分配的内存
        return -1;
    }

    int content_length = 0;
    // 解析请求头中的其他字段
    while ((line = strtok_r(NULL, "\r\n", &saveptr)) != NULL) {
        char *colon = strchr(line, ':');
        if (!colon) {
            continue;  // 如果没有冒号，跳过该行
        }

        *colon = '\0';  // 分割出头部的 key 和 value
        char *key = line;
        char *value = colon + 1;
        value = trim_leading_spaces(value);  // 去掉 value 前面的空格

        // 创建一个新的 HeaderNode 节点并填充数据
        HeaderNode *node = malloc(sizeof(HeaderNode));
        if (!node) {
            free(buf_copy);
            free(headers_section);
            httprequest_destroy(req);
            return -1;
        }

        node->key = strdup(key);
        node->value = strdup(value);
        if (!node->key || !node->value) {
            free(node->key);
            free(node->value);
            free(node);
            httprequest_destroy(req);
            free(buf_copy);
            free(headers_section);
            return -1;
        }

        node->next = req->headers;
        req->headers = node;  // 将新的头部节点插入到头部链表的前面

        // 如果头部字段是 "Content-Length"，解析其值
        if (strcasecmp(key, "Content-Length") == 0) {
            content_length = atoi(value);  // 将 Content-Length 转换为整数
        }
    }

    // 如果请求体存在，根据 Content-Length 读取请求体
    if (content_length > 0) {
        if (headers_len + content_length > buffer_len) {
            free(buf_copy);
            free(headers_section);
            httprequest_destroy(req);
            return -1;
        }

        // 为请求体分配内存
        char *temp_payload = malloc(content_length + 1);
        if (!temp_payload) {
            free(buf_copy);
            free(headers_section);
            httprequest_destroy(req);
            return -1;
        }

        memcpy(temp_payload, payload_ptr, content_length);  // 将请求体复制到分配的内存中
        temp_payload[content_length] = '\0';  // 添加结尾的空字符
        req->payload = temp_payload;
    }

    // 释放缓冲区和请求头部分的内存
    free(buf_copy);
    free(headers_section);
    return headers_len + content_length;  // 返回已处理的字节数
}

/**
 * httprequest_read
 * 
 * 从套接字中读取数据并填充到 `req` 结构中。
 * 返回从套接字读取并处理的字节数。
 */
#define READ_BLOCK_SIZE 4096

ssize_t httprequest_read(HTTPRequest *req, int sockfd) {
    size_t capacity = 8192;  // 初始缓冲区大小
    char *buffer = malloc(capacity);
    if (!buffer) {
        return -1;  // 内存分配失败，返回错误
    }

    ssize_t total_read = 0;
    ssize_t parse_result = -1;

    while (1) {
        // 如果缓冲区不够大，则扩展缓冲区
        if ((size_t)total_read + READ_BLOCK_SIZE > capacity) {
            size_t new_capacity = capacity * 2;
            char *tmp = realloc(buffer, new_capacity);
            if (!tmp) {
                return -1;  // 内存重新分配失败，返回错误
            }
            buffer = tmp;
            capacity = new_capacity;
        }

        // 从套接字中读取数据
        ssize_t bytes_read = read(sockfd, buffer + total_read, READ_BLOCK_SIZE);
        if (bytes_read < 0) {
            free(buffer);
            return -1;  // 读取失败，返回错误
        }
        if (bytes_read == 0) {
            // 如果没有更多数据，尝试解析 HTTP 请求头
            parse_result = httprequest_parse_headers(req, buffer, total_read);
            free(buffer);
            if (parse_result >= 0) {
                return total_read;  // 如果解析成功，返回读取的字节数
            }
            return -1;  // 解析失败，返回错误
        }

        total_read += bytes_read;  // 累加已读取的字节数
        parse_result = httprequest_parse_headers(req, buffer, total_read);
        if (parse_result >= 0) {
            free(buffer);
            return total_read;  // 如果解析成功，返回读取的字节数
        }
    }

    free(buffer);
    return -1;  // 解析失败，返回错误
}

/**
 * httprequest_get_action
 * 
 * 返回 HTTP 请求的动作（例如 GET、POST 等）。
 */
const char *httprequest_get_action(HTTPRequest *req) {
  return req->action;
}

/**
 * httprequest_get_header
 * 
 * 返回 HTTP 请求中指定 `key` 的头部字段的值。
 */
const char *httprequest_get_header(HTTPRequest *req, const char *key) {
  if (!req || !key) {
    return NULL;  // 如果请求或关键字为空，返回 NULL
  }
  HeaderNode *current = req->headers;
  while (current) {
    if (current->key && strcasecmp(current->key, key) == 0) {
      return current->value;  // 如果找到匹配的头部字段，返回其值
    }
    current = current->next;
  }
  return NULL;  // 如果没有找到匹配的头部字段，返回 NULL
}

/**
 * httprequest_get_path
 * 
 * 返回 HTTP 请求的路径（例如 "/index.html"）。
 */
const char *httprequest_get_path(HTTPRequest *req) {
  if (!req) {
    return NULL;  // 如果请求为空，返回 NULL
  }
  return req->path;
}

/**
 * httprequest_destroy
 * 
 * 释放与 `req` 相关的所有内存。
 */
void httprequest_destroy(HTTPRequest *req) {
  if (!req) { 
    return;  // 如果请求为空，什么都不做
  }
  // 释放请求中各个成员的内存
  free((void *)req->action);
  free((void *)req->path);
  free((void *)req->version);
  free((void *)req->payload);

  // 释放请求头链表中的所有节点
  HeaderNode *current = req->headers;
  while (current) {
    HeaderNode *next = current->next;
    if (current->key) {
      free(current->key);  // 释放头部字段的 key
    }  
    if (current->value) {
      free(current->value);  // 释放头部字段的 value
    }
    free(current);  // 释放当前头部节点
    current = next;
  }
  req->headers = NULL;  // 设置头部为 NULL
}
```

### 主要功能总结：

1. **`httprequest_parse_headers`**：解析 HTTP 请求的头部并将信息存入 `req`。
2. **`httprequest_read`**：从套接字读取数据并调用 `httprequest_parse_headers` 解析 HTTP 请求。
3. **`httprequest_get_action`**：返回 HTTP 请求的动作（如 GET、POST）。
4. **`httprequest_get_header`**：返回请求中指定头部字段的值。
5. **`httprequest_get_path`**：返回请求的路径部分（例如 `/index.html`）。
6. **`httprequest_destroy`**：销毁请求，释放与其相关的所有内存。

代码的核心任务是通过解析 HTTP 请求的各个部分来填充 `HTTPRequest` 结构体，处理请求方法、路径、版本、头部信息和请求体。





/ 获取用户输入
      Input              / 输入X
      STORE InputX     / 将X存储到InputX地址
      Input              / 输入Y
      STORE InputY     / 将Y存储到InputY地址
      Input              / 输入操作符
      STORE Operation  / 将操作符存储到Operation地址

/ 检查操作符
      LOAD Operation   / 加载操作符
      SUBT ASCII_a      / 如果操作符是‘a’，执行加法
      SKIPCOND 400      / 如果操作符是‘a’，跳转到加法子程序
      JUMP Subtract     / 否则执行减法子程序

/ 加法子程序
Add,  LOAD InputX      / 加载X
      ADD InputY       / 加X和Y
      JUMP PrintResult  / 跳转并输出结果

/ 减法子程序
Subtract,  LOAD InputX  / 加载X
           SUBT InputY  / 执行X - Y
           JUMP PrintResult  / 跳转并输出结果

/ 输出结果
PrintResult,  Output     / 输出结果
             HALT    / 程序结束

/ ASCII 值
ASCII_a, DEC 97     / 字符'a'的ASCII值
InputX,  DEC 0         / 存储第一个输入X
InputY,  DEC 0         / 存储第二个输入Y
Operation, DEC 0       / 存储操作符（‘a’或‘s’）
END