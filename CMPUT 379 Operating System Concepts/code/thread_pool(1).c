
#include "threadpool.h"
#include <stdlib.h>
#include <stdio.h>
#include <pthread.h>
#include <stdbool.h>

typedef struct {
    pthread_t* threads;
    pthread_mutex_t lock;
    ThreadPool_job_queue_t jobs;
    pthread_cond_t note;
    bool shutdown;
    unsigned int thread_count;
} ThreadPool_current;

void* thread_worker(void* arg) {
    ThreadPool_current* tp = (ThreadPool_current*)arg;
}

ThreadPool_current*ThreadPool_create(unsigned int num){
    ThreadPool_current *pool = malloc(sizeof(ThreadPool_current));
    if (!pool) return NULL;

    pool->threads = malloc(sizeof(pthread_t) * num);
    pool->jobs.size = 0;
    pool->jobs.head = NULL;
    pthread_mutex_init(&pool->lock, NULL);
    pthread_cond_init(&pool->note, NULL);
    pool->shutdown = false;
    pool->thread_count = num;

    for (unsigned int i = 0; i < num; i++) {
        pthread_create(&pool->threads[i], NULL, thread_worker, (void*)pool);
    }

    return pool;
}

void ThreadPool_destroy(ThreadPool_current* tp){
    if (!tp) return;
    pthread_mutex_lock(&tp->jobs.lock);
    tp->shutdown = true;   
    pthread_cond_broadcast(&tp->jobs.note); 
    pthread_mutex_unlock(&tp->jobs.lock);

    for (unsigned int i = 0; i < tp->thread_count; i++) {
        pthread_join(tp->threads[i], NULL);
    }

    free(tp->threads);

    ThreadPool_job_t* current = tp->jobs.head;
    while (current) {
        ThreadPool_job_t* tmp = current;
        current = current->next;
        free(tmp);
    }
    pthread_mutex_destroy(&tp->jobs.lock);
    pthread_cond_destroy(&tp->jobs.note);
}

bool ThreadPool_add_job(ThreadPool_t* tp, thread_func_t func, void* arg){
    if (!tp || !func) return false;

    ThreadPool_job_t* job = (ThreadPool_job_t*)malloc(sizeof(ThreadPool_job_t));
    if (!job) return false;

    job->func = func;
    job->arg = arg;
    job->next = NULL;


    pthread_mutex_lock(&tp->lock);

    if (tp->jobs.head == NULL) {
        tp->jobs.head = job;
    } else {
        ThreadPool_job_t* tail = tp->jobs.head;
        while (tail->next) tail = tail->next;
        tail->next = job;
    }

    tp->jobs.size++;  

    pthread_cond_signal(&tp->note);
    pthread_mutex_unlock(&tp->lock);

    return true;
}


ThreadPool_job_t* ThreadPool_get_job(ThreadPool_current* tp){
    if (!tp) return NULL;

    pthread_mutex_lock(&tp->lock);

    while (tp->jobs.size == 0 && !tp->shutdown) {
        pthread_cond_wait(&tp->note, &tp->lock);
    }
    if (tp->shutdown && tp->jobs.size == 0) {
        pthread_mutex_unlock(&tp->lock);
        return NULL;
    }

    ThreadPool_job_t* job = tp->jobs.head;
    if (job) {
        tp->jobs.head = job->next;
        tp->jobs.size--;   
        job->next = NULL;
    }

    pthread_mutex_unlock(&tp->lock);  
    return job;
}

void* Thread_run(ThreadPool_current* tp){
    if (!tp) return NULL;

    while (1) {
        ThreadPool_current* job = ThreadPool_get_job(tp);
        if (!job) break;
        if (job->func) {
            job->func(job->arg);
        }
        free(job);
    }

    return NULL;

}

void ThreadPool_check(ThreadPool_current* tp){
    pthread_mutex_lock(&tp->lock);

    while (tp->jobs.size > 0 || tp->active_jobs > 0) {
        pthread_cond_wait(&tp->note, &tp->lock);
    }

    pthread_mutex_unlock(&tp->lock);
}



