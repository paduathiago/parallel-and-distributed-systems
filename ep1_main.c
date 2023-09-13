#include <stdio.h>
#include <stdlib.h>

int main()
{
    int tid, free_time, critical_time;
    int resources[8];
    int num_resources = 0;
    
    while(scanf("%d %d %d", tid, free_time, critical_time) == 3)  // Get input as long as there are 3 integers in the line
    {
        // Process the first part of the input
        
        while (num_resources < 8 && scanf("%d", &resources[num_resources]) == 1) 
            num_resources++;
        
        // Process the second part of the input (requested resources)

    }
    return 0;
}