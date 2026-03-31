program parallel_private
	use omp_lib

	integer :: thread_id

	!$omp parallel private(thread_id)
    thread_id = omp_get_thread_num()
    print *, "hello from process: ", thread_id
	!$omp end parallel
end
