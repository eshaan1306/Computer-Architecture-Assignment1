from pathlib import Path
import csv


ROOT = Path(__file__).resolve().parent.parent
RAW = ROOT / "results" / "raw"
OUT = ROOT / "results" / "processed"

OUT.mkdir(parents=True, exist_ok=True)


# ---------------------------------------------------------
# Read one statistics block from stats.txt
# ---------------------------------------------------------

def read_stats(path, block=0):
    text = Path(path).read_text()

    blocks = []
    current = []
    inside = False

    for line in text.splitlines():
        if "Begin Simulation Statistics" in line:
            inside = True
            current = []
            continue

        if "End Simulation Statistics" in line:
            if inside:
                blocks.append(current)
            inside = False
            continue

        if inside:
            current.append(line)

    if block >= len(blocks):
        raise RuntimeError(
            f"{path}: requested block {block}, "
            f"but only {len(blocks)} block(s) exist"
        )

    stats = {}

    for line in blocks[block]:
        parts = line.split()

        if len(parts) >= 2:
            stats[parts[0]] = parts[1]

    return stats


def get_metrics(stats):
    return {
        "sim_ticks": int(stats["simTicks"]),
        "sim_insts": int(stats["simInsts"]),
        "l2_miss_rate": float(
            stats["system.l2.overallMissRate::total"]
        ),
        "l3_miss_rate": float(
            stats["system.l3.overallMissRate::total"]
        ),
    }


def write_csv(filename, rows):
    if not rows:
        return

    path = OUT / filename

    with path.open("w", newline="") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=rows[0].keys()
        )

        writer.writeheader()
        writer.writerows(rows)

    print(f"Wrote {path}")


# ---------------------------------------------------------
# 1. Q1 baseline results
# ---------------------------------------------------------

baseline_rows = []

for cpu, folder in [
    ("timing", "baseline_timing"),
    ("o3", "baseline_o3"),
]:
    stats = read_stats(RAW / folder / "stats.txt")
    metrics = get_metrics(stats)

    baseline_rows.append({
        "cpu": cpu,
        "l2_size_kib": 512,
        "l2_assoc": 4,
        "l3_size_mib": 1,
        "l3_assoc": 8,
        **metrics,
    })

write_csv("baseline.csv", baseline_rows)


# ---------------------------------------------------------
# 2. Q2 L2 sweep
#
# L3 remains fixed at 1 MiB / 8-way.
# ---------------------------------------------------------

l2_configs = [
    ("32KiB", 32, 4),
    ("64KiB", 64, 2),
    ("64KiB", 64, 4),
    ("64KiB", 64, 8),
    ("256KiB", 256, 2),
    ("256KiB", 256, 4),
    ("1MiB", 1024, 2),
    ("1MiB", 1024, 8),
]

l2_rows = []

for cpu in ["timing", "o3"]:
    for folder_size, size_kib, assoc in l2_configs:

        folder = f"l2_{folder_size}_{assoc}_{cpu}"

        stats = read_stats(
            RAW / folder / "stats.txt"
        )

        metrics = get_metrics(stats)

        l2_rows.append({
            "cpu": cpu,
            "l2_size_kib": size_kib,
            "l2_assoc": assoc,
            "l3_size_mib": 1,
            "l3_assoc": 8,
            **metrics,
        })

write_csv("l2_sweep.csv", l2_rows)


# ---------------------------------------------------------
# 3. Q2 L3 sweep
#
# L2 remains fixed at 512 KiB / 4-way.
# ---------------------------------------------------------

l3_configs = [
    ("1MiB", 1, 8),
    ("1MiB", 1, 16),
    ("2MiB", 2, 8),
    ("2MiB", 2, 16),
]

l3_rows = []

for cpu in ["timing", "o3"]:
    for folder_size, size_mib, assoc in l3_configs:

        folder = f"l3_{folder_size}_{assoc}_{cpu}"

        stats = read_stats(
            RAW / folder / "stats.txt"
        )

        metrics = get_metrics(stats)

        l3_rows.append({
            "cpu": cpu,
            "l2_size_kib": 512,
            "l2_assoc": 4,
            "l3_size_mib": size_mib,
            "l3_assoc": assoc,
            **metrics,
        })

write_csv("l3_sweep.csv", l3_rows)


# ---------------------------------------------------------
# 4. Experiment 3: full-run vs qsort-only ROI
#
# ROI stats are block 2 (Python index 1) because:
#
# block 0 = before qsort
# block 1 = qsort only
# block 2 = after qsort
# ---------------------------------------------------------

roi_rows = []

for cpu, baseline_folder, roi_folder in [
    ("timing", "baseline_timing", "roi_timing"),
    ("o3", "baseline_o3", "roi_o3"),
]:

    # Full program
    full_stats = read_stats(
        RAW / baseline_folder / "stats.txt"
    )

    roi_rows.append({
        "cpu": cpu,
        "region": "full",
        **get_metrics(full_stats),
    })

    # qsort() only
    roi_stats = read_stats(
        RAW / roi_folder / "stats.txt",
        block=1
    )

    roi_rows.append({
        "cpu": cpu,
        "region": "qsort_roi",
        **get_metrics(roi_stats),
    })

write_csv("roi_comparison.csv", roi_rows)


print()
print("All results collected successfully.")
