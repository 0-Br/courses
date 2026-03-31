program Q2
    ! 建议使用gfortran编译器，编译选项: -O2
    implicit none

    integer :: N, i
    character(len=32), allocatable :: sentences(:)
    character(len=32) :: temp
    logical :: sorted = .false.
    read(*, *) N
    allocate(sentences(N))

    do i = 1, N
        read(*, "(A)") sentences(i)
    enddo

    ! 冒泡排序
    do while (.not. sorted)
        sorted = .true.
        do i = 1, N - 1
            if (sentences(i) > sentences(i + 1)) then
                temp = sentences(i)
                sentences(i) = sentences(i + 1)
                sentences(i + 1) = temp
                sorted = .false.
            endif
        enddo
    enddo

    do i = 1, N
        write(*, "(A)") sentences(i)
    enddo
    deallocate(sentences)

end program Q2
