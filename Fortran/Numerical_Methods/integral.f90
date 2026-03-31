module numerical
    implicit none
contains
real(kind=8) function func(x)
    implicit none
    real(kind=8) :: x
	func=x*exp(x)
    return
end function func
end module numerical

program main !// 辛普森积分
	use numerical
    implicit none 
    real(kind=8), parameter :: a = 0.d0, b = 1.d0     ! 积分区间为[a,b], 被积函数为f(x) = x*e^x
    integer, parameter :: n = 100    ! 区间等份
    real(kind=8), parameter :: h = ( b - a ) / ( n*1.d0 )
    real(kind=8) :: s = 0.d0    ! 积分结果
    real(kind=8) :: x(0:n), tmp, y0, y1, y2    ! x:节点坐标
    integer :: i
    write ( *,'(1x,a,g0)' ) '精确积分结果为: ', 1.d0
    
	do i = 0, n 
        x(i) = a + i * h
    end do 
   
    ! 计算梯形积分
    s = 0.d0
    do i = 1, n
        y0 = func(x(i-1))
        y1 = func(x(i))
        s = s + h * ( y0 + y1 ) / 2.d0    ! 梯形积分公式
    end do
    write ( *,'(1x,a,g0)' ) '梯形积分结果为: ', s
    
    s = 0.d0 
	! 计算辛普森积分
    do i = 1, n
        y0 = func(x(i-1))
        tmp = ( x(i-1) + x(i) ) / 2.d0
        y1 = func(tmp)
        y2 = func(x(i))
        s = s + h/2.d0 * ( y0 + 4.d0 * y1 + y2 ) / 3.d0    ! 辛普森积分公式
    end do
    write ( *,'(1x,a,g0)' ) '辛普森积分结果为: ', s
end program main
