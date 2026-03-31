program jacobi2
	use mpi
	implicit none
	!定义数组的规模
	integer,parameter:: totalsize = 16
	integer,parameter:: mysize    = totalsize/4
	integer,parameter:: steps     = 100
	integer n, myid, numprocs, i, j, rc
	real a(totalsize,mysize+2),b(totalsize,mysize+2)

	integer begin_col, end_col, ierr
	integer status(MPI_STATUS_SIZE)
	integer left,right,tag1,tag2

	call mpi_init( ierr )
	call mpi_comm_rank( MPI_COMM_WORLD, myid, ierr )
	call mpi_comm_size( MPI_COMM_WORLD, numprocs, ierr )

	!数组初始化
	do j=1,mysize+2
		do i=1,totalsize
			a(i,j)=0.0
		enddo
	end do

	if (myid == 0) then
		do i=1,totalsize
			a(i,2)=8.0
		enddo
	end if

	if (myid == 3) then
		do i=1,totalsize
			a(i,mysize+1)=8.0
		enddo
	end if

	do i=1,mysize+2
		a(1,i)=8.0
		a(totalsize,i)=8.0
	enddo

	tag1=3
	tag2=4
	!设置当前进程左右两侧的进程标识
	if (myid > 0) then
		left = myid-1
	else
		left = MPI_PROC_NULL
	end if
	if (myid < 3) then
		right = myid+1
	else
		right = MPI_PROC_NULL
	end if

	!jacobi 迭代部分
	do n=1,steps
		!从左向右平移数据
		call MPI_SENDRECV(a(1,mysize+1),totalsize,MPI_REAL,right,&
				tag1,a(1,1),totalsize,MPI_REAL,left,tag1,MPI_COMM_WORLD,status,ierr)
		!从右向左平移数据
		call MPI_SENDRECV(a(1,2),totalsize,MPI_REAL,left,&
	            tag2,a(1,mysize+2),totalsize,MPI_REAL,right,tag2,MPI_COMM_WORLD,status,ierr)

		begin_col=2
		end_col=mysize+1

		if (myid == 0) then
			begin_col=3
		endif

		if (myid == 3) then
			end_col=mysize
		endif

		do j=begin_col,end_col
			do i=2,totalsize-1
				b(i,j)=(a(i,j+1)+a(i,j-1)+a(i+1,j)+a(i-1,j))*0.25
			enddo
		enddo

		do j=begin_col,end_col
			do i=2,totalsize-1
				a(i,j)=b(i,j)
			enddo
		enddo

	enddo

	do i=2,totalsize-1
		print *, myid,(a(i,j),j=begin_col,end_col)
	enddo

	call mpi_finalize(rc)
end program
