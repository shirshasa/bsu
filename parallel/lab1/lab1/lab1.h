#ifndef LAB1_LAB1_H
#define LAB1_LAB1_H

#include <vector>
#include <iostream>
#include <fstream>

#include "omp.h"
#include "utils.h"

using namespace std;


void multiply(matrix_t& A, matrix_t& B, matrix_t& C, int r, int threads_count, int n);

void block_multiply(matrix_t&, matrix_t&, matrix_t&,  int,int,int);

#endif //LAB1_LAB1_H
