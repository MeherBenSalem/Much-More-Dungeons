package com.nightbeam.muchmoredungeons;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertTrue;

import com.nightbeam.muchmoredungeons.dungeon.Placement;
import java.util.OptionalInt;
import org.junit.jupiter.api.Test;

class PlacementTest {
    private static final int MIN = -56;

    @Test
    void flatDryGroundUsesItsHeightPlusOffset() {
        int[] ground = {70, 70, 70, 70, 70};
        assertEquals(OptionalInt.of(69), Placement.baseY(ground, ground, 6, -1, MIN));
    }

    @Test
    void gentleSlopeUsesTheAverage() {
        int[] ground = {68, 70, 72, 70, 71};
        assertEquals(OptionalInt.of(70), Placement.baseY(ground, ground, 6, 0, MIN));
    }

    @Test
    void steepSlopeIsRejected() {
        int[] ground = {64, 64, 64, 64, 80};
        assertTrue(Placement.baseY(ground, ground, 8, 0, MIN).isEmpty());
    }

    @Test
    void slopeAtTheLimitIsAccepted() {
        int[] ground = {64, 64, 64, 64, 72};
        assertTrue(Placement.baseY(ground, ground, 8, 0, MIN).isPresent());
    }

    @Test
    void waterOverAnyColumnIsRejected() {
        int[] surface = {63, 63, 63, 63, 63};
        int[] ground = {63, 63, 63, 63, 58};
        assertTrue(Placement.baseY(surface, ground, 8, 0, MIN).isEmpty());
    }

    @Test
    void aSingleBlockOfWaterIsTolerated() {
        int[] surface = {64, 64, 64, 64, 64};
        int[] ground = {64, 64, 64, 64, 63};
        assertTrue(Placement.baseY(surface, ground, 8, 0, MIN).isPresent());
    }

    @Test
    void tooCloseToTheWorldBottomIsRejected() {
        int[] ground = {-60, -60, -60, -60, -60};
        assertTrue(Placement.baseY(ground, ground, 8, 0, MIN).isEmpty());
    }

    @Test
    void mismatchedOrEmptySamplesAreRejected() {
        assertTrue(Placement.baseY(new int[0], new int[0], 8, 0, MIN).isEmpty());
        assertTrue(Placement.baseY(new int[]{64}, new int[]{64, 64}, 8, 0, MIN).isEmpty());
    }

    @Test
    void chanceRolls() {
        assertTrue(Placement.passes(0.0, 1.0));
        assertTrue(Placement.passes(0.999, 1.0));
        assertFalse(Placement.passes(0.0, 0.0));
        assertTrue(Placement.passes(0.49, 0.5));
        assertFalse(Placement.passes(0.5, 0.5));
    }
}
