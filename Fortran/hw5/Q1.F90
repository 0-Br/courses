program Q1
    ! 建议使用gfortran编译器，编译选项: -O2
    implicit none

    ! 尽量减小位宽能提高程序的运行效率
    integer(kind=2) :: N, i, j, k ! N/i/j/k < 100 < 32768，采用2位宽整形存储
    integer(kind=2), allocatable :: array(:, :, :) ! array中储存的值 < 20000 < 32768，采用2位宽整形存储
    integer(kind=4) :: sum ! sum < 2000000 < 2147483648，采用4位宽整形存储
    read(*, *) N
    sum = 0
    allocate(array(N, N, N))

    ! 赋值与计算同时进行，避免重复遍历数组
    ! 顺序为自低维向高维，充分利用内存访问的局部性加速
    do k = 1, N
        do j = 1, N
            do i = 1, N
                array(i, j, k) = 100 * i + 10 * j + k
                if ((i + j + k) .eq. N) then
                    sum = array(i, j, k) + sum
                endif
            enddo
        enddo
    enddo

    write(*, "(I0)") sum
    deallocate(array)

end program Q1
