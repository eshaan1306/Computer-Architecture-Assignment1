#!/usr/bin/env bash

CPU="${1:-timing}"

printf "%-10s %-6s %-15s %-15s %-15s\n" \
    "L2_SIZE" "ASSOC" "L2_MISS_RATE" "L3_MISS_RATE" "SIM_TICKS"

for CONFIG in \
    "32KiB 4" \
    "64KiB 2" \
    "64KiB 4" \
    "64KiB 8" \
    "256KiB 2" \
    "256KiB 4" \
    "1MiB 2" \
    "1MiB 8"
do
    read -r SIZE ASSOC <<< "$CONFIG"

    STATS="results/raw/l2_${SIZE}_${ASSOC}_${CPU}/stats.txt"

    L2_MISS=$(awk '$1=="system.l2.overallMissRate::total" {print $2}' "$STATS")
    L3_MISS=$(awk '$1=="system.l3.overallMissRate::total" {print $2}' "$STATS")
    TICKS=$(awk '$1=="simTicks" {print $2}' "$STATS")

    printf "%-10s %-6s %-15s %-15s %-15s\n" \
        "$SIZE" "$ASSOC" "$L2_MISS" "$L3_MISS" "$TICKS"
done
