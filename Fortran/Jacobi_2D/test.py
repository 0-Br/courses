import os
import filecmp

for S in (64, 128, 256):
    print("*" * 64)
    print("[Scale: %d]" % S)
    for N in (1, 2, 4, 8):
        print("-" * 16)
        print("[Num of Processes: %d]" % N)
        with open("config.nml", 'w+') as f:
            f.write("&CONFIG\n N=%d,\n S=%d,\n /\n" % (N, S))
        os.system("mpif90 main.F90 -o main")
        os.system("mpirun -np %d main" % N)
        with open("timecost(N=%d)(S=%d)" % (N, S)) as f:
            timecost = float(f.readline())
        if N == 1:
            timecost_S = timecost
        print(">> Timecost: %.6f" % timecost)
        print(">> Sp: %.4f" % (timecost_S / timecost))
        print(">> Ep: %.4f" % (timecost_S / timecost / N))
        if not filecmp.cmp("result(N=%d)(S=%d)" % (1, S), "result(N=%d)(S=%d)" % (N, S)):
            print("<Error!> Inconsistent Results! (N=%d)(S=%d)" % (N, S))
            exit()
    print("[Checks Complete, Results Consistent!]")