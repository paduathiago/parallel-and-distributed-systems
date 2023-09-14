#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <pthread.h>
#include "spend_time.h"

#define MAX_THREADS 1000
#define AVAILABLE_RESOURCES 8

/*
This struct is used to keep track of the information about each thread.
It contains the thread id, the time it takes to get to the critical section and the time it takes to execute the critical section.
It also contains an array of integers that represents the resources that the thread needs to execute the critical section.
The number of resources is stored in num_resources. This makes it possible to loop through the array without having to know its size
*/
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
The have been defined as part of the struct because it represents the elements that are shared between threads and, therefore, can cause race conditions.
Keeping track of which resources are available is done by the available boolean array. 
Each position represents a resource, ensuring that any query for the availability of an individual resource is O(1).
*/
typedef struct
{
    pthread_mutex_t mutex;
    pthread_cond_t cond;
    bool available[AVAILABLE_RESOURCES];
} Resources;


/*
This struct is used to pass the arguments to the thread_function.
It contains a pointer to the resources struct, which is shared between threads throughot the entire execution of the program.
This aproach was chosen instead of using global variables because it allows the program to be more flexible and safe.
It also contains a Thread struct, which keeps the information about the thread that is being created
*/
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

/*
This functiom is responsible for control the shared resources. The syncronization is assured by the mutex and condition variable.
The mutex that grants access to the resources and the available array is locked when a thread enters the critical section. It then checks if the requested resources are available.
If they are not, the thread waits for a signal from another thread that the resources are available.
When the signal is received, the thread checks again, on the while loop, if the resources are available. If they are not, it waits again.
Once the resources are available, the thread locks the resources and sets the availability of the resources to false.
When the thread leaves the critical section, it unlocks the mutex so that others can try to access the resources.
*/
void lock_resources(const Thread thread, Resources *resources)
{
    pthread_mutex_lock(&resources->mutex);
    
    while (!is_requested_available(thread, resources))
        pthread_cond_wait(&resources->cond, &resources->mutex);
    
    for(int i = 0; i < thread.num_resources; i++)
        resources->available[thread.resources[i]] = false;
    
    pthread_mutex_unlock(&resources->mutex);
}

/*
This function is responsible for freeing the resources that were locked by the thread.
It locks the mutex that grants access to the available array, sets the availability of the resources to true and broadcasts a signal to all threads that the resources are available.
After that, it unlocks the mutex so that other threads can access the resources.
*/
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