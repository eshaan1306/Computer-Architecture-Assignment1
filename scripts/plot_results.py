from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt


ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "results" / "processed"
PLOTS = ROOT / "plots"

PLOTS.mkdir(parents=True, exist_ok=True)


# ---------------------------------------------------------
# L2 MISS-RATE PLOT
# ---------------------------------------------------------

l2 = pd.read_csv(DATA / "l2_sweep.csv")

l2["configuration"] = (
    l2["l2_size_kib"].astype(str)
    + " KiB / "
    + l2["l2_assoc"].astype(str)
    + "-way"
)

# Convert fraction -> percentage.
l2["miss_percent"] = l2["l2_miss_rate"] * 100


fig, ax = plt.subplots(figsize=(10, 6))

for cpu, label in [
    ("timing", "RiscvTimingSimpleCPU"),
    ("o3", "RiscvO3CPU"),
]:
    subset = l2[l2["cpu"] == cpu]

    ax.plot(
        subset["configuration"],
        subset["miss_percent"],
        marker="o",
        label=label,
    )

ax.set_xlabel("L2 cache configuration")
ax.set_ylabel("L2 overall miss rate (%)")
ax.set_title("L2 Cache Miss Rate vs Cache Configuration")
ax.legend()
ax.grid(True, alpha=0.3)

plt.xticks(rotation=35, ha="right")
plt.tight_layout()

fig.savefig(
    PLOTS / "l2_miss_rate.png",
    dpi=300,
)

plt.close(fig)


# ---------------------------------------------------------
# L3 MISS-RATE PLOT
# ---------------------------------------------------------

l3 = pd.read_csv(DATA / "l3_sweep.csv")

l3["configuration"] = (
    l3["l3_size_mib"].astype(str)
    + " MiB / "
    + l3["l3_assoc"].astype(str)
    + "-way"
)

l3["miss_percent"] = l3["l3_miss_rate"] * 100


fig, ax = plt.subplots(figsize=(9, 6))

for cpu, label in [
    ("timing", "RiscvTimingSimpleCPU"),
    ("o3", "RiscvO3CPU"),
]:
    subset = l3[l3["cpu"] == cpu]

    ax.plot(
        subset["configuration"],
        subset["miss_percent"],
        marker="o",
        label=label,
    )

ax.set_xlabel("L3 cache configuration")
ax.set_ylabel("L3 overall miss rate (%)")
ax.set_title("L3 Cache Miss Rate vs Cache Configuration")
ax.legend()
ax.grid(True, alpha=0.3)

plt.xticks(rotation=25, ha="right")
plt.tight_layout()

fig.savefig(
    PLOTS / "l3_miss_rate.png",
    dpi=300,
)

plt.close(fig)


print("Generated:")
print(PLOTS / "l2_miss_rate.png")
print(PLOTS / "l3_miss_rate.png")
