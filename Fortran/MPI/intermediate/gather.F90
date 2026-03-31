program gather
    use mpi  
	integer irecv(4), rank, size, isend

    call mpi_init(ierr)
    call mpi_comm_rank(MPI_COMM_WORLD, rank, ierr)
    call mpi_comm_size(MPI_COMM_WORLD, size, ierr)

	irecv=0
    isend = rank + 999

    call mpi_gather(isend, 1, MPI_INTEGER, irecv, 1, MPI_INTEGER, 0, MPI_COMM_WORLD, ierr)

	if(rank .eq. 0) then
        print *, 'irecv = ', irecv
    endif
    call mpi_finalize(ierr)
end program
