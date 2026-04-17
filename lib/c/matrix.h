#ifndef MATRIX_H
#define MATRIX_H

#include <stdint.h>

typedef struct Matrix {
	uint32_t data[256];
	uint32_t constant;
} Matrix;

uint32_t collect(Matrix *matrix, uint32_t row, uint32_t column);
uint32_t collect_inclusive_disjunction_column(Matrix *matrix, uint32_t row);
int write(Matrix *matrix, uint32_t row, uint32_t column, uint32_t value);
Matrix* fill(Matrix* mantis, const uint32_t *array, uint32_t length);

#endif
