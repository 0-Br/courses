program main

	use mpi
	implicit none

    integer :: narg
    character(len=16) :: arg
	character(len=16) :: info, my_info, buf
    character(len=16), allocatable :: buffers(:)
    integer :: sour, dest
    integer :: i, j
	integer :: id, size_procs, ierr

	integer status(MPI_STATUS_SIZE)
	call MPI_INIT(ierr)
	call MPI_COMM_RANK(MPI_COMM_WORLD, id, ierr)
	call MPI_COMM_SIZE(MPI_COMM_WORLD, size_procs, ierr)

    narg = iargc()
    if (narg .ne. 1) then
        write(*, "(A, I0, A)") "[PID", id, "] Error: Requires and Only Requires ONE Integer Argument!"
        call MPI_Finalize(ierr)
        stop
    end if
    if (size_procs < 2) then
        write(*, "(A, I0, A)") "[PID", id, "] Error: Requires at Least 2 Processes!"
        call MPI_Finalize(ierr)
        stop
    end if
    allocate(buffers(size_procs))

    write(info, "(A)") "Hello"
    write(my_info, "(A, I0, A)") "Hello(id=", id, ")"
    if (id > 0) then
        sour = id - 1
    else
        sour = size_procs - 1
    end if
    if (id < size_procs - 1) then
        dest = id + 1
    else
        dest = 0
    end if

    call getarg(1, arg)
    if (trim(arg) .eq. "1") then
        write(*, "(A, I0, A)") "[PID", id, "] >> Task 1: Relay!"
        call relay()
    else if (trim(arg) .eq. "2") then
        write(*, "(A, I0, A)") "[PID", id, "] >> Task 2: Greetings!"
        call greetings()
    else
        write(*, "(A, I0, A)") "[PID", id, "] Error: The Argument Can Only Be 1 or 2!"
    end if
    deallocate(buffers)
    call MPI_Finalize(ierr)

    contains

    subroutine relay()
        if (id > 0) then
            call MPI_RECV(buf, 16, MPI_CHARACTER, sour, 42, MPI_COMM_WORLD, status, ierr)
            write(*, "(A, I0, A, I0, A, A)") "[PID", id, "] Receive a message from Process ", sour, ": ", trim(buf)
        end if
        call MPI_SEND(info, 16, MPI_CHARACTER, dest, 42, MPI_COMM_WORLD, ierr)
        write(*, "(A, I0, A, I0, A, A)") "[PID", id, "] Send a message to Process ", dest, ": ", trim(info)
        if (id == 0) then
            call MPI_RECV(buf, 16, MPI_CHARACTER, sour, 42, MPI_COMM_WORLD, status, ierr)
            write(*, "(A, I0, A, I0, A, A)") "[PID", id, "] Receive a message from Process ", sour, ": ", trim(buf)
        end if
    end subroutine

    subroutine greetings()
        do i = 0, size_procs - 1
            buf = my_info
            call MPI_BCAST(buf, 16, MPI_CHARACTER, i, MPI_COMM_WORLD, ierr)
            buffers(i + 1) = buf
            if (id .eq. i) then
                do j = 0, size_procs
                    if (id .ne. j) then
                        write(*, "(A, I0, A, I0, A, A)") "[PID", id, "] Send a message to Process ", j, ": ", trim(buf)
                    end if
                end do
            end if
            if (id .ne. i) then
                write(*, "(A, I0, A, I0, A, A)") "[PID", id, "] Receive a message from Process ", i, ": ", trim(buffers(i + 1))
            end if
        end do
    end subroutine

end program main
