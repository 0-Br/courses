program mcpi
    implicit none
    integer :: nthrow,hits,i
    real    :: dist,x2,y2,x,y,ratio,pi
    nthrow = 28000000
    hits=0

    do i=1,nthrow
        call random_number(x)
        call random_number(y)

        x2=x*x
        y2=y*y
        dist=sqrt(x2+y2)

        if (dist .le. 1.0) then
            hits=hits+1
        endif
    enddo

    ratio=real(hits)/real(nthrow)
    pi=4.0*ratio
    write(*,"('the value of pi is calculated to be ',f14.8)") pi
end program
