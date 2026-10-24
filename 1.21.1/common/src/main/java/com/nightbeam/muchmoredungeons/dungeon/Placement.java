package com.nightbeam.muchmoredungeons.dungeon;

import java.util.OptionalInt;

/**
 * Picks the height a dungeon is placed at from the ground under its footprint, or rejects the spot. Columns are
 * sampled on a grid over the footprint, before features (trees) are placed.
 */
public final class Placement {
    /** More water than this over the ground at any sampled column and the spot is rejected (rivers, lakes, oceans). */
    public static final int MAX_WATER_DEPTH = 1;

    private Placement() {
    }

    /**
     * @param surface  per column, the first free block above the world surface, water included
     * @param ground   per column, the first free block above the ground, water excluded
     * @param maxSlope the largest height difference between the sampled columns that is still accepted
     * @param yOffset  added to the chosen height (negative sinks the floor into the ground)
     * @param minY     the lowest allowed result (sea level, or the world's bottom plus a margin)
     * @return the y of the template's bottom layer, or empty when the spot is unsuitable
     */
    public static OptionalInt baseY(int[] surface, int[] ground, int maxSlope, int yOffset, int minY) {
        if (surface.length == 0 || surface.length != ground.length) {
            return OptionalInt.empty();
        }
        int lowest = Integer.MAX_VALUE;
        int highest = Integer.MIN_VALUE;
        long sum = 0;
        for (int i = 0; i < ground.length; i++) {
            if (surface[i] - ground[i] > MAX_WATER_DEPTH) {
                return OptionalInt.empty();
            }
            lowest = Math.min(lowest, ground[i]);
            highest = Math.max(highest, ground[i]);
            sum += ground[i];
        }
        if (highest - lowest > maxSlope) {
            return OptionalInt.empty();
        }
        // The average keeps the dungeon level with most of its footprint; terrain adaptation fills or cuts the rest.
        int y = (int) Math.floor((double) sum / ground.length) + yOffset;
        return y < minY ? OptionalInt.empty() : OptionalInt.of(y);
    }

    /** True when a roll in [0, 1) passes the configured spawn chance. */
    public static boolean passes(double roll, double chance) {
        return roll < chance;
    }
}
