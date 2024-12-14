from numba import jit, cuda
import numba
import numpy as np

# to measure exec time
from timeit import default_timer as timer

N = 100000000


# normal function to run on cpu
def func(a):
    for i in range(N):
        a[i] += 1


# function optimized to run on gpu
# @jit(target_backend="cuda")
@cuda.jit()
def func2(a):
    for i in range(N):
        a[i] += 1


if __name__ == "__main__":
    n = N
    a = np.ones(n, dtype=np.float64)
    d_a = numba.cuda.to_device(a)

    start = timer()
    func(a)
    print("without GPU:", timer() - start)

    start = timer()
    blockspergrid = 64
    threadsperblock = 8
    func2[blockspergrid, threadsperblock](a)
    print("with GPU:", timer() - start)
