module interpolate_utility
    implicit none
    type point
        real x,y
    end type
    real, parameter :: pi=3.14159
    real, parameter :: xmin = 0.0, xmax = pi*3.0
    integer, parameter :: n = 10, np = 30
    type(point) :: datas(n)
    type(point) :: interpolate(np)
contains
! 产生数列
subroutine generatedata(func)
    real, external :: func
    real r, width
    integer i
    width = (xmax-xmin)/(n-1)
    r = 0
    do i=1,n
        datas(i)%x = r
        datas(i)%y = func(r)
        r = r+width
    end do
end subroutine

real function lagrange(x)
    real x
    real coeff
    integer i,j
    lagrange = 0
    do i=1,n
        coeff = 1
        do j=1,n
            if ( i/=j ) coeff = coeff * (x-datas(j)%x)/(datas(i)%x-datas(j)%x)
        end do
        lagrange = lagrange + coeff*datas(i)%y
    end do
end function
end module

program main
    use interpolate_utility
    implicit none
    real, intrinsic :: sin
    real xinc,x
    integer i

    call generatedata(sin) ! 产生数据点
    x=0
    xinc = (xmax-xmin)/(np-1)
    do i=1,np
        interpolate(i)%x = x
        interpolate(i)%y = lagrange(x) ! 插值出f(x)的值
		print *,interpolate(i)%x, interpolate(i)%y, sin(interpolate(i)%x)
        x = x+xinc
    end do
end program
