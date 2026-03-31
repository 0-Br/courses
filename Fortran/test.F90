Program array

	implicit none

	integer :: IX, JY, KZ
	integer :: array1(-1:1, -1:3), array2(2, 4), array3(2, 4)

	DO IX=1,15
		array1(mod(IX-1,3)-1,(IX-1)/3-1)=IX
	ENDDO

	write(6,*) 'array1', array1

	array2 = array1(-1:0,-1:2)
	array3 = array1(0:1,0:3)
	write(6,*) 'array2', array2
	write(6,*) 'array3', array3

	array2(1, 1) = 10086
	write(6,*) 'array1', array1
	write(6,*) 'array2', array2

END Program
