# Final Experimental Observations

1. Increasing cache capacity produced the strongest reduction in cache
   miss rate. Both the L2 and L3 experiments showed that qsort_large
   benefited substantially from larger caches.

2. Increasing associativity did not monotonically reduce miss rate in
   the tested configurations. For this workload, increasing cache
   capacity was more beneficial than increasing associativity.

3. Large reductions in cache miss rate resulted in comparatively small
   reductions in total simulation ticks. Therefore, cache miss rate is
   an important performance factor but does not alone determine total
   execution time.

4. RiscvTimingSimpleCPU and RiscvO3CPU exhibited almost identical cache
   miss-rate trends, indicating that cache locality was primarily
   determined by the qsort_large workload and cache organization.

5. Despite similar cache behavior and identical architectural
   instruction counts, RiscvO3CPU required substantially fewer
   simulated ticks. The baseline O3 execution required about 6.81 times
   fewer ticks than TimingSimpleCPU. This demonstrates the importance
   of CPU microarchitecture and instruction-level parallelism.

6. The qsort-only ROI contained 83,461,430 instructions compared with
   305,769,008 instructions for the complete application. Thus, only
   about 27.3% of the full-program instructions belong to the sorting
   operation itself.

7. ROI cache miss rates differed from full-program miss rates,
   especially at L3. This demonstrates that startup, input processing,
   data preparation, and output have different memory-access behavior
   and can bias full-program statistics.

8. Within the qsort ROI, both CPUs again showed nearly identical cache
   miss rates but very different simulated execution times. Therefore,
   the performance difference between the CPU models is primarily due
   to their microarchitectural execution behavior rather than a major
   difference in cache locality.
