program jacobi 
  use mpi
  implicit none
  !定义数组的规模
  integer,parameter:: totalsize = 16
  integer,parameter:: mysize    = totalsize/4
  integer,parameter:: steps     = 10
  integer n, myid, numprocs, i, j, rc
  real a(totalsize,mysize+2),b(totalsize,mysize+2)

  integer begin_col, end_col, ierr
  integer status(MPI_STATUS_SIZE)

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


!Jacobi 迭代部分
do n=1,steps
	  !从右侧的邻居得到数据
	  if (myid < 3) then
		    call MPI_RECV(a(1,mysize+2),totalsize,MPI_REAL,myid+1,10,MPI_COMM_WORLD,status,ierr)
	  endif

	  !向左侧的邻居发送数据
	  if (myid > 0) then
		    call MPI_SEND(a(1,2),totalsize,MPI_REAL,myid-1, 10,MPI_COMM_WORLD,ierr)
	  endif

	  !向右侧的邻居发送数据
	  if (myid < 3) then
		    call MPI_SEND(a(1,mysize+1),totalsize,MPI_REAL,myid+1, 10,MPI_COMM_WORLD,ierr)
	  endif

	  !从左侧的邻居接收数据
	  if (myid > 0) then
	     call MPI_RECV(a(1,1),totalsize,MPI_REAL,myid-1, 10,MPI_COMM_WORLD,status,ierr)
	  endif
	
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

  call MPI_Finalize(rc)
end program
