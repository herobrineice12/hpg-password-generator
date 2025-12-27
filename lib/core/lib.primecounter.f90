
module prime_utils
    use iso_c_binding
contains
    subroutine array_processing(arr, len, buffer, out, out_len, overflow, next_index) bind(C, name="array_processing")
        implicit none

        TYPE(C_PTR), intent(in), VALUE  :: arr
        INTEGER(C_INT), intent(in), VALUE :: len
        INTEGER(C_INT), intent(in), VALUE :: buffer
        TYPE(C_PTR), intent(in), VALUE :: out
        INTEGER(C_INT), intent(out) :: out_len
        INTEGER(C_INT), intent(out) :: overflow
        INTEGER(C_INT), intent(out) :: next_index

        INTEGER(C_INT), pointer :: farr(:)
        INTEGER(C_INT), pointer :: fout(:)

        INTEGER :: i, count

        call c_f_pointer(arr, farr, [len])
        call c_f_pointer(out, fout, [buffer])

        overflow = 0
        count = 0

        do i = next_index + 1, len
            if (is_prime(farr(i))) then
                if (count >= buffer) then
                    overflow = 1
                    next_index = i - 1
                    out_len = count
                    return
                end if

                count = count + 1
                fout(count) = farr(i)
            end if
        end do

        overflow = 0
        out_len = count
        next_index = len
    end subroutine

    logical function is_prime(num)
        implicit none

        INTEGER, intent(in) :: num
        INTEGER :: limit

        INTEGER :: i

        limit = int(sqrt(real(num))) + 1
        is_prime = .true.

        do i=3, limit, 2
            if (i > 10 .and. mod(i,5) == 0) then
                continue
            end if

            if (mod(num,i) == 0) then
                is_prime = .false.
                return
            end if
        end do
    end function

    subroutine add_to_list(list, element) ! by francescalus
        implicit none

        INTEGER(C_INT) :: i
        INTEGER(C_INT) :: isize
        INTEGER(C_INT), intent(in) :: element
        INTEGER(C_INT), dimension(:), allocatable, intent(inout) :: list
        INTEGER(C_INT), dimension(:), allocatable :: clist

        if (allocated(list)) then
            isize = size(list)
            allocate(clist(isize+1))

            do i=1, isize
                clist(i) = list(i)
            end do

            clist(isize+1) = element

            deallocate(list)
            call move_alloc(clist,list)

        else
            allocate(list(1))
            list(1) = element
        end if

        return
    end subroutine
end module

program primecounter
    implicit none

end program primecounter
