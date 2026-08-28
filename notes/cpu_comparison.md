# CPU Model Comparison

## Same workload
RiscvTimingSimpleCPU and RiscvO3CPU execute the same architectural
workload. Both executed 305,769,008 instructions for the full program
and 83,461,430 instructions within the qsort ROI.

## Cache behavior
The two CPU models produced very similar L2 and L3 miss rates across
the tested cache configurations. This indicates that the dominant cache
behavior is determined by the qsort_large memory-access pattern and the
cache hierarchy rather than the CPU model.

## Difference in simulated execution time
Despite similar cache miss rates, RiscvO3CPU completed the workload in
far fewer simulated ticks. The baseline required approximately
978 billion ticks with RiscvTimingSimpleCPU compared with approximately
144 billion ticks with RiscvO3CPU.

## Architectural explanation
RiscvTimingSimpleCPU is an in-order processor model and stalls while
waiting for timing memory accesses to complete. In contrast,
RiscvO3CPU models an out-of-order pipeline with instruction renaming,
instruction scheduling, speculative execution, and multiple in-flight
instructions. It can therefore exploit instruction-level parallelism
and overlap independent computation with some memory latency.

Thus, similar cache miss rates do not imply similar processor
performance. CPU microarchitecture strongly affects how efficiently
memory latency and instruction dependencies are handled.
