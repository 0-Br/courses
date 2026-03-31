!   输入为："Name: Xiaoming Wang      Age: 22   Weight: 67.5   "
!   输入为："Name: Xiaoming Wang;     Age: 22;  Weight: 67.5   "
!   输出为："He said that: "His name is "Xiaoming Wang". He is 022 years old. His weight is 6.750E+01 kg"."

program main

    implicit none

    character(len=128) name
    integer age
    real weight

    read(*, "(6X, A15, 9X, I2, 11X, E4.1, A)") name, age, weight

    write(*, "(A, A13, A, I3.3, A, ES9.3E2, A)") &
    'He said that: "His name is "', trim(name), '". He is ', age, ' years old. His weight is ', weight, ' kg".'

end program main