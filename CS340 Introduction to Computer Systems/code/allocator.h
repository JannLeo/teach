#include <stddef.h>

// /** Called once before any other function here; argument is the smallest usable address */
// void allocator_init(void *base);

// /** Called once before each test case; should free any used memory and reset for the next test */
// void allocator_reset();

// /** Like malloc but using the memory provided to allocator_init */
// void *mymalloc(size_t size);
// /** Like free but using the memory provided to allocator_init */
// void myfree(void *ptr);
// /** Like realloc but using the memory provided to allocator_init */
// void *myrealloc(void *ptr, size_t size);

#define ALIGNMENT 8
#define POOL_SIZE (1024*1024*10)
void  allocator_init(void *newbase);
void  allocator_reset(void);

void *mymalloc(size_t size);
void  myfree(void *ptr);
void *myrealloc(void *ptr, size_t size);