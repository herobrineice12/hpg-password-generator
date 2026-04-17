module selector
  use iso_c_binding
contains
  subroutine select_constants(inp,out,len) bind(C,"select_constants")
    implicit none
    
    TYPE(C_PTR), INTENT(IN), VALUE :: inp, out
    INTEGER(C_INT32_T), INTENT(IN) :: len

    INTEGER(C_INT32_T), POINTER :: iarr(:), oarr(:)
    INTEGER(C_INT32_T) :: subject

    INTEGER(TYPE=4) :: min_entropy, entropy, extracted, idx

    call c_f_pointer(inp,iarr,[len])
    call c_f_pointer(out,oarr,[len])

    entropy = 0

    do idx = 1, len
      subject = iarr(idx)
      
      if (subject < 0) then
        subject = -subject
      end if

      if (mod(subject,2) == 0) then
        subject = subject + 1
      end if

      do while (entropy < min_entropy)
        if (subject >= 4294967040) then
          subject = shiftr(not(subject),4)
        end if

        do while (.not. is_prime(subject))
          subject = subject + 2
        end do

        extracted = calculate_constant(subject)
        entropy = calculate_entropy(extracted)
      end do

      entropy = 0
      oarr(idx) = extracted
    end do

  end subroutine select_constants

  logical function is_prime(dummy_number) result(prime)
    implicit none
    
    INTEGER(C_INT32_T), INTENT(IN) :: dummy_number

    INTEGER(TYPE=4) :: number, limit
    INTEGER :: idx
    REAL :: square
    
    prime = .false.

    if (dummy_number <= 0) then
      return
    end if

    if (dummy_number == 2 .or. dummy_number == 3) then
      prime = .true.
      return
    end if

    number = dummy_number

    if (mod(number,2) == 0) then
      return
    end if

    square = sqrt(real(number))

    if (square - floor(square) == 0) then
      return
    end if

    limit = integer(square,type=4)
      
    do idx = 3, limit, 2
      if (mod(number,idx) == 0) then
        return
      end if
    end do

    prime = .true.
  end function is_prime

  integer(c_int32_t) function calculate_constant(dummy_number) result(number)
    implicit none
    
    INTEGER(C_INT32_T), INTENT(IN) :: dummy_number
    
    REAL, CONSTANT :: const = 4294967296.0
    REAL :: decimal

    number = dummy_number

    decimal = sqrt(real(number))
    decimal = (decimal - floor(decimal)) * const

    number = integer(decimal)

  end function calculate_constant

  real function calculate_entropy(dummy_number) result(entropy)
    implicit none
    
    INTEGER(C_INT32_T), INTENT(IN) :: dummy_number 

    INTEGER(TYPE=4) :: number, digit, total, idx
    INTEGER(TYPE=1) :: digits(0:9)

    REAL :: variant

    entropy = 0

    if (dummy_number == 0) then
      return
    else if (dummy_number < 0) then
      number = -dummy_number
    else
      number = dummy_number
    end if

    number = dummy_number
    digits = 0
    total = 0

    do while (number /= 0)
      number = number / 10
      digit = mod(number,10)

      digits(digit) = digits(digit) + 1

      total = total + 1
    end do

    variant = 0.0

    do idx = 0, 9
      variant = variant + digit(idx) / real(total)
    end do

    entropy = -variant * log(variant) / log(2)
  end function calculate_entropy
end module selector
