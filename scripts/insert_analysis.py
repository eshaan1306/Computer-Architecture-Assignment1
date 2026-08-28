from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
REPORT = ROOT / "report" / "report.md"

text = REPORT.read_text()


cpu_initial = """
Both CPU models executed the same workload and the same number of
architectural instructions, but RiscvO3CPU completed the baseline
simulation in substantially fewer simulated ticks. TimingSimpleCPU
required 978,000,084,000 ticks, whereas RiscvO3CPU required
143,552,496,000 ticks.

The cache miss rates of the two processors were very similar. Therefore,
the large difference in simulated execution time is primarily due to
the CPU microarchitecture rather than substantially different cache
locality. RiscvTimingSimpleCPU is an in-order timing model that waits
for memory accesses, while RiscvO3CPU models out-of-order execution and
can exploit instruction-level parallelism.
""".strip()


l2_analysis = """
Increasing L2 cache capacity produced a strong reduction in L2 miss
rate for both processor models. For RiscvTimingSimpleCPU, the miss rate
decreased from 79.5396% with the 32 KiB, 4-way configuration to
21.9476% with the 1 MiB, 2-way configuration. RiscvO3CPU exhibited
almost the same trend.

Increasing associativity did not monotonically reduce miss rate in the
tested configurations. For example, at 64 KiB the 2-way cache produced
a lower miss rate than the 4-way and 8-way caches for both CPUs.
Therefore, for qsort_large, increasing cache capacity was more
beneficial than increasing associativity within the configurations
tested.

The large decrease in L2 miss rate resulted in a comparatively small
reduction in simulation ticks. This shows that L2 misses are only one
of several contributors to overall processor execution time.

The two CPU models produced nearly overlapping L2 miss-rate curves,
indicating that the dominant L2 behavior was determined by the
workload's memory-access pattern and cache organization rather than the
CPU model.
""".strip()


l3_analysis = """
Increasing L3 capacity from 1 MiB to 2 MiB produced a very large
reduction in L3 miss rate. With RiscvTimingSimpleCPU, the 8-way miss
rate decreased from 70.5563% to 27.5278%. RiscvO3CPU showed almost
identical behavior. This indicates that qsort_large benefits
significantly from the additional L3 capacity.

Increasing associativity from 8-way to 16-way did not improve miss
rate in the tested configurations. At both 1 MiB and 2 MiB, the
16-way cache produced a slightly higher miss rate than the corresponding
8-way cache. Thus, for this workload, increasing capacity was much more
effective than increasing associativity.

The L2 miss rate remained essentially unchanged while L3 was varied,
which confirms that the experiment successfully kept the upper cache
configuration fixed.

Although doubling the L3 capacity dramatically reduced its miss rate,
the reduction in total simulation ticks was relatively small. Therefore,
a reduction in lower-level cache miss rate does not necessarily produce
a proportional improvement in overall execution time.
""".strip()


cpu_analysis = """
RiscvTimingSimpleCPU and RiscvO3CPU executed exactly 305,769,008
instructions during the complete benchmark, demonstrating that both
processors performed the same architectural workload.

Their cache miss-rate trends were also very similar across the L2 and
L3 experiments. However, their simulated execution times differed
substantially. In the baseline configuration, TimingSimpleCPU required
978,000,084,000 ticks while O3CPU required only 143,552,496,000 ticks,
approximately 6.8 times fewer ticks.

This difference arises from the processor microarchitecture.
TimingSimpleCPU executes instructions in order and exposes memory stalls
more directly. RiscvO3CPU models an out-of-order processor that can keep
multiple instructions in flight, schedule ready instructions, perform
register renaming and exploit instruction-level parallelism. Therefore,
similar cache miss rates do not imply similar overall processor
performance.
""".strip()


roi_analysis = """
The complete benchmark executed 305,769,008 instructions, whereas the
qsort-only ROI executed 83,461,430 instructions. Thus, only about
27.3% of the full-program instructions occurred inside the sorting
operation. The remaining instructions belong to startup, input
processing, data preparation, output and other runtime activity.

The ROI also required substantially fewer simulated ticks. For
RiscvTimingSimpleCPU, the full execution required approximately
978.0 billion ticks while the ROI required approximately 256.9 billion
ticks. For RiscvO3CPU, the corresponding values were approximately
143.6 billion and 43.8 billion ticks.

Cache statistics also changed when only qsort was measured. For
TimingSimpleCPU, the L2 miss rate changed from 35.1769% for the full run
to 34.2117% for the ROI, while the L3 miss rate changed from 70.5563%
to 65.0524%. O3CPU showed almost identical differences.

These results show that startup, input processing, data preparation and
output have different memory-access behavior from the sorting operation.
Using the dump/reset markers immediately around qsort therefore gives a
more representative measurement of the architectural behavior of the
sorting computation itself.

Within the ROI, both CPU models executed exactly 83,461,430
instructions and exhibited almost identical cache miss rates. However,
O3CPU still required far fewer simulated ticks, reinforcing that the
main performance difference arises from CPU microarchitecture rather
than substantially different cache locality.
""".strip()


final_observations = """
The experiments show that cache capacity had a stronger influence on
qsort_large miss rate than associativity within the tested
configurations. Increasing L2 capacity substantially reduced L2 misses,
while increasing L3 capacity from 1 MiB to 2 MiB produced a particularly
large reduction in L3 misses.

Higher associativity did not monotonically reduce miss rate for this
workload. This result is specific to the tested cache organizations and
qsort_large access pattern and should not be interpreted as a general
claim that higher associativity is detrimental.

Despite large changes in cache miss rates, changes in total simulation
ticks were comparatively modest. Processor performance therefore
depends on more than cache miss rate alone.

RiscvTimingSimpleCPU and RiscvO3CPU showed almost identical cache
miss-rate trends, but O3CPU completed both the complete workload and the
qsort-only ROI in substantially fewer simulated ticks. This demonstrates
the importance of processor microarchitecture and instruction-level
parallelism.

Finally, the ROI experiment showed that full-program statistics contain
a large amount of behavior unrelated to sorting. Isolating the qsort
call produced different instruction counts, execution times and cache
miss rates, demonstrating why region-of-interest measurement is useful
when evaluating a specific computation.
""".strip()


replacements = {
    "[WRITE CPU COMPARISON]": cpu_initial,
    "[INSERT L2 ANALYSIS]": l2_analysis,
    "[INSERT L3 ANALYSIS]": l3_analysis,
    "[INSERT TIMINGSIMPLE VS O3 ANALYSIS]": cpu_analysis,
    "[INSERT ROI ANALYSIS]": roi_analysis,
    "[INSERT FINAL OBSERVATIONS]": final_observations,
}


for placeholder, replacement in replacements.items():
    if placeholder not in text:
        raise RuntimeError(f"Missing placeholder: {placeholder}")

    text = text.replace(placeholder, replacement)


REPORT.write_text(text)

print("Inserted report analysis successfully.")
