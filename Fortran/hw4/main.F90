program main

    implicit none

    character(len=65536) sentence
    character c
    integer(kind=2) array(65536)
    integer i, j
    integer(kind=8) product

    write(*, "(A)") "[Please enter a sentence containing a number of digits.]"
    write(*, "(A)") "[This programme will extract the non-zero digits in the sentence and find out their product in order.]"

    write(*, "(A)") "[Please enter a sentence!]"
    read(*, "(A)") sentence

    sentence = trim(sentence)
    j = 0
    do i = 1, len(sentence), 1
        c = sentence(i: i)
        if (c > '0' .and. c <= '9') then
            j = j + 1
            read(c, '(I1)') array(j)
        endif
    enddo

    if (j == 0) then
        write(*, "(A)") "[There are no non-zero numbers in the string!]"
        stop
    endif

    write(*, "(A)") "[From left to right, all non-zero numbers in the string are:]"
    product = 1
    do i = 1, j, 1
        write (*, "(I2$)") array(i)
        product = product * array(i)
    enddo
    write(*, "(/A)") "[Their product is:]"
    write(*, "(I0)") product

    write(*, "(A)") "[Below we will calculate the product of these numbers one by one in turn, &
                        exiting when the product is greater than 100000:]"
    product = 1
    do i = 1, j, 1
        product = product * array(i)
        write(*, "(A, I0, A, I0)") "(Multiply by ", array(i), ") current product is: ", product
        if (product > 100000) then
            write(*, "(A)") "Product is already greater than 100000, so we exit!"
            exit
        endif
    enddo
    write(*, "(A)") "[The product is:]"
    write(*, "(I0)") product

end program main
