# L3 Sweep Analysis

## Effect of L3 capacity
Increasing the L3 cache size from 1 MiB to 2 MiB produced a very large
reduction in L3 miss rate. For RiscvTimingSimpleCPU, the miss rate
decreased from 70.5563% for 1 MiB, 8-way to 27.5278% for 2 MiB,
8-way. RiscvO3CPU showed nearly identical behavior.

This indicates that qsort_large benefits strongly from additional L3
capacity, since more of the working set can remain cached and fewer
requests need to access main memory.

## Effect of associativity
Increasing associativity from 8-way to 16-way did not improve the L3
miss rate for the tested configurations. At both 1 MiB and 2 MiB, the
16-way cache produced a slightly higher miss rate than the 8-way cache.
Thus, for this workload, increasing capacity was substantially more
effective than increasing associativity.

## Effect on simulation ticks
Despite the large reduction in L3 miss rate when the cache size was
increased, the reduction in total simulation ticks was relatively small.
This shows that L3 misses are only one contributor to overall execution
time and that improvements in cache behavior do not translate
proportionally into total performance improvement.

## Comparison of CPU models
RiscvTimingSimpleCPU and RiscvO3CPU showed almost identical L3
miss-rate trends. This indicates that the L3 behavior is primarily
determined by the workload's memory-access pattern and cache
configuration. However, RiscvO3CPU still completed the workload in far
fewer simulated ticks because of its out-of-order execution capabilities.
