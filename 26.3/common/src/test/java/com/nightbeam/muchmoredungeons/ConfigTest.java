package com.nightbeam.muchmoredungeons;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertTrue;

import com.google.gson.JsonObject;
import com.nightbeam.muchmoredungeons.config.CommentedJson;
import com.nightbeam.muchmoredungeons.config.DungeonsConfig;
import com.nightbeam.muchmoredungeons.dungeon.Dungeon;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.io.TempDir;

class ConfigTest {
    @Test
    void defaultsEnableEverything() {
        DungeonsConfig.Values values = DungeonsConfig.Values.defaults();
        assertTrue(values.guardians());
        for (Dungeon dungeon : Dungeon.values()) {
            assertTrue(values.of(dungeon).enabled());
            assertEquals(1.0, values.of(dungeon).chance());
        }
    }

    @Test
    void userValuesAreReadAndChanceIsClamped() {
        JsonObject root = (JsonObject) CommentedJson.parse("""
                // comment
                {"guardians": false, "dungeons": {
                  "tower_dungeon": {"enabled": false},
                  "dungeon_t2": {"chance": 0.25},
                  "soulfire_crypt": {"chance": 7},
                  "outdoor_villa": {"chance": "lots"},
                  "unknown_dungeon": {"enabled": false}
                }}""");
        DungeonsConfig.Values values = DungeonsConfig.read(root);
        assertFalse(values.guardians());
        assertFalse(values.of(Dungeon.TOWER_DUNGEON).enabled());
        assertEquals(1.0, values.of(Dungeon.TOWER_DUNGEON).chance());
        assertEquals(0.25, values.of(Dungeon.DUNGEON_T2).chance());
        assertEquals(1.0, values.of(Dungeon.SOULFIRE_CRYPT).chance());
        assertEquals(1.0, values.of(Dungeon.OUTDOOR_VILLA).chance());
    }

    @Test
    void negativeChanceBecomesZero() {
        JsonObject root = (JsonObject) CommentedJson.parse("{\"dungeons\": {\"tower_dungeon\": {\"chance\": -1}}}");
        assertEquals(0.0, DungeonsConfig.read(root).of(Dungeon.TOWER_DUNGEON).chance());
    }

    @Test
    void fileIsWrittenWithCommentsAndKeepsUserValues(@TempDir Path dir) throws IOException {
        Path file = dir.resolve(DungeonsConfig.FILE);
        Files.writeString(file, "{\"dungeons\": {\"outdoor_villa\": {\"chance\": 0.5}}}");
        DungeonsConfig.load(dir);
        String text = Files.readString(file);
        assertTrue(text.startsWith("// Much More Dungeons."));
        assertTrue(text.contains("\"chance\": 0.5"));
        assertTrue(text.contains("\"soulfire_crypt\""));
        assertEquals(0.5, DungeonsConfig.get().of(Dungeon.OUTDOOR_VILLA).chance());
        DungeonsConfig.load(dir);
        assertEquals(text, Files.readString(file));
    }

    @Test
    void brokenFileFallsBackToDefaultsAndIsLeftAlone(@TempDir Path dir) throws IOException {
        Path file = dir.resolve(DungeonsConfig.FILE);
        Files.writeString(file, "{ this is not json");
        DungeonsConfig.load(dir);
        assertEquals("{ this is not json", Files.readString(file));
        assertTrue(DungeonsConfig.get().of(Dungeon.TOWER_DUNGEON).enabled());
    }

    @Test
    void dungeonIdsAreStable() {
        assertEquals("tower_dungeon", Dungeon.TOWER_DUNGEON.id());
        assertEquals("dungeon_t2_piece", Dungeon.DUNGEON_T2.pieceId());
        assertEquals("chests/soulfire_crypt_vault", Dungeon.SOULFIRE_CRYPT.vaultLootTable());
        assertEquals(Dungeon.OUTDOOR_VILLA, Dungeon.byId("outdoor_villa"));
    }
}
