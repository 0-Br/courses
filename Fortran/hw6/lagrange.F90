module Lagrange_Interpolation
    ! 拉格朗日插值方法的实现，部分参考了老师提供的示例代码
    implicit none
    type point
        real(kind=8) :: x, y
    end type
    real(kind=8), intrinsic :: sin, exp

    real(kind=8), parameter :: PI = 3.141592653589793 ! 16位有效数字
    real(kind=8), parameter :: MIN = PI * (-1), MAX = PI ! range: [-pi, pi]
    type(point) :: points(65536)
    integer :: n

    contains

    subroutine init(n_init)
        ! 初始化
        integer, intent(in) :: n_init
        integer :: i
        n = n_init
        do i = 1, n
            points(i) % x = MAX * (i - 1) / (n - 1) + MIN * (n - i) / (n - 1)
            points(i) % y = cal_a(points(i) % x)
        end do
    end subroutine

    real(kind=8) function cal_a(x_in)
        ! 解析计算方法
        real(kind=8), intent(in) :: x_in
        cal_a = exp(x_in) * sin(x_in)
    end function

    real(kind=8) function cal_ip(x_in)
        ! 插值计算方法
        real(kind=8), intent(in) :: x_in
        real(kind=8) :: delta
        integer :: i, j
        cal_ip = 0
        do i = 1, n
            delta = points(i) % y
            do j = 1, n
                if (j .ne. i) then
                    delta = delta * (x_in - points(j) % x) / (points(i) % x - points(j) % x)
                end if
            end do
            cal_ip = cal_ip + delta
        end do
    end function
end module

program main
    use Lagrange_Interpolation
    implicit none
    real(kind=8), intrinsic :: abs

    integer :: i, j
    integer, parameter :: n_test = 4
    real(kind=8) :: x_array(n_test), y_array(n_test), y_true_array(n_test), err_array(n_test), err_min, err_max, score

    do i = 4, 16, 4
        call init(i)
        score = 0
        err_min = 2
        err_max = -2
        write(*, "(A)") "****************************************************************"
        write(*, "(A, I0)") "Number of Interpolated Nodes: ", n
        write(*, "(A4, A2, A19, A2, A19, A2, A19, A2, A19)") &
                " id ", "", "         x         ", "", "   y(interpolated)   ", "", &
                "  y(analytical)  ", "", "       error       "
        do j = 1, n_test
            x_array(j) = 3.0 * (j - 1) / (n_test - 1) + (-3.0) * (n_test - j) / (n_test - 1)
            y_array(j) = cal_ip(x_array(j))
            y_true_array(j) = cal_a(x_array(j))
            err_array(j) = abs(y_array(j) - y_true_array(j))
            score = score + err_array(j)
            if (err_array(j) < err_min) err_min = err_array(j)
            if (err_array(j) > err_max) err_max = err_array(j)
            write(*, "(I4, A2, E19.10, A2, E19.10, A2, E19.10, A2, E19.10)") &
                    j, "", x_array(j), "", y_array(j), "", y_true_array(j), "", err_array(j)
        end do
        score = score / n_test
        write(*, "(A, E19.10)") ">> error_min: ", err_min
        write(*, "(A, E19.10)") ">> error_max: ", err_max
        write(*, "(A, E19.10)") ">>     score: ", score
        if (err_min < 0.000001) write(*, "(A)") "[MIN Accepted!]"
        if (err_max < 0.000001) write(*, "(A)") "[MAX Accepted!]"
        if (score < 0.000001) write(*, "(A)") "[AVG Accepted!]"
    end do

end program
