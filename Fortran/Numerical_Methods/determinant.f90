module linearalgebra
    implicit none
contains
! 求矩阵的determinant值
real function determinant(matrix)
    real        :: matrix(:,:)
    real, allocatable :: ma(:,:)
    integer :: i,n
    n = size(matrix,1)
    allocate(ma(n,n))
    ma = matrix
    call upper(ma)    
    determinant = 1.0
    do i=1,n
        determinant = determinant*ma(i,i)
    end do
end function
! 求上三角矩阵的子程序
subroutine upper(matrix)
    real    :: matrix(:,:)
    integer :: m,n
    integer :: i,j
    real :: e
    m=size(matrix,1)
    n=size(matrix,2)
    do i=1,n-1
    do j=i+1,m        
        e=matrix(j,i)/matrix(i,i)
        ! 用90的功能可以少一层循环
        matrix(j,i:m)=matrix(j,i:m)-matrix(i,i:m)*e
    end do
    end do
    return
end subroutine upper
end module

program main
    use linearalgebra
    implicit none
    integer, parameter :: n = 3    ! size of matrix
    real :: a(n,n) = reshape( (/1,2,1,3,2,3,2,3,4/),(/n,n/) )
    write(*,"('det(a)=',f6.2)") determinant(a)
    stop
end program
