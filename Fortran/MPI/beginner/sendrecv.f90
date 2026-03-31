program main 
	use mpi
    implicit none
	integer rank, size, tag, ierr
    integer senddata, recvdata
	integer status(MPI_STATUS_SIZE)	
    call MPI_Init(ierr) 
    call MPI_Comm_rank(MPI_COMM_WORLD, rank, ierr) !该进程编号
    call MPI_Comm_size(MPI_COMM_WORLD, size, ierr) !总进程数目
   
	tag=1 
    if(rank==0) then
        senddata=9999 
		!发送数据到进程1
        call MPI_Send(senddata, 1, MPI_INT, 1, tag, MPI_COMM_WORLD, ierr)  
		print *, "Process",rank,"send ",senddata,"to Process ",rank+1,"."	
	endif
    if(rank==1) then 
		!从进程0接收数据       
        call MPI_Recv(recvdata, 1, MPI_INT, 0, tag, MPI_COMM_WORLD, status, ierr)
		print *, "Process",rank,"receive ",recvdata,"from Process",rank-1,"."	
	endif
    call MPI_Finalize(ierr) 
    stop
end program main
