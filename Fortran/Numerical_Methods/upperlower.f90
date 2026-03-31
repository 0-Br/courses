module linearalgebra
    implicit none
contains
! 输出矩阵的子程序
subroutine output(matrix)
    implicit none
    integer :: m,n
    real    :: matrix(:,:)
    integer :: i
    character(len=20) :: for='(??(1x,f6.3))'
    m = size(matrix,1)
    n = size(matrix,2)
    ! 用字符串来设定输出格式
    write( for(2:3), '(i2)' ) n
    do i=1,n
        write( *, fmt=for ) matrix(i,:)
    end do
    return
end subroutine output
! 求上三角矩阵的子程序
subroutine upper(matrix)
    implicit none
    real    :: matrix(:,:)
    integer :: m,n
    integer :: i,j
    real    :: e
    m=size(matrix,1) 
    n=size(matrix,2)
    do i=1,n-1
        do j=i+1,m        
            e=matrix(j,i)/matrix(i,i)
            ! 用Fortran90的功能可以少一层循环
            matrix(j,i:m)=matrix(j,i:m)-matrix(i,i:m)*e
        end do
    end do
    return
end subroutine upper
! 求下三角矩阵的子程序
subroutine lower(matrix)
    implicit none
    real    :: matrix(:,:)
    integer :: m,n
    integer :: i,j
    real :: e
    m = size(matrix,1)
    n = size(matrix,2)
    do i=n,2,-1
        do j=i-1,1,-1                     
            e=matrix(j,i)/matrix(i,i)
            ! 用90的功能可以少一层循环
            matrix(j,1:i)=matrix(j,1:i)-matrix(i,1:i)*e 
        end do
    end do
    return
end subroutine lower
end module

program main
    use linearalgebra
    implicit none
    integer, parameter :: n = 3    ! size of matrix
    real :: a(n,n) = reshape( (/1,2,3,1,3,4,1,4,6/),(/n,n/) )
    real :: b(n,n)

    write(*,*) "matrix a:"
    call output(a)
    b=a
    write(*,*) "upper:"
    call upper(b)
    call output(b)
    b=a
    write(*,*) "lower:"
    call lower(b)
    call output(b)
    stop
end program
