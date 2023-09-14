#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <pthread.h>
#include "spend_time.h"

#define MAX_THREADS 1000
#define AVAILABLE_RESOURCES 8

typedef struct
{
    int tid;
    int free_time;
    int critical_time;
    int resources[AVAILABLE_RESOURCES];
    int num_resources;
} Thread;

/*
Resources have been defined as a struct to allow more flexibility.
mutex and cond are, respectively, pthreads' mutex and condition variables used to control parallel access to the resources properly.
Keeping track of which resources are available is done by the available boolean array. 
Each position represents a resource, ensuring that any query for the availability of an individual resource is O(1).
*/
typedef struct
{
    pthread_mutex_t mutex;
    pthread_cond_t cond;
    bool available[AVAILABLE_RESOURCES];
} Resources;

struct ThreadArgs {
    Resources *resources;
    Thread thread;
};

bool is_requested_available(const Thread thread, const Resources *resources)
{
    for (int i = 0; i < thread.num_resources; i++)
    {
        if (!resources->available[thread.resources[i]])
            return false;
    }
    return true;
}

/*Initializes mutex, condition variable and sets every value in Resources.available to true*/
void init_resources(Resources *resources)
{
    pthread_mutex_init(&resources->mutex, NULL);
    pthread_cond_init(&resources->cond, NULL);

    for (int i = 0; i < AVAILABLE_RESOURCES; i++)
        resources->available[i] = true;
}

void lock_resources(const Thread thread, Resources *resources)
{
    pthread_mutex_lock(&resources->mutex);
    
    while (!is_requested_available(thread, resources))
        pthread_cond_wait(&resources->cond, &resources->mutex);
    
    for(int i = 0; i < thread.num_resources; i++)
        resources->available[thread.resources[i]] = false;
    
    pthread_mutex_unlock(&resources->mutex);
}

void free_resources(const Thread thread, Resources *resources)
{
    pthread_mutex_lock(&resources->mutex);
    
    for (int i = 0; i < thread.num_resources; i++)
        resources->available[thread.resources[i]] = true;
    
    pthread_cond_broadcast(&resources->cond);
    pthread_mutex_unlock(&resources->mutex);
}

void *thread_function(void *func_arg)
{
    struct ThreadArgs *arg = (struct ThreadArgs *) func_arg;
    spend_time(arg->thread.tid, NULL, arg->thread.free_time); 
    lock_resources(arg->thread, arg->resources);     // a forma de representar os recursos é uma decisão do desenvolvedor
    spend_time(arg->thread.tid, "C", arg->thread.critical_time);
    free_resources(arg->thread, arg->resources);     // note que cada thread deve ser ter sua lista de recursos registrada em algum lugar
    pthread_exit(NULL);
}

int main()
{
    int tid, free_time, critical_time, num_threads = 0;
    char new_char;
    Resources resources;
    pthread_t THREADS[MAX_THREADS];
    struct ThreadArgs thread_args[MAX_THREADS];
    
    init_resources(&resources);
    
    while(scanf("%d %d %d", &tid, &free_time, &critical_time) == 3)  // Get input as long as there are 3 integers in the line
    {
        Thread new_thread;

        // Process the first part of the input
        //printf("tid: %d, free_time: %d, critical_time: %d\n", tid, free_time, critical_time);
        
        int num_resources = 0;
        
        do { 
            scanf("%d%c", &new_thread.resources[num_resources], &new_char);
            //printf("requested_resources[%d]: %d\n", num_resources, requested_resources[num_resources]); 
            num_resources++; 
        } while(new_char != '\n'); 


        // Process the second part of the input (requested resources)
        
        new_thread.tid = tid;
        new_thread.free_time = free_time;
        new_thread.critical_time = critical_time;
        new_thread.num_resources = num_resources;

        thread_args[num_threads].resources = &resources;
        thread_args[num_threads].thread = new_thread;
        
        if(pthread_create(&THREADS[num_threads], NULL, thread_function, &thread_args[num_threads]) != 0)
        {
            printf("Error creating thread\n");
            exit(1);
        }

        num_threads++;
    }
    return 0;
}