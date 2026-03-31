# !/bin/bash

# Task 1
for i in 1 2 3
do
    mkdir -p /tmp/liubr/dir$i
done

# Task 2
cd /tmp/liubr

# Task 3
cp -r /tmp/files_liubr test

# Task 4
chmod -R 750 test

# Task 5
find test -type f -size +100c | awk '{system("mv "$0" /tmp/liubr/dir1")}'
