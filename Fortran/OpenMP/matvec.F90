program main
	use mpi
	implicit none

	integer MAX_ROWS, MAX_COLS, rows, cols
	parameter (MAX_ROWS = 1000, MAX_COLS = 1000)
	double precision a(MAX_ROWS,MAX_COLS), b(MAX_COLS), c(MAX_ROWS)
	double precision buffer(MAX_COLS), ans

	integer myid, master, numprocs, ierr, status(MPI_STATUS_SIZE)
	integer i, j, numsent, sender
	integer anstype, row

	call mpi_init( ierr )
	call mpi_comm_rank( MPI_COMM_WORLD, myid, ierr )
	call mpi_comm_size( MPI_COMM_WORLD, numprocs, ierr )
	master = 0
	rows = 100
	cols = 100

	if ( myid == master ) then
		!master initializes and then dispatches
		!主进程对矩阵A和B赋初值
		do i=1,cols
			b(i)=1
			do j=1,rows
				a(i,j)=i
			end do
		end do

		numsent=0

		!将矩阵B发送给所有其它的从进程通过下面的广播语句实现
		call mpi_bcast(b,cols,MPI_DOUBLE_PRECISION,master,MPI_COMM_WORLD, ierr)

		!依次将矩阵A的各行发送给其它的numprocs-1个从进程
		do i=1,min(numprocs-1,rows)
			do j=1,cols
				!将一行的数据取出来依次放到缓冲区中
				buffer(j)=a(i,j)
			end do
			!将准备好的一行数据发送出去
			call mpi_send(buffer, cols, MPI_DOUBLE_PRECISION,i,i,MPI_COMM_WORLD, ierr)
			print *, "Process",myid,"send    the ",i,"th row to   Process",i,"."
			numsent=numsent+1
		end do

		do i=1,rows
			!对所有的行依次接收从进程对一行数据的计算结果
			call mpi_recv(ans, 1,MPI_DOUBLE_PRECISION, MPI_ANY_SOURCE,MPI_ANY_TAG,MPI_COMM_WORLD, status, ierr)
			sender=status(MPI_SOURCE)
			anstype=status(MPI_TAG)
			print *, "Process",myid,"receive the ",anstype,"th row from Process",sender,"."
			!将该行数据赋给结果数组C的相应单元
			c(anstype)=ans
			if (numsent < rows) then
				!如果还有其它的行没有被计算则继续发送
				do j=1,cols
					!准备好新一行的数据
					buffer(j)=a(numsent+1,j)
				end do
				!将该行数据发送出去
				call mpi_send(buffer,cols, MPI_DOUBLE_PRECISION, sender,numsent+1,MPI_COMM_WORLD, ierr)
				print *, "Process",myid,"send    the ",numsent+1,"th row to   Process",sender,"."
				numsent=numsent+1
			else
				!若所有行都已发送出去则每接收一个消息则向相应的从进程发送一个标识为0的空消息            !终止该从进程的执行
				call mpi_send(1.0,0,MPI_DOUBLE_PRECISION,sender,0, MPI_COMM_WORLD, ierr)
				print *, "Process",myid,"send    the stop command to Process",sender,"."
			end if
		end do 
	else
		!下面为从进程的执行步骤首先是接收数组B
		call mpi_bcast(b,cols,MPI_DOUBLE_PRECISION,master,MPI_COMM_WORLD, ierr)
		!接收主进程发送过来的矩阵A一行的数据
	90 	call mpi_recv(buffer,cols, MPI_DOUBLE_PRECISION, master,MPI_ANY_TAG, MPI_COMM_WORLD, status,ierr)
		!若接收到标识为非0的消息则进行计算
		if (status(MPI_TAG) /= 0) then
			row=status(MPI_TAG)
			ans=0.0
			do i=1,cols
				ans=ans+buffer(i)*b(i)
			end do
			!计算一行的结果并将结果发送给主进程
			call mpi_send(ans, 1, MPI_DOUBLE_PRECISION,master, row,MPI_COMM_WORLD, ierr)
			goto 90
		end if
	endif

	call mpi_finalize(ierr) 
	stop 
end
