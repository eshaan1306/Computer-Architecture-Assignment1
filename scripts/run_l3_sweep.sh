#!/usr/bin/env bash

set -e

CPU="${1:-timing}"

if [[ "$CPU" != "timing" && "$CPU" != "o3" ]]; then
    echo "Usage: $0 [timing|o3]"
    exit 1
fi

GEM5="../gem5/build/RISCV/gem5.opt"
CONFIG="configs/sweep.py"

L3_CONFIGS=(
    "1MiB 8"
    "1MiB 16"
    "2MiB 8"
    "2MiB 16"
)

# During the L3 sweep, L2 stays at the assignment baseline.
L2_SIZE="512KiB"
L2_ASSOC="4"

for CONFIGURATION in "${L3_CONFIGS[@]}"; do

    read -r L3_SIZE L3_ASSOC <<< "$CONFIGURATION"

    RUN_NAME="l3_${L3_SIZE}_${L3_ASSOC}_${CPU}"
    OUTDIR="results/raw/${RUN_NAME}"

    echo
    echo "=================================================="
    echo "CPU : $CPU"
    echo "L2  : $L2_SIZE, ${L2_ASSOC}-way (FIXED)"
    echo "L3  : $L3_SIZE, ${L3_ASSOC}-way"
    echo "OUT : $OUTDIR"
    echo "=================================================="

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
echo "L3 sweep finished for CPU: $CPU"
