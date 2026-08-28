import argparse
from pathlib import Path

import m5
from m5.objects import *


parser = argparse.ArgumentParser()
parser.add_argument(
    "--cpu",
    choices=["timing", "o3"],
    default="timing",
    help="CPU model to simulate",
)
args = parser.parse_args()


# ---------------------------------------------------------
# Cache definitions
# ---------------------------------------------------------

class L1ICache(Cache):
    size = "16KiB"
    assoc = 2
    tag_latency = 2
    data_latency = 2
    response_latency = 2
    mshrs = 4
    tgts_per_mshr = 20


class L1DCache(Cache):
    size = "16KiB"
    assoc = 2
    tag_latency = 2
    data_latency = 2
    response_latency = 2
    mshrs = 4
    tgts_per_mshr = 20


class L2Cache(Cache):
    size = "512KiB"
    assoc = 4
    tag_latency = 10
    data_latency = 10
    response_latency = 10
    mshrs = 16
    tgts_per_mshr = 12


class L3Cache(Cache):
    size = "1MiB"
    assoc = 8
    tag_latency = 20
    data_latency = 20
    response_latency = 20
    mshrs = 32
    tgts_per_mshr = 12


# ---------------------------------------------------------
# System
# ---------------------------------------------------------

system = System()

system.clk_domain = SrcClockDomain()
system.clk_domain.clock = "1GHz"
system.clk_domain.voltage_domain = VoltageDomain()

system.mem_mode = "timing"
system.mem_ranges = [AddrRange("512MiB")]
system.cache_line_size = 64


# ---------------------------------------------------------
# CPU
# ---------------------------------------------------------

if args.cpu == "timing":
    system.cpu = RiscvTimingSimpleCPU()
else:
    system.cpu = RiscvO3CPU()


# ---------------------------------------------------------
# Cache hierarchy
#
# CPU
#  |-- L1I
#  |-- L1D
#       |
#      L2
#       |
#      L3
#       |
#     Memory
# ---------------------------------------------------------

system.l1i = L1ICache()
system.l1d = L1DCache()

system.l2bus = L2XBar()
system.l2 = L2Cache()

system.l3bus = L2XBar()
system.l3 = L3Cache()

system.membus = SystemXBar()


# CPU <-> L1
system.cpu.icache_port = system.l1i.cpu_side
system.cpu.dcache_port = system.l1d.cpu_side

# L1 <-> L2 bus
system.l1i.mem_side = system.l2bus.cpu_side_ports
system.l1d.mem_side = system.l2bus.cpu_side_ports

# L2 bus <-> L2
system.l2.cpu_side = system.l2bus.mem_side_ports

# L2 <-> L3 bus
system.l2.mem_side = system.l3bus.cpu_side_ports

# L3 bus <-> L3
system.l3.cpu_side = system.l3bus.mem_side_ports

# L3 <-> main memory bus
system.l3.mem_side = system.membus.cpu_side_ports


# ---------------------------------------------------------
# Main memory
# ---------------------------------------------------------

system.mem_ctrl = MemCtrl()
system.mem_ctrl.dram = DDR3_1600_8x8()
system.mem_ctrl.dram.range = system.mem_ranges[0]
system.mem_ctrl.port = system.membus.mem_side_ports

system.system_port = system.membus.cpu_side_ports


# ---------------------------------------------------------
# Interrupts / threads
# ---------------------------------------------------------

system.cpu.createInterruptController()
system.cpu.createThreads()


# ---------------------------------------------------------
# qsort_large workload
# ---------------------------------------------------------

repo_root = Path(__file__).resolve().parent.parent
qsort_dir = repo_root / "benchmarks" / "qsort"

binary = qsort_dir / "qsort_large_roi.riscv"
input_file = qsort_dir / "input_large.dat"
output_file = qsort_dir / "output_large.txt"

system.workload = SEWorkload.init_compatible(str(binary))

process = Process()
process.cmd = [str(binary), str(input_file)]
process.output = str(output_file)

system.cpu.workload = process


# ---------------------------------------------------------
# Start simulation
# ---------------------------------------------------------

root = Root(full_system=False, system=system)

m5.instantiate()

print(f"Starting simulation with CPU model: {args.cpu}")

exit_event = m5.simulate()

print(
    f"Exiting @ tick {m5.curTick()} because "
    f"{exit_event.getCause()}"
)
