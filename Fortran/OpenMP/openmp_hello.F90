program parallel_hello
	use omp_lib
	implicit none
	
	!$omp parallel
    print *, "hello from process: ", omp_get_thread_num()
	!$omp end parallel
end
