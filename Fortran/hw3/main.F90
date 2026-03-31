program main

    implicit none

    character(len=65536) text_1, text_2, text_3
    character(len=65536) temp

    write(*, "(A)") "[This programme will incrementally sort three strings in dictionary order.]"

    write(*, "(A)") "[Please enter the FIRST string!]"
    read(*, "(A)") text_1
    write(*, "(A)") "[Please enter the SECOND string!]"
    read(*, "(A)") text_2
    write(*, "(A)") "[Please enter the THIRD string!]"
    read(*, "(A)") text_3

    if (text_2 > text_1) then
        temp = text_1
        text_1 = text_2
        text_2 = temp
    end if

    if (text_3 > text_1) then
        temp = text_1
        text_1 = text_3
        text_3 = temp
    end if

    if (text_3 > text_2) then
        temp = text_2
        text_2 = text_3
        text_3 = temp
    end if

    write(*, "(A)") "[The sorted strings are:]"
    write(*, "(A)") trim(text_1)
    write(*, "(A)") trim(text_2)
    write(*, "(A)") trim(text_3)

end program main
