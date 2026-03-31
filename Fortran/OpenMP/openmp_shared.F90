program parallel_shared
    use omp_lib
    integer :: partial_sum, total_sum
    
    !$omp parallel private(partial_sum) shared(total_sum)
        partial_sum = 0;
        total_sum = 0;

        !$omp do
        do i=1,1000
            partial_sum = partial_sum + i 
        end do
        !$omp end do

        !$omp critical
        total_sum = total_sum + partial_sum
        !$omp end critical
    !$omp end parallel
    print *, "total sum:", total_sum
end

