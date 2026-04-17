#ifndef PROCESSOR_H
#define PROCESSOR_H

#include "matrix.h"

uint32_t roll_l_func(uint32_t number, uint32_t offset);
uint32_t roll_r_func(uint32_t number, uint32_t offset);
void process(uint32_t *arr, uint32_t *out, Matrix mantis, uint32_t start, uint32_t length, uint32_t salt);

#endif
