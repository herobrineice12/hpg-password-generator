package main

/*
#cgo LDFLAGS: -L../fortran -lfor -Wl,-rpath,$ORIGIN/../fortran
#include <stdio.h>
#include <stdlib.h>

void array_processing(void *arr, int len, int buffer, void *out, int *out_len, int *overflow, int *next_index);
*/
import "C"

import (
	"fmt"
	"math"
	"runtime"
	"strings"
	"sync"
	"unsafe"
)

func threadCalculation(arraySize *C.int) int {
	var workers int = 1
	var threads int = runtime.NumCPU()
	const minimunWorkload int = 65536

	switch {
	case threads <= 1:
		return 1
	case threads <= 4:
		workers = 2
	case threads <= 16:
		workers = threads / 2
	case threads <= 24:
		workers = int(float32(threads) * 0.70)
	default:
		workers = int(float32(threads) * 0.75)
	}

	var estimated int = int(*arraySize) / minimunWorkload

	switch {
	case estimated < 2:
		return 2
	case estimated < workers:
		return estimated
	default:
		return workers
	}
}

//export generatePrimes
func generatePrimes(candidates *C.int, size C.int) *C.char {
	var waitGroup sync.WaitGroup
	var mutex sync.Mutex

	var threadNumber int = threadCalculation(&size)
	var matrix [][]C.int = make([][]C.int, threadNumber)

	var workDivision int = int(size) / threadNumber

	for i := 0; i < threadNumber; i++ {
		waitGroup.Add(1)

		go func(threadIdx int, start int) {
			defer waitGroup.Done()

			var arrayPointer = unsafe.Add(unsafe.Pointer(candidates), uintptr(start)*unsafe.Sizeof(*candidates))
			var length C.int = C.int(workDivision)

			if threadIdx == threadNumber-1 {
				length = size - C.int(start)
			}

			var estimateNumbers = func(floor int, ceil int) int {
				var rosserFormula = func(num int) int {
					var x float64 = float64(num)

					var natx float64 = math.Log(x)

					return int((x*natx + 1.2762*x) / (natx * natx))
				}

				return rosserFormula(ceil) - rosserFormula(floor)
			}

			var bufferSize C.int = C.int(estimateNumbers(start, start+workDivision))

			var arrayOutput []C.int
			var arrayOutputLength C.int

			var startIndex C.int = C.int(0)
			var overflow C.int = C.int(0)

			for overflow == 1 || arrayOutputLength == 0 {
				if overflow == 1 {
					bufferSize += bufferSize / 2

					if bufferSize > length {
						bufferSize = length
					}
				}

				arrayOutput = make([]C.int, bufferSize)
				arrayOutputLength = 0

				C.array_processing(
					arrayPointer,                    // void *arr
					length,                          // int len
					bufferSize,                      // int buffer
					unsafe.Pointer(&arrayOutput[0]), // void *out
					&arrayOutputLength,              // int *out_len
					&overflow,                       // int *overflow
					&startIndex,                     // int *start_index
				)
			}

			mutex.Lock()
			matrix[threadIdx] = arrayOutput[:arrayOutputLength]
			mutex.Unlock()

		}(i, i*workDivision)
	}

	waitGroup.Wait()

	var builder strings.Builder

	for _, row := range matrix {
		for _, v := range row {
			builder.WriteString(fmt.Sprintf("%d", int(v)))
		}
	}

	return C.CString(strings.TrimSpace(builder.String()))
}

func main() {

}
