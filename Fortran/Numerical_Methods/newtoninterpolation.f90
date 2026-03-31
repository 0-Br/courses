! newton interpolation
module interpolation
contains
subroutine newtdd( x,y,c )    ! 计算牛顿插值系数
    implicit none
    real(kind=8), intent( in )    :: x(:), y(:)
    real(kind=8), intent( inout ) :: c(:,:)    ! 数组c存储系数矩阵
    real(kind=8), allocatable     :: v(:,:)
    integer :: i, j, n

    n = size(x)
    allocate( v(n,n) )
    v = 0.d0
    do i = 1, n
        v(i,1) = y(i)
    end do

    do j = 2, n
        do i = 1, n + 1 - j
            v(i,j) = ( v(i+1,j-1) - v(i,j-1) ) / ( x(i+j-1) - x(i) )
        end do
    end do

    c(1,:) = v(1,:)    ! 获取系数
end subroutine newtdd

subroutine calinterpolation( x,xx,c,res )
    implicit none
    real(kind=8), intent( in ) :: x(:), xx(:), c(:,:)
    real(kind=8), intent( inout ) :: res(:,:)
    real(kind=8), allocatable :: d(:,:)
    integer :: i, j, m

    m = size(x)
    allocate( d(m,m) )

    d(1,:) = 1.d0
    do j = 1, m
        do i = 2, m
            d(i,j) = d(i-1,j) * ( xx(j) - x(i-1) )
        end do
    end do
    res = matmul( c,d )
end subroutine calinterpolation
end module interpolation

program newtoninterpolation
    use interpolation
    implicit none
    integer, parameter :: n = 20
    real(kind=8) :: a = -1.d0, b = 1.d0
    real(kind=8) :: x(n), xx(n), y(n), c(1,n), res(1,n)
    integer :: i

    do i = 1, n
        x(i) = a + real(i,8) * ( b - a ) / real(n,8)    ! 已知节点均匀分布
        xx(i) = a / 2.d0 + real(i,8) * ( b - a ) / 2.d0 / real(n,8)    ! 待求插值节点
        y(i) = exp( x(i) )    ! y = exp(x)
    end do
    call newtdd( x,y,c )    ! 求解系数c
    call calinterpolation( x,xx,c,res )    ! 求解插值节点处的节点值
    open ( 101, file = 'result.dat' )
    do i = 1, n
        write ( 101,'(4(2x,g0))' ) x(i), y(i), xx(i), res(1,i)
        write ( *,'(4(2x,g0))' ) x(i), y(i), xx(i), res(1,i)
    end do
    close ( 101 )
end program newtoninterpolation
