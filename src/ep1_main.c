#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <pthread.h>
#include "spend_time.h"

typedef struct
{
    int tid;
    int free_time;
    int critical_time;
    int resources[8];
    int num_resources;
} Thread;

typedef struct
{
    pthread_mutex_t mutex;
    pthread_cond_t cond;
    bool available[8];
} Resources;

struct ThreadArgs {
    Resources *resources;
    Thread *thread;
};

bool requested_available(Thread *thread, Resources *resources)
{
    for (int i = 0; i < thread->num_resources; i++)
    {
        if (!resources->available[thread->resources[i]])
            return false;
    }
    return true;
}

void init_resources(Resources *resources)
{
    pthread_mutex_init(&resources->mutex, NULL);
    pthread_cond_init(&resources->cond, NULL);

    for (int i = 0; i < 8; i++)
        resources->available[i] = true;
}

void lock_resources(Thread *thread, Resources *resources)
{
    pthread_mutex_lock(&resources->mutex);
    
    while (!requested_available(thread, resources))
        pthread_cond_wait(&resources->cond, &resources->mutex);
    
    for(int i = 0; i < thread->num_resources; i++)
        resources->available[thread->resources[i]] = false;
    
    pthread_mutex_unlock(&resources->mutex);
}

void free_resources(Thread *thread, Resources *resources)
{
    pthread_mutex_lock(&resources->mutex);
    
    for (int i = 0; i < thread->num_resources; i++)
        resources->available[thread->resources[i]] = true;
    
    pthread_cond_broadcast(&resources->cond);
    pthread_mutex_unlock(&resources->mutex);
}

void *thread_function(void *func_arg)
{
    struct ThreadArgs *arg = (struct ThreadArgs *) func_arg;
    spend_time(arg->thread->tid, NULL, arg->thread->free_time); 
    lock_resources(arg->thread, arg->resources);     // a forma de representar os recursos é uma decisão do desenvolvedor
    spend_time(arg->thread->tid,"C",arg->thread->critical_time);
    free_resources(arg->thread, arg->resources);     // note que cada thread deve ser ter sua lista de recursos registrada em algum lugar
    pthread_exit(NULL);
}

int main()
{
    int tid, free_time, critical_time;
    int requested_resources[8];
    char new_char;
    Resources resources;
    
    init_resources(&resources);
    
    while(scanf("%d %d %d", &tid, &free_time, &critical_time) == 3)  // Get input as long as there are 3 integers in the line
    {

        // Process the first part of the input
        //printf("\ntid: %d, free_time: %d, critical_time: %d\n", tid, free_time, critical_time);
        
        int num_resources = 0;
        
        do { 
            scanf("%d%c", &requested_resources[num_resources], &new_char);
            //printf("requested_resources[%d]: %d\n", num_resources, requested_resources[num_resources]); 
            num_resources++; 
        } while(new_char != '\n'); 


        // Process the second part of the input (requested resources)
        Thread thread = {tid, free_time, critical_time, requested_resources, num_resources};
        struct ThreadArgs thread_args = {&resources, &thread};
        
        pthread_t thread_id;

        if(pthread_create(&thread_id, NULL, thread_function, &thread_args) != 0)
        {
            printf("Error creating thread\n");
            exit(1);
        }

        // while ((ch = getchar()) != '\n' && ch != EOF);
    }
    printf("Im out\n");
    return 0;
}