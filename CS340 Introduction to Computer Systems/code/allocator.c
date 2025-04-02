#include <stdio.h>
#include <string.h>
#include <stdlib.h>

typedef struct Block {
  size_t size;
  struct Block *next;
  int free_data;
} Block;

#define ALIGNMENT 8
#define ALIGN(size) (((size) + (ALIGNMENT - 1)) & ~(ALIGNMENT - 1))
#define BLOCK_SIZE sizeof(Block)
#define POOL_SIZE (1024*1024*10)

static void *base = NULL;
static Block *free_list = NULL;  
static size_t used = 0;

void allocator_init(void *newbase) {
  base = newbase;
  free_list = NULL;
  used = 0;
}

void allocator_reset() {
  free_list = NULL;
  used = 0;
}
static void insert_block_sorted(Block *block) {
  if (!free_list) {
    free_list = block;
      block->next = NULL;
      return;
    }
    if (block < free_list) {
        block->next = free_list;
        free_list = block;
        return;
    }
    Block *cur = free_list;
    while (cur->next && cur->next < block) {
        cur = cur->next;
    }
    block->next = cur->next;
    cur->next = block;
}
//Merge adjacent free data blocks and i also use this function as a helper function for the try_merge function.
static void merge_with_next(Block *block) {
    Block *next = block->next;
    if (!next) {
      return;
    }
    char *block_end = (char*)block + BLOCK_SIZE + block->size;
    if ((char*)next == block_end) {
        block->size += BLOCK_SIZE + next->size;
        block->next = next->next;
    }
}

static void try_merge(Block *block) { // use the previous function for recursion
    merge_with_next(block);
    if (block != free_list) {
      Block *prev = free_list;
      while (prev && prev->next && prev->next < block) {
        prev = prev->next;
      }
      if (prev && prev->next == block) {
        merge_with_next(prev);
      }
    }
}
Block* find_free_block(size_t size) {
  Block *prev = NULL;
  Block *cur  = free_list;
  while (cur) {
    if (cur->size >= size && cur->free_data) {
      if (cur->size >= size + BLOCK_SIZE + ALIGNMENT) {
        Block *new_block = (Block *)((char*)cur + BLOCK_SIZE + size);
        new_block->size = cur->size - size - BLOCK_SIZE;
        new_block->free_data = 1;
        new_block->next = cur->next;
        cur->next = new_block;
        cur->size = size;
        }//this block is too large, so use this to split.
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
void *mymalloc(size_t size) {
    if (!base || size == 0) {
      return NULL;
    }
    size = ALIGN(size);
    Block *block = find_free_block(size);
    if (block) {
        return (block + 1);
    }
    if (used + BLOCK_SIZE + size > POOL_SIZE) {
        return NULL; 
    }
    block = (Block*)((char*)base + used);
    block->size = size;
    block->free_data = 0;
    block->next = NULL;
    used += BLOCK_SIZE + size;
    return (void*)(block + 1);
}
void myfree(void *ptr) {
    if (!ptr) {
      return;
    }
    Block *block = (Block*)ptr - 1;
    block->free_data = 1;
    insert_block_sorted(block);
    try_merge(block);//use the helper function to make this function easy.
}

void *myrealloc(void *ptr, size_t size) {
    if (ptr == NULL) {
        return mymalloc(size);
    }
    if (size == 0) {
        myfree(ptr);
        return NULL;
    }
    Block *block = (Block*)ptr - 1;
    size = ALIGN(size);
    char *block_end = (char*)block + BLOCK_SIZE + block->size;
    char *heap_end  = (char*)base + used;//to make sure that shrink at the end
    if (block_end == heap_end) {
      size_t diff = block->size - size;
      block->size = size;
      used -= diff;
    }
    void *new_ptr = mymalloc(size);
    if (new_ptr) {
        memcpy(new_ptr, ptr, block->size < size ? block->size : size);
        myfree(ptr);
    }
    return new_ptr;
}
