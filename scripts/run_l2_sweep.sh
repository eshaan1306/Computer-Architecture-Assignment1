#!/usr/bin/env bash

set -e

CPU="${1:-timing}"

if [[ "$CPU" != "timing" && "$CPU" != "o3" ]]; then
    echo "Usage: $0 [timing|o3]"
    exit 1
fi

GEM5="../gem5/build/RISCV/gem5.opt"
CONFIG="configs/sweep.py"

# L2 configurations given in Assignment 1.
# Format: "SIZE ASSOCIATIVITY"
L2_CONFIGS=(
    "32KiB 4"
    "64KiB 2"
    "64KiB 4"
    "64KiB 8"
    "256KiB 2"
    "256KiB 4"
    "1MiB 2"
    "1MiB 8"
)

# L3 must remain fixed during the L2 sweep.
L3_SIZE="1MiB"
L3_ASSOC="8"

for CONFIGURATION in "${L2_CONFIGS[@]}"; do

    read -r L2_SIZE L2_ASSOC <<< "$CONFIGURATION"

    # Make a filesystem-friendly name:
    # 64KiB -> 64KiB, 1MiB -> 1MiB
    RUN_NAME="l2_${L2_SIZE}_${L2_ASSOC}_${CPU}"
    OUTDIR="results/raw/${RUN_NAME}"

    echo
    echo "=================================================="
    echo "CPU : $CPU"
    echo "L2  : $L2_SIZE, ${L2_ASSOC}-way"
    echo "L3  : $L3_SIZE, ${L3_ASSOC}-way (FIXED)"
    echo "OUT : $OUTDIR"
    echo "=================================================="

    # If this experiment already completed successfully,
    # don't waste time running it again.
    if [[ -f "$OUTDIR/stats.txt" ]] &&
       grep -q "End Simulation Statistics" "$OUTDIR/stats.txt"; then

        echo "Already completed -- skipping."
        continue
    fi

    "$GEM5" \
        --outdir="$OUTDIR" \
        "$CONFIG" \
        --cpu "$CPU" \
        --l2-size "$L2_SIZE" \
        --l2-assoc "$L2_ASSOC" \
        --l3-size "$L3_SIZE" \
        --l3-assoc "$L3_ASSOC"

done

echo
echo "L2 sweep finished for CPU: $CPU"
