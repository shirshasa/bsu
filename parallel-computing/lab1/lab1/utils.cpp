#include "pch.h"
#include "utils.h"

hr_clock::time_point Timer::start_time = hr_clock::now();

void Timer::start() {
	start_time = hr_clock::now();
}

double Timer::end() {
	auto end_time = hr_clock::now();
	return chrono::duration_cast<ms>(end_time - start_time).count() / 1000.;
}

void Timer::print() {
	cout << "elapsed: " << setprecision(3) << end() << " s" << endl;
}

/*
 * generate random number in [-100, 100]
 */
int get_random_number() {
	return (rand() % 200) - 100;
}

matrix_t get_matrix(int rows, int cols) {
	matrix_t v = new int[rows*cols];
	int k = 0;
	for (int i = 0; i < rows; i++) {
		for (int j = 0; j < cols; j++) {
			v[k] = get_random_number();
			k++;
		}
	}
	return v;
}

matrix_t get_matrix(int rows, int cols,int mode) {
	matrix_t v = new int[rows*cols];
	int k = 0;
	for (int i = 0; i < rows; i++) {
		for (int j = 0; j < cols; j++) {
			v[k] = 0;
			k++;
		}
	}
	
	return v;
}

ostream& print_matrix(matrix_t& v,int n) {
	for (int i = 0; i <n; i++) {
		for (int j = 0; j < n; j++) {
			cout << v[i*n + j] << " ";
		}
		cout << endl;
	}
	cout << endl;
	return cout;
}