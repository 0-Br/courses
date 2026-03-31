program hygrid_pi 
	use mpi
	use omp_lib
	integer :: i,n,myid ,numtasks ,ierr ,rc
	double precision,parameter :: pi25dt=3.141592653589793238462643d0
	double precision :: a,h,mypi,pi,sum,x

	call mpi_init( ierr )
	call mpi_comm_rank( MPI_COMM_WORLD, myid, ierr )
	call mpi_comm_size( MPI_COMM_WORLD , numtasks , ierr )

	if(myid .eq. 0)then 
        read(*,*) n 
	endif
	
	call mpi_bcast(n,1,MPI_INTEGER ,0,MPI_COMM_WORLD ,ierr)
	
	h=1.0d0/n
	sum = 0.0d0
	
	!$omp parallel do reduction(+:sum) private(i,x)
	do i = myid+1, n, numtasks
		x = h * (dble(i)-0.5d0)
		sum = sum +4.d0 / (1.d0 + x*x)
	end do
	!$omp end parallel do 
	
	mypi=h*sum
	call mpi_reduce(mypi,pi,1,MPI_DOUBLE_PRECISION,MPI_SUM,0, MPI_COMM_WORLD ,ierr)

	if (myid .eq. 0) then
		print *, pi, abs(pi-pi25dt) 
	endif
	call mpi_finalize(ierr)
end program 
