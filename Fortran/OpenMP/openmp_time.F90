program parallel_time
	use omp_lib
	implicit none
	
	integer j
	double precision t1,t2
	t1 = omp_get_wtime()
	!$omp parallel do
	do j=0,2
 		call test()	
 	enddo
	!$omp end parallel do
 	t2 = omp_get_wtime()
	print *,"Totle Time = ", t2-t1
end

subroutine test() 
	use omp_lib
	implicit none

	integer a,i
	double precision t_start,t_end
	a=0
	t_start = omp_get_wtime()
	do i= 0,100000000
		a=i+1;
	enddo	
 	t_end = omp_get_wtime()
	print *,"Time = ", t_end-t_start, "thread: ",omp_get_thread_num()
end subroutine 
