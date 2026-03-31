! 二分法求解
module numerical
    implicit none
    real, parameter :: zero = 0.00001
contains
real function bisect( a, b )
    implicit none
    real a,b,c  
    real fa,fb,fc  

    ! 计算c和f(c)的值
    c = (a+b)/2.0    
    fc = func(c)

    ! f(c)绝对值小于 zero 时,就视为f(c)=0,就结束循环
    do while( abs(fc) > zero )
        fa = func(a)
        fb = func(b)
        if ( fa*fc < 0 ) then
            !f(a)*f(c)<0,以a,c值为新的区间
            b=c
        else
            !不然就以b,c为新的区间
            a=c
        end if
        c=(a+b)/2.0
        fc=func(c)
    end do
    bisect = c
    return
end function

! 求解用的函数
real function func(x)
    implicit none
    real x
    func=(x+3)*(x-3)
    return
end function

end module

program main
    use numerical
    implicit none
    real    a,b        ! 两个猜值
    real    ans        ! 算出的值
    do while(.true.)
        write(*,*) '输入两个猜测值'
        read (*,*) a,b
        ! f(a)*f(b) < 0 的猜值才是有效的猜值
        if ( func(a)*func(b) < 0 ) exit
        write(*,*) "不正确的猜值"
    end do
    ! 调用二叉法求根的函数
    ans=bisect( a, b )
    ! 写出结果
    write(*,"('x=',f6.3)") ans
    stop
end
