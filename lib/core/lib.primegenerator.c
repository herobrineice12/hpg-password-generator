#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <string.h>

#define uint32 __uint32_t

int isprime(int number) {
    int limit = sqrt(number);

    for (int i = 3; i <= limit; i += 2) {
        if (i > 10 && !(i % 5)) continue;
        if (!(number % i)) return 0;
    }

    return 1;
}

char* generateprimes(int* array, int length) {
    char* hash = malloc(1);
    if (!hash) return NULL;

    hash[0] = '\0';
    uint32 hashlength = 0;
    
    for (int i = 0; i < length; i++) {
        int num = *(array + i);
        
        if (isprime(num)) {
            char tempbuffer[6];

            snprintf(tempbuffer, sizeof(tempbuffer), "%d", num);

            uint32 templength = strlen(tempbuffer);

            char* newhash = realloc(hash, hashlength + templength + 1);
            if (!newhash) {
                free(hash);
                return NULL;
            }

            hash = newhash;
            memcpy(hash + hashlength, tempbuffer, templength + 1);

            hashlength += templength;
        }
    }

    return hash;
}