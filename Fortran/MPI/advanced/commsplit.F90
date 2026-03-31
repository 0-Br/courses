program main
	use mpi
	implicit none
	integer world_rank, world_size, row_rank, row_size, row_comm, ierr
	integer color, key	
	call mpi_init(ierr)
	call mpi_comm_rank(MPI_COMM_WORLD, world_rank, ierr)
	call mpi_Comm_size(MPI_COMM_WORLD, world_size, ierr)

	color = mod(world_rank, 3)
	key   = world_rank/3

	! determine color based on row split the communicator based on the color and use the original rank for ordering
	call mpi_comm_split(MPI_COMM_WORLD, color, key, row_comm, ierr)

	call mpi_comm_rank(row_comm, row_rank, ierr)
	call mpi_comm_size(row_comm, row_size, ierr)

	print *,"world rank=",world_rank, "world_size=",world_size,"row_rank=", row_rank,"row_size=", row_size

	call mpi_comm_free(row_comm,ierr)
	call mpi_finalize(ierr)
end program

