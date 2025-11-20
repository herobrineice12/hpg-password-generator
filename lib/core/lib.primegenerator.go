package main

//#include <stdio.h>
import "C"

import (
	"fmt"
	"math"
	"sync"
	"unsafe"
)

func isPrime(number int) bool {
	var limit int = int(math.Sqrt(float64(number)))

	for i := 3; i <= limit; i++ {
		if number%i == 0 {
			return false
		}
	}

	return true
}

//export generatePrimes
func generatePrimes(candidates *C.int, size C.int) *C.char {
	var length int = int(size)
	var midpoint int = length / 2

	var primeString1 []string
	var primeString2 []string

	var waitGroup sync.WaitGroup

	var loopCandidates = func(start int, end int, primeString *[]string) {
		var local []string

		for i := start; i < end; i++ {
			var candidate C.int = *(*C.int)(unsafe.Pointer(uintptr(unsafe.Pointer(candidates)) + uintptr(i)*unsafe.Sizeof(C.int(0))))

			if isPrime(int(candidate)) {
				local = append(local, fmt.Sprint(candidate))
			}
		}

		*primeString = local

		waitGroup.Done()
	}

	waitGroup.Add(2)

	go loopCandidates(0, midpoint, &primeString1)
	go loopCandidates(midpoint, length, &primeString2)

	waitGroup.Wait()

	var primes = append(primeString1, primeString2...)
	var hash string = ""

	for i := range primes {
		hash += fmt.Sprint(primes[i])
	}

	return C.CString(hash)
}

func main() {

}
