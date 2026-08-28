from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "results" / "processed"
REPORT = ROOT / "report"

REPORT.mkdir(parents=True, exist_ok=True)


# -----------------------
# L2 configurations
# -----------------------

l2 = pd.read_csv(DATA / "l2_sweep.csv")

l2_table = l2.copy()

l2_table["CPU"] = l2_table["cpu"].map({
    "timing": "RiscvTimingSimpleCPU",
    "o3": "RiscvO3CPU",
})

l2_table["L2 Configuration"] = l2_table.apply(
    lambda r:
        (f"{int(r['l2_size_kib'] / 1024)} MiB"
         if r["l2_size_kib"] >= 1024
         else f"{int(r['l2_size_kib'])} KiB")
        + f", {int(r['l2_assoc'])}-way",
    axis=1
)

l2_table["L2 Miss Rate (%)"] = (
    l2_table["l2_miss_rate"] * 100
).round(4)

l2_table["Simulation Ticks"] = l2_table["sim_ticks"]

l2_table = l2_table[
    [
        "CPU",
        "L2 Configuration",
        "L2 Miss Rate (%)",
        "Simulation Ticks",
    ]
]

l2_table.to_csv(
    REPORT / "l2_results_table.csv",
    index=False
)


# -----------------------
# L3 configurations
# -----------------------

l3 = pd.read_csv(DATA / "l3_sweep.csv")

l3_table = l3.copy()

l3_table["CPU"] = l3_table["cpu"].map({
    "timing": "RiscvTimingSimpleCPU",
    "o3": "RiscvO3CPU",
})

l3_table["L3 Configuration"] = l3_table.apply(
    lambda r:
        f"{int(r['l3_size_mib'])} MiB, "
        f"{int(r['l3_assoc'])}-way",
    axis=1
)

l3_table["L3 Miss Rate (%)"] = (
    l3_table["l3_miss_rate"] * 100
).round(4)

l3_table["Simulation Ticks"] = l3_table["sim_ticks"]

l3_table = l3_table[
    [
        "CPU",
        "L3 Configuration",
        "L3 Miss Rate (%)",
        "Simulation Ticks",
    ]
]

l3_table.to_csv(
    REPORT / "l3_results_table.csv",
    index=False
)

print("Generated result tables.")
