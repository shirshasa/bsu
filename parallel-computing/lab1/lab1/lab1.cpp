#include "pch.h"
#include "lab1.h"
#include <iostream>
#include <algorithm>

int main(int argc, char* argv[]) {
	if (argc < 5) {
		cerr << "Error. Usage is:" << endl;
		cerr << "./lab1 -n <rows>  -r <block_size> " << endl;
		return 1;
	}

	int n,block_size,num_threads;
	string filename = "output.txt";

	for (int i = 1; i < argc; i += 2) {
		if (string(argv[i]) == "-n") {
			n = atoi(argv[i + 1]);
		}
	
		else if (string(argv[i]) == "-r") {
			block_size = atoi(argv[i + 1]);
		}
		else if (string(argv[i]) == "-f") {
			num_threads = atoi(argv[i + 1]);
		}
		else {
			cerr << "./lab1 -n <rows>  -r <block_size>  -f threads" << endl;
			return 1;
		}
	}

	fstream fout;
	fout.open(filename, fstream::out | fstream::app);
	omp_set_dynamic(0); //the runtime will not dynamically adjust the number of threads
	int* matrix1 = get_matrix(n, n);
	int* matrix2 = get_matrix(n, n);
	int* result_matrix = get_matrix(n,n,0);

	if (num_threads == 1) {
		fout << block_size << " ";
	}

	Timer::start();
	multiply(matrix1, matrix2, result_matrix, block_size, num_threads, n);
	fout << Timer::end() << " ";

	if (num_threads == 4) {
		fout << endl;
	}
	return 0;
}


void multiply(matrix_t& A, matrix_t& B, matrix_t& C, int r, int threads_count, int n) {

	for (int i_grid = 0; i_grid < n; i_grid += r) {
#pragma omp parallel for num_threads(threads_count)
		for (int j_grid = 0; j_grid < n; j_grid += r) {
			for (int k_grid = 0; k_grid < n; k_grid += r) {

				const int upper_i_grid = std::min(i_grid + r, n) * n;

				for (int i_ = i_grid * n; i_ < upper_i_grid; i_ += n) {

					const int upper_j_grid = std::min(j_grid + r, n);

					for (int j_ = j_grid; j_ < upper_j_grid; ++j_) {

						const int upper_k_grid = std::min(k_grid + r, n);

						for (int k_ = k_grid; k_ < upper_k_grid; ++k_) {
							C[i_ + j_] += A[i_ + k_] * B[k_*n + j_];
						}

					}
				}


			}
		}
	}
};

void block_multiply(matrix_t& m1, matrix_t& m2, matrix_t& result,int block_size,int threads_count, int n) {
	int q = ceil(n / block_size);

	for (int i1 = 0; i1 < q; i1++) {
	#pragma omp parallel for num_threads(threads_count)
		for (int j1 = 0; j1 < q; j1++) {
			for (int k1 = 0; k1 < q; k1++) {

				for (int i = i1 * block_size; i < min((i1+1) * block_size, n); i++) {

					for (int j = j1 * block_size; j < min((j1 + 1) * block_size, n); j++) {

						for (int k = k1 * block_size; k < min((k1 + 1) * block_size, n); k++) {
			
							result[i*n + j] += m1[i*n + k ] * m2[k*n + j];
						}
					}
				}

			}
		}
	}
	return;
}


