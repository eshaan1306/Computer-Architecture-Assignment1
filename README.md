# CSE/ECE 511 - Computer Architecture Assignment 1

gem5-based study of CPU and cache hierarchy performance using the
MiBench qsort_large benchmark on RISC-V.

## CPU Models

- RiscvTimingSimpleCPU
- RiscvO3CPU

## Baseline Cache Hierarchy

- L1 Instruction Cache: 16 kB, 2-way, latency 2
- L1 Data Cache: 16 kB, 2-way, latency 2
- L2 Cache: 512 kB, 4-way, latency 10
- L3 Cache: 1 MB, 8-way, latency 20

## Repository Structure

- configs/ - gem5 configuration scripts
- benchmarks/ - benchmark source/input files
- scripts/ - experiment automation and data extraction
- results/ - processed and raw simulation results
- plots/ - generated graphs
- report/ - assignment report
- notes/ - experiment and viva notes
