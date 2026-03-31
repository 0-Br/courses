module linearalgebra
    implicit none
contains
! gauss_jordan法
subroutine gauss_jordan(a,s,ans)
    implicit none
    real        :: a(:,:)
    real        :: s(:)
    real        :: ans(:)
    real, allocatable :: b(:,:)
    integer :: i, n
    n = size(a,1)    
    allocate(b(n,n))
    ! 保存原先的矩阵a,及数组s
    b=a 
    ans=s    
    ! 把b化成对角线矩阵(除了对角线外,都为0)
    call upper(b,ans,n) ! 先把b化成上三角矩阵
    call lower(b,ans,n) ! 再把b化成下三角矩阵
    ! 求解
    forall(i=1:n)
        ans(i)=ans(i)/b(i,i) 
    end forall
    return
end subroutine gauss_jordan
! 输出等式
subroutine output(m,s)
    implicit none
    real        :: m(:,:), s(:)
    integer :: n,i,j
    n = size(m,1)
    ! write中加上advance="no",可以中止断行发生,使下一次的
    ! write接续在同一行当中.
    do i=1,n
        write(*,"(1x,f5.2,a1)", advance="no") m(i,1),'A'
        do j=2,n
            if ( m(i,j) < 0 ) then
                write(*,"('-',f5.2,a1)",advance="no") -m(i,j),char(64+j)
            else
                write(*,"('+',f5.2,a1)",advance="no") m(i,j),char(64+j)
            end if
        end do
        write(*,"('=',f8.4)") s(i)
    end do
    return
end subroutine output
! 求上三角矩阵的子程序
subroutine upper(m,s,n)
    implicit none
    integer :: n
    real        :: m(n,n)
    real        :: s(n)
    integer :: i,j
    real :: e
    do i=1,n-1
        do j=i+1,n                            
            e=m(j,i)/m(i,i)
            m(j,i:n)=m(j,i:n)-m(i,i:n)*e
            s(j)=s(j)-s(i)*e
        end do
    end do
    return
end subroutine upper
! 求下三角矩阵的子程序
subroutine lower(m,s,n)
    implicit none
    integer :: n
    real        :: m(n,n)
    real        :: s(n)
    integer :: i,j
    real :: e
    do i=n,2,-1
        do j=i-1,1,-1                     
            e=m(j,i)/m(i,i)
            m(j,1:n)=m(j,1:n)-m(i,1:n)*e
            s(j)=s(j)-s(i)*e
        end do
    end do
    return
end subroutine lower
end module
! 求解联立式
program main
    use linearalgebra
    implicit none
    integer, parameter :: n=3 ! size of matrix
    real :: a(n,n)=reshape( (/3,2,1,2,1,-4,1,-1,5/),(/n,n/) )
    real :: s(n)=(/6,2,2/)
    real :: ans(n)
    integer :: i
    write(*,*) 'equation:'
    call output(a,s)
    call gauss_jordan(a,s,ans)
    write(*,*) 'ans:'
    do i=1,n
        write(*,"(1x,a1,'=',f8.4)") char(64+i),ans(i) 
    end do
    stop
end program
