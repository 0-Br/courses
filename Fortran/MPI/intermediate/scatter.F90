 program scatter
	use mpi  
    integer isend(4), recv, rank, size

    call mpi_init(ierr)
    call mpi_comm_rank(MPI_COMM_WORLD, rank, ierr)
    call mpi_comm_size(MPI_COMM_WORLD, size, ierr)

	if(rank .eq. 0) then
    	do i=1,size
           isend(i) = i
        enddo
    endif

	call mpi_scatter(isend, 1, MPI_INTEGER,irecv, 1, MPI_INTEGER, 0, MPI_COMM_WORLD, ierr)

      print *, 'rank = ', rank , ': ','irecv= ', irecv
      call mpi_finalize(ierr)
 end program
