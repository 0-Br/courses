program contiguous
	use mpi
	implicit none

	integer size 
	parameter(size=4)
	integer numtasks, rank, source, dest, tag, i,  ierr
	real*4  a(0:size-1,0:size-1), b(0:size-1)
	integer stat(mpi_status_size)
	integer columntype   ! required variable
	tag = 1

	! fortran stores this array in column major order
	data a  /1.0, 2.0, 3.0, 4.0, &
        	 5.0, 6.0, 7.0, 8.0, &
        	 9.0, 10.0, 11.0, 12.0, & 
        	 13.0, 14.0, 15.0, 16.0 /

	call mpi_init(ierr)
	call mpi_comm_rank(MPI_COMM_WORLD, rank, ierr)
	call mpi_comm_size(MPI_COMM_WORLD, numtasks, ierr)

	! create contiguous derived data type
	call mpi_type_contiguous(size, MPI_REAL, columntype, ierr)
	call mpi_type_commit(columntype, ierr)

	if (numtasks .eq. size) then
    	! task 0 sends one element of columntype to all tasks
    	if (rank .eq. 0) then
        	do i=0, numtasks-1
        		call mpi_send(a(0,i), 1, columntype, i, tag, mpi_comm_world,ierr)
        	end do
 	   endif

   		! all tasks receive columntype data from task 0
    	source = 0
    	call mpi_recv(b, size, MPI_REAL, source, tag, mpi_comm_world, stat, ierr)
    	print *, 'rank= ',rank,' b= ',b
	else
    	print *, 'must specify',size,' processors.  terminating.' 
	endif

	! free datatype when done using it
	call mpi_type_free(columntype, ierr)
	call mpi_finalize(ierr)
end
