from pathlib import Path
import pandas as pd


ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "results" / "processed"
REPORT = ROOT / "report" / "report.md"


def cpu_name(cpu):
    return {
        "timing": "RiscvTimingSimpleCPU",
        "o3": "RiscvO3CPU",
    }[cpu]


def markdown_table(headers, rows):
    lines = []

    lines.append(
        "| " + " | ".join(headers) + " |"
    )

    lines.append(
        "| " + " | ".join(["---"] * len(headers)) + " |"
    )

    for row in rows:
        lines.append(
            "| " + " | ".join(str(x) for x in row) + " |"
        )

    return "\n".join(lines)


# =========================================================
# BASELINE TABLE
# =========================================================

baseline = pd.read_csv(DATA / "baseline.csv")

baseline_rows = []

for _, r in baseline.iterrows():
    baseline_rows.append([
        cpu_name(r["cpu"]),
        f"{int(r['sim_ticks']):,}",
        f"{r['l2_miss_rate'] * 100:.4f}%",
        f"{r['l3_miss_rate'] * 100:.4f}%",
    ])

baseline_table = markdown_table(
    [
        "CPU",
        "Simulation Ticks",
        "L2 Miss Rate",
        "L3 Miss Rate",
    ],
    baseline_rows,
)


# =========================================================
# L2 TABLE
# =========================================================

l2 = pd.read_csv(DATA / "l2_sweep.csv")

l2_rows = []

for _, r in l2.iterrows():

    size = int(r["l2_size_kib"])

    if size >= 1024:
        size_text = f"{size // 1024} MiB"
    else:
        size_text = f"{size} KiB"

    config = (
        f"{size_text}, "
        f"{int(r['l2_assoc'])}-way"
    )

    l2_rows.append([
        cpu_name(r["cpu"]),
        config,
        f"{r['l2_miss_rate'] * 100:.4f}%",
        f"{int(r['sim_ticks']):,}",
    ])

l2_table = markdown_table(
    [
        "CPU",
        "L2 Configuration",
        "L2 Miss Rate",
        "Simulation Ticks",
    ],
    l2_rows,
)


# =========================================================
# L3 TABLE
# =========================================================

l3 = pd.read_csv(DATA / "l3_sweep.csv")

l3_rows = []

for _, r in l3.iterrows():

    config = (
        f"{int(r['l3_size_mib'])} MiB, "
        f"{int(r['l3_assoc'])}-way"
    )

    l3_rows.append([
        cpu_name(r["cpu"]),
        config,
        f"{r['l3_miss_rate'] * 100:.4f}%",
        f"{int(r['sim_ticks']):,}",
    ])

l3_table = markdown_table(
    [
        "CPU",
        "L3 Configuration",
        "L3 Miss Rate",
        "Simulation Ticks",
    ],
    l3_rows,
)


# =========================================================
# ROI TABLE
# =========================================================

roi = pd.read_csv(DATA / "roi_comparison.csv")

roi_rows = []

for _, r in roi.iterrows():

    region = (
        "Full Program"
        if r["region"] == "full"
        else "qsort ROI"
    )

    roi_rows.append([
        cpu_name(r["cpu"]),
        region,
        f"{int(r['sim_ticks']):,}",
        f"{int(r['sim_insts']):,}",
        f"{r['l2_miss_rate'] * 100:.4f}%",
        f"{r['l3_miss_rate'] * 100:.4f}%",
    ])

roi_table = markdown_table(
    [
        "CPU",
        "Region",
        "Simulation Ticks",
        "Instructions",
        "L2 Miss Rate",
        "L3 Miss Rate",
    ],
    roi_rows,
)


# =========================================================
# INSERT EVERYTHING
# =========================================================

text = REPORT.read_text()

replacements = {
    "[INSERT BASELINE CPU TABLE]":
        baseline_table,

    "[INSERT L2 TABLE]":
        l2_table,

    "[INSERT L2 FIGURE]":
        "![L2 Cache Miss Rate](../plots/l2_miss_rate.png)",

    "[INSERT L3 TABLE]":
        l3_table,

    "[INSERT L3 FIGURE]":
        "![L3 Cache Miss Rate](../plots/l3_miss_rate.png)",

    "[INSERT ROI TABLE]":
        roi_table,
}


for placeholder, replacement in replacements.items():

    if placeholder not in text:
        print(f"Warning: placeholder not found: {placeholder}")
        continue

    text = text.replace(
        placeholder,
        replacement,
    )


REPORT.write_text(text)

print(f"Populated {REPORT}")
