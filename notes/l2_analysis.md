# L2 Sweep Analysis

## Effect of L2 capacity
Increasing L2 cache capacity significantly reduced the L2 miss rate for
both CPU models. For example, with RiscvTimingSimpleCPU, the miss rate
decreased from 79.5396% for 32 KiB, 4-way to 21.9476% for 1 MiB,
2-way. RiscvO3CPU showed a very similar trend.

## Effect of associativity
Increasing associativity did not monotonically reduce the miss rate for
this workload. At 64 KiB, the 2-way configuration produced a lower miss
rate than the 4-way and 8-way configurations for both CPU models.
Therefore, for qsort_large and the tested configurations, increasing
cache capacity was more beneficial than increasing associativity.

## Effect on simulation ticks
The reduction in miss rate produced only a modest reduction in total
simulation ticks. This indicates that L2 miss behavior is only one of
several factors contributing to overall execution time.

## Comparison of CPU models
RiscvTimingSimpleCPU and RiscvO3CPU produced almost identical L2
miss-rate trends, suggesting that the cache behavior is primarily driven
by the workload and cache organization. However, O3 required far fewer
simulation ticks because its out-of-order execution model can exploit
more instruction-level parallelism and overlap work more effectively.
