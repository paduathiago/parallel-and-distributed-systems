#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <pthread.h>

typedef struct
{
    int tid;
    int free_time;
    int critical_time;
    int resources[8];
    int num_resources;
} Task;

typedef struct
{
    bool available[8];
} Resources;

void init_resources(Resources *resources)
{
    for (int i = 0; i < 8; i++)
        resources->available[i] = true;
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
        printf("\ntid: %d, free_time: %d, critical_time: %d\n", tid, free_time, critical_time);
        
        int num_resources = 0;
        
        do { 
            scanf("%d%c", &requested_resources[num_resources], &new_char);
            printf("requested_resources[%d]: %d\n", num_resources, requested_resources[num_resources]); 
            num_resources++; 
        } while(new_char != '\n'); 


        // Process the second part of the input (requested resources)
        // while ((ch = getchar()) != '\n' && ch != EOF);
    }
    printf("Im out\n");
    return 0;
}