program main 
	use mpi
    implicit none
	integer rank, size, tag, ierr
    integer i, buf(1)
	integer senddata, recvdata
	integer status(MPI_STATUS_SIZE)	
    
	call mpi_init(ierr) 
    call mpi_comm_rank(MPI_COMM_WORLD, rank, ierr) !该进程编号
    call mpi_comm_size(MPI_COMM_WORLD, size, ierr) !总进程数目
  
	buf=9999
	tag=1 
    if(rank==0) then
    	do i=0, 3*(size-1) 
        	call mpi_recv( buf, 1, MPI_INT, MPI_ANY_SOURCE, MPI_ANY_TAG, MPI_COMM_WORLD, status, ierr )
            print *, "Recv message from Porsess",  status(MPI_SOURCE),  " with tag ", status(MPI_TAG)
		enddo
    else 
        do i=0, 3 
            call mpi_send( buf, 1, MPI_INT, 0, rank, MPI_COMM_WORLD, ierr)
            !print *, "Send message from Pocess", rank, " to Process 0", " with tag ", rank 
		enddo
	endif
    call mpi_finalize(ierr) 
    stop
end program main
