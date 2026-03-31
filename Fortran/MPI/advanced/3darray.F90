program main
	use mpi
	implicit none
	
	integer rank, size, ierr
	real a(100,100,100), e(9,9,9) 
    integer oneslice, twoslice, threeslice, sizeofreal 
    integer status(mpi_status_size) 
 
	call mpi_init(ierr)
	call mpi_comm_rank(MPI_COMM_WORLD, rank, ierr)
	call mpi_Comm_size(MPI_COMM_WORLD, size, ierr)
	
	!返回对应数据类型的长度
	call mpi_type_extent( MPI_REAL, sizeofreal, ierr) 
	print *, "sizeofreal=",sizeofreal

	!extract the section a(1:17:2, 3:11, 2:10) and store it in e(:,:,:). 	
	!1D
    call mpi_type_vector( 9, 1, 2, MPI_REAL, oneslice, ierr) 
 
	!2D
    call mpi_type_hvector(9, 1, 100*sizeofreal, oneslice, twoslice, ierr) 
 
	!3D
    call mpi_type_hvector( 9, 1, 100*100*sizeofreal, twoslice, threeslice, ierr) 
 
	call mpi_type_commit( threeslice, ierr) 
    call mpi_sendrecv(a(1,3,2), 1, threeslice, rank, 0, e, 9*9*9, MPI_REAL, rank, 0, MPI_COMM_WORLD, status, ierr) 

	call mpi_finalize(ierr)
end program
