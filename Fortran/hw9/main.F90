program main

	use mpi
	implicit none

    real, parameter :: pi_real = 3.14159265358979323846264338 ! 高精度圆周率值
    integer :: n_total, n_local, n_valid, n_valid_total
    integer :: i
    real :: x, y, pi_cal, error
    real :: start, finish
	integer :: id, size_procs, ierr

	integer status(MPI_STATUS_SIZE)
	call MPI_INIT(ierr)
	call MPI_COMM_RANK(MPI_COMM_WORLD, id, ierr)
	call MPI_COMM_SIZE(MPI_COMM_WORLD, size_procs, ierr)

    if (id .eq. 0) then
        read(*, *) n_total
        n_local = n_total / size_procs
    end if
    call MPI_BCAST(n_local, 1, MPI_INTEGER, 0, MPI_COMM_WORLD, ierr)
    n_valid = 0
    if (id .eq. 0) then
        n_local = n_total - (size_procs - 1) * n_local
    end if

    call cpu_time(start)
    do i = 1, n_local
        call random_number(x)
        call random_number(y)
        if (x**2 + y**2 <= 1.0) then
            n_valid = n_valid + 1
        end if
    end do
    call MPI_REDUCE(n_valid, n_valid_total, 1, MPI_INTEGER, MPI_SUM, 0, MPI_COMM_WORLD, ierr)
    call cpu_time(finish)

    if (id == 0) then
        pi_cal = 4.0 * n_valid_total / n_total
        error = abs(pi_cal - pi_real)
        write(*, "(A, F15.12, A)") "Finished! Total Time Cost (s): "
        write(*, "(F18.12)") finish - start
        write(*, "(A)") "The Value of PI Calculated Based on the Parallel Monte Carlo Algorithm:"
        write(*, "(F18.12)") pi_cal
        write(*, "(A)") "Error from True Value is:"
        write(*, "(F18.12)") error
    end if

    call MPI_FINALIZE(ierr)

end program