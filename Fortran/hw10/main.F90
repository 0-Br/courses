module Sorted_Convolution

    implicit none
    integer :: size, i
    integer, allocatable :: array_int(:)
    real, allocatable :: array_float(:)
    real :: re0

    ! (4)
    interface sort
        module procedure sort_int
        module procedure sort_float
    end interface

    contains

    subroutine init(N)
        implicit none
        integer, intent(in) :: N
        size = N
        allocate(array_int(size))
        allocate(array_float(size))
    end subroutine

    subroutine realease()
        implicit none
        deallocate(array_int)
        deallocate(array_float)
    end subroutine

    ! (3)
    subroutine sort_int(array)
        implicit none
        integer, intent(in) :: array(:)
        integer :: temp
        logical :: sorted = .false.
        do i = 1, size
            array_int(i) = array(i)
        end do
        do while (.not. sorted)
            sorted = .true.
            do i = 1, size - 1
                if (array_int(i) > array_int(i + 1)) then
                    temp = array_int(i)
                    array_int(i) = array_int(i + 1)
                    array_int(i + 1) = temp
                    sorted = .false.
                end if
            end do
        end do
        ! check
        write(*, "(A)") "== Checking for Sort Correctness..."
        do i = 1, size - 1
            if (array_int(i) > array_int(i + 1)) then
                write(*, "(A)") "[Error] Sort Failed!"
                stop
            end if
        end do
        write(*, "(A)") "== Check Complete!"
        write(*, "(A)") ">> Integer Sort Result: "
        print *, array_int
    end subroutine

    ! (3)
    subroutine sort_float(array)
        implicit none
        real, intent(in) :: array(:)
        real :: temp
        logical :: sorted = .false.
        do i = 1, size
            array_float(i) = array(i)
        end do
        do while (.not. sorted)
            sorted = .true.
            do i = 1, size - 1
                if (array_float(i) > array_float(i + 1)) then
                    temp = array_float(i)
                    array_float(i) = array_float(i + 1)
                    array_float(i + 1) = temp
                    sorted = .false.
                end if
            end do
        end do
        ! check
        write(*, "(A)") "== Checking for Sort Correctness..."
        do i = 1, size - 1
            if (array_float(i) > array_float(i + 1)) then
                write(*, "(A)") "[Error] Sort Failed!"
                stop
            end if
        end do
        write(*, "(A)") "== Check Complete!"
        write(*, "(A)") ">> Float Sort Result: "
        print *, array_float
    end subroutine

    ! (5)
    subroutine conv()
        implicit none
        re0 = 0
        do i = 1, size
            re0 = re0 + array_int(i) * array_float(i)
        end do
        write(*, "(A, F0.8)") ">> Convolution Result: ", re0
    end subroutine

end module


program main

    use Sorted_Convolution
    implicit none

    integer :: N, M, var
    character(len=1024) :: PATH, flag
    real :: input_float(1024)
    integer :: input_int(1024)

    ! (1)
    namelist /input/ N, PATH
    open(42, file="./input.nml", status="old", action="read", iostat=var)
    if (var .ne. 0) then
        write(*, "(A)") "[Error] Namelist Not Found!"
        close(42)
        stop
    end if
    read(42, nml=input)
    if (N .le. 0) then
        write(*, "(A)") "[Error] N Should be Positive!"
        close(42)
        stop
    end if
    close(42)
    write(*, "(A, I0, A, A)") "<< N = ", N, "; Path: ", trim(PATH)

    ! (2)
    M = 0
    open(3407, file=trim(PATH), status="old", action="read", iostat=var)
    if (var .ne. 0) then
        write(*, "(A)") "[Error] File Not Found!"
        close(3407)
        stop
    end if
    do while (M .ne. (N + 1))
        M = M + 1
        read(3407, *, iostat=var) input_float(M), input_int(M)
        if (var < 0) exit
    end do
    M = M - 1
    close(3407)
    write(*, "(A)") "<< Contents of the Input Arrays are:"
    print *, input_float(1:M)
    print *, input_int(1:M)
    do while (.true.)
        write(*, "(A)") "== Please Confirm the Input! [Y/N]"
        read(*, "(A)") flag
        if ((trim(flag) .eq. "Y") .or. (trim(flag) .eq. "y")) then
            write(*, "(A)") "== Confirmed and Continue!"
            exit
        else if ((trim(flag) .eq. "N") .or. (trim(flag) .eq. "n")) then
            write(*, "(A)") "[Error] Exit!"
            stop
        end if
    end do

    ! (5)
    call init(M)
    call sort(input_float)
    call sort(input_int)
    call conv()
    call realease()

end program
