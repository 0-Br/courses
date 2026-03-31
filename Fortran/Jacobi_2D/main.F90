program main

    use mpi
    implicit none

    integer :: counter
    integer, parameter :: num_iter = 100 ! 固定迭代100次
    integer :: N, S, var
    integer :: k, m_type
    integer :: i_num, j_num, i_id, j_id, i_type, j_type
    integer :: i, j, i_len, j_len, i_begin, j_begin, i_end, j_end
    integer :: up, down, left, right
    integer, parameter :: tag_up = 0, tag_down = 1, tag_left = 2, tag_right = 3
    real(kind=8), allocatable :: matrix(:, :), buffer(:, :), temp(:, :, :), result(:, :) ! 使用8位浮点数: MPI_REAL8

    character(len=256) :: save_path
    integer :: ts1, ts2
    namelist /config/ N, S

    integer :: id_procs, size_procs, ierr
    integer status(MPI_STATUS_SIZE)
    call MPI_INIT(ierr)
    call MPI_COMM_RANK(MPI_COMM_WORLD, id_procs, ierr)
    call MPI_COMM_SIZE(MPI_COMM_WORLD, size_procs, ierr)

    ! 【读取模块】 读取并检查配置文件，不计入并行运行时间
    if (id_procs .eq. 0) then
        open(42, file="config.nml", status="old", action="read", iostat=var)
        read(42, nml=config)
        close(42)
    end if

    call MPI_BCAST(N, 1, MPI_INT, 0, MPI_COMM_WORLD, ierr)
    call MPI_BCAST(S, 1, MPI_INT, 0, MPI_COMM_WORLD, ierr)
    if (N .ne. size_procs) then
        write(*, "(A, I0, A)") "[PID", id_procs, "] Error: Incorrect Number of Processes!"
        call MPI_FINALIZE(ierr)
        stop
    end if

    ! 【初始化模块】 定义分割方式，并为矩阵赋初值
    if (id_procs .eq. 0) call system_clock(ts1)

    select case (N) ! 考虑到内存访问的局部性，优先按行分割
    case(1)
        i_num = 1
        j_num = 1
    case(2)
        i_num = 1
        j_num = 2
    case(4)
        i_num = 2
        j_num = 2
    case(8)
        i_num = 2
        j_num = 4
    case default
        write(*, "(A, I0, A)") "[PID", id_procs, "] Error: Number of Processes SHOULD Be 1, 2, 4, 8!"
        call MPI_FINALIZE(ierr)
        stop
    end select
    i_id = id_procs / j_num ! 为进程设置二维编号，列方向
    j_id = mod(id_procs, j_num) ! 为进程设置二维编号，行方向

    i_len = S / i_num
    j_len = S / j_num
    allocate(matrix(0: (i_len + 1), 0: (j_len + 1)))
    allocate(buffer(0: (i_len + 1), 0: (j_len + 1)))
    if (id_procs .eq. 0) then
        allocate(temp(0: (i_len + 1), 0: (j_len + 1), 0: (N - 1)))
        allocate(result(S, S))
    end if
    do j = 0, (j_len + 1)
        do i = 0, (i_len + 1)
            matrix(i, j) = 0.0
        end do
    end do
    if (i_id == 0) then
        do j = 1, j_len
            matrix(1, j) = 8.0
        end do
    end if
    if (i_id == (i_num - 1)) then
        do j = 1, j_len
            matrix(i_len, j) = 8.0
        end do
    end if
    if (j_id == 0) then
        do i = 1, i_len
            matrix(i, 1) = 8.0
        end do
    end if
    if (j_id == (j_num - 1)) then
        do i = 1, i_len
            matrix(i, j_len) = 8.0
        end do
    end if

    ! print *, i_id, j_id
    ! print *, matrix(0,:)
    ! print *, matrix(1,:)
    ! print *, matrix(2,:)
    ! print *, matrix(3,:)

    i_begin = 1
    j_begin = 1
    i_end = i_len
    j_end = j_len
    if (i_id > 0) then
        up = (i_id - 1) * j_num + j_id
    else
        i_begin = 2
        up = MPI_PROC_NULL
    end if
    if (i_id < (i_num - 1)) then
        down = (i_id + 1) * j_num + j_id
    else
        i_end = i_len - 1
        down = MPI_PROC_NULL
    end if
    if (j_id > 0) then
        left = i_id * j_num + (j_id - 1)
    else
        j_begin = 2
        left = MPI_PROC_NULL
    end if
    if (j_id < (j_num - 1)) then
        right = i_id * j_num + (j_id + 1)
    else
        j_end = j_len - 1
        right = MPI_PROC_NULL
    endif

    ! print *, i_id, j_id
    ! print *, up, down, left, right

    ! 【通信与计算模块】 各进程间传递边界值，并进行Jacobi迭代，循环num_iter次，最后汇总数据至0号进程
    call MPI_TYPE_CONTIGUOUS(i_len, MPI_REAL8, i_type, ierr)
    call MPI_TYPE_COMMIT(i_type, ierr)
    call MPI_TYPE_VECTOR(j_len, 1, (i_len + 2), MPI_REAL8, j_type, ierr)
    call MPI_TYPE_COMMIT(j_type, ierr)

    do counter = 1, num_iter
        call MPI_SENDRECV(matrix(1, 1), 1, i_type, left, tag_left, &
                          matrix(1, (j_len + 1)), 1, i_type, right, tag_left, &
                          MPI_COMM_WORLD, status, ierr)
        call MPI_SENDRECV(matrix(1, j_len), 1, i_type, right, tag_right, &
                          matrix(1, 0), 1, i_type, left, tag_right, &
                          MPI_COMM_WORLD, status, ierr)
        call MPI_SENDRECV(matrix(1, 1), 1, j_type, up, tag_up, &
                          matrix((i_len + 1), 1), 1, j_type, down, tag_up, &
                          MPI_COMM_WORLD, status, ierr)
        call MPI_SENDRECV(matrix(i_len, 1), 1, j_type, down, tag_down, &
                          matrix(0, 1), 1, j_type, up, tag_down, &
                          MPI_COMM_WORLD, status, ierr)

        do j = j_begin, j_end
            do i = i_begin, i_end
                buffer(i, j) = (matrix(i, (j + 1)) + matrix(i, (j - 1)) + matrix((i + 1), j) + matrix((i - 1), j)) * 0.25
            end do
        end do
        do j = j_begin, j_end
            do i = i_begin, i_end
                matrix(i, j) = buffer(i, j)
            end do
        end do
    end do

    call MPI_TYPE_CONTIGUOUS((i_len + 2) * (j_len + 2), MPI_REAL8, m_type, ierr)
    call MPI_TYPE_COMMIT(m_type, ierr)
    call MPI_GATHER(matrix(0, 0), 1, m_type, temp(0, 0, 0), 1, m_type, 0, MPI_COMM_WORLD, ierr)

    if (id_procs .eq. 0) call system_clock(ts2)

    ! 【保存模块】 将计算结果与运行时间保存到文件中，不计入并行运行时间
    if (id_procs .eq. 0) then
        do k = 0, (N - 1)
            i_id = k / j_num
            j_id = mod(k, j_num)
            do j = 1, j_len
                do i = 1, i_len
                    result((i_id * i_len + i), (j_id * j_len + j)) = temp(i, j, k)
                end do
            end do
        end do
    end if

    if (id_procs .eq. 0) then
        write(save_path, fmt="(A, I0, A, I0, A)") "result(N=", N, ")(S=", S, ")"
        open(3407, file=save_path, status="replace", action="write", iostat=var)
        do i = 1, S
            write(3407, fmt=*) result(i, :)
        end do
        close(3407)
        write(save_path, fmt="(A, I0, A, I0, A)") "timecost(N=", N, ")(S=", S, ")"
        open(12, file=save_path, status="replace", action="write", iostat=var)
        write(12, fmt="(F0.16)") ((ts2 - ts1) / 1000.0)
        close(12)
    end if

    call MPI_TYPE_FREE(m_type, ierr)
    call MPI_TYPE_FREE(j_type, ierr)
    call MPI_TYPE_FREE(i_type, ierr)
    if (id_procs .eq. 0) then
        deallocate(result)
        deallocate(temp)
    end if
    deallocate(buffer)
    deallocate(matrix)

    call MPI_FINALIZE(ierr)

end program main
