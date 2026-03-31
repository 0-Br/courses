      program main
c        this is a homework
         implicit none
         integer a
         integer(kind=8) b
         real*8  c
         real d
         integer*4 e
         a = 10000000000
10       d = 55555555.80
         c = a *                   ! c = a * d
     c       d
         b = c
         d = b / (a/10)
         e = b / (a/10)
         print *,'final result is: ',d, e, b
      endprogram
