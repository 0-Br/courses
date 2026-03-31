program main 
	use mpi
    implicit none
	integer rank, size, ierr
    integer value
	integer status(MPI_STATUS_SIZE)	
    call mpi_init(ierr) 
    call mpi_comm_rank(MPI_COMM_WORLD, rank, ierr) 
    call mpi_comm_size(MPI_COMM_WORLD, size, ierr)

    do while (value .ge. 0)
        if (rank == 0) then 
            read(*,*) value 
        endif
        call MPI_Bcast( value, 1, MPI_INT, 0, MPI_COMM_WORLD , ierr)
       	print *, "Process %d got %d\n", rank, value 
   	enddo 
    
	call mpi_finalize(ierr) 
    stop
end program 
