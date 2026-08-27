#!/usr/bin/env bash

CPU="${1:-timing}"

printf "%-10s %-6s %-15s %-15s %-15s\n" \
    "L3_SIZE" "ASSOC" "L2_MISS_RATE" "L3_MISS_RATE" "SIM_TICKS"

for CONFIG in \
    "1MiB 8" \
    "1MiB 16" \
    "2MiB 8" \
    "2MiB 16"
do
    read -r SIZE ASSOC <<< "$CONFIG"

    STATS="results/raw/l3_${SIZE}_${ASSOC}_${CPU}/stats.txt"

    L2_MISS=$(awk '$1=="system.l2.overallMissRate::total" {print $2}' "$STATS")
    L3_MISS=$(awk '$1=="system.l3.overallMissRate::total" {print $2}' "$STATS")
    TICKS=$(awk '$1=="simTicks" {print $2}' "$STATS")

    printf "%-10s %-6s %-15s %-15s %-15s\n" \
        "$SIZE" "$ASSOC" "$L2_MISS" "$L3_MISS" "$TICKS"
done
