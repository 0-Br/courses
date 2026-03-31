program main
	use mpi
	implicit none

	integer rank, size, ierr
	integer packsize, position
	integer a
	real 	b
	character  packbuf(100)

	call mpi_init(ierr)
	call mpi_comm_rank(MPI_COMM_WORLD, rank, ierr)
	call mpi_Comm_size(MPI_COMM_WORLD, size, ierr)

	a=9999
	b=1.1
 	if (rank == 0) then 
 	    packsize = 0
 	    call MPI_Pack( a, 1, MPI_INT, packbuf, 100, packsize, MPI_COMM_WORLD, ierr)
 	    call MPI_Pack( b, 1, MPI_DOUBLE, packbuf, 100, packsize, MPI_COMM_WORLD, ierr )
 	endif	
	
    call mpi_bcast( packsize, 1, MPI_INT, 0, MPI_COMM_WORLD, ierr )
    call mpi_bcast( packbuf, packsize, MPI_PACKED, 0, MPI_COMM_WORLD, ierr )
    
    if (rank /= 0) then 
        position = 0
        call MPI_Unpack( packbuf, packsize, position, a, 1, MPI_INT, MPI_COMM_WORLD, ierr )
        call MPI_Unpack( packbuf, packsize, position, b, 1, MPI_DOUBLE,MPI_COMM_WORLD, ierr )
    endif	
    
    print *, "Process ", rank, " got", a, b

	call mpi_finalize(ierr)
end program
