# ROI vs Full-Program Analysis

## Instruction count
The complete qsort_large execution contains 305,769,008 simulated
instructions, whereas the qsort-only ROI contains 83,461,430
instructions. Therefore, only about 27.3% of the full-program
instructions are executed within the sorting operation itself.

The remaining instructions belong to startup, file input, data
preparation, output, and other program/runtime operations.

## Simulated execution time
For RiscvTimingSimpleCPU, the full program required approximately
978 billion ticks while the qsort ROI required approximately
257 billion ticks. For RiscvO3CPU, the corresponding values were
approximately 144 billion and 43.8 billion ticks.

Thus, measuring the entire program includes a substantial amount of
execution that is unrelated to the sorting operation.

## Cache behavior
The cache miss rates measured within the qsort ROI differ from the
full-program miss rates. For RiscvTimingSimpleCPU, the L2 miss rate
decreased from 35.1769% to 34.2117%, while the L3 miss rate decreased
from 70.5563% to 65.0524%.

RiscvO3CPU showed nearly identical changes.

This demonstrates that the input, preparation, and output phases have
different memory-access patterns from the qsort operation and therefore
affect the full-program cache statistics.

## Importance of ROI measurement
Using m5_dump_reset_stats immediately before and after qsort isolates
the architectural statistics of the sorting operation. This prevents
startup, input processing, data preparation, and output from biasing
the measurements of the region of interest.

## CPU comparison within the ROI
Both CPU models execute exactly 83,461,430 instructions within the ROI
and show nearly identical cache miss rates. However, RiscvO3CPU
requires far fewer simulated ticks. This reinforces the conclusion that
the performance difference between the CPU models arises primarily from
their microarchitectural execution behavior rather than substantially
different cache locality.
