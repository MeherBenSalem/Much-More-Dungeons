package com.nightbeam.muchmoredungeons.config;

import com.google.gson.JsonObject;
import com.nightbeam.muchmoredungeons.dungeon.Dungeon;
import java.nio.file.Path;
import java.util.EnumMap;
import java.util.Map;

/**
 * {@code config/muchmoredungeons.json}: which dungeons generate, how often a valid spot is used, and whether guardians
 * spawn. Read once at startup. Spacing, separation and biomes are datapack data (see the README).
 */
public final class DungeonsConfig {
    public static final String FILE = "muchmoredungeons.json";

    private static volatile Values values = Values.defaults();

    private DungeonsConfig() {
    }

    public record Settings(boolean enabled, double chance) {
    }

    public record Values(boolean guardians, Map<Dungeon, Settings> dungeons) {
        public static Values defaults() {
            return read(spec().defaults());
        }

        public Settings of(Dungeon dungeon) {
            return dungeons.get(dungeon);
        }
    }

    public static CommentedJson spec() {
        JsonObject dungeons = new JsonObject();
        for (Dungeon dungeon : Dungeon.values()) {
            dungeons.add(dungeon.id(), Json.obj("enabled", true, "chance", 1.0));
        }
        CommentedJson spec = new CommentedJson(Json.obj("guardians", true, "dungeons", dungeons))
                .header("""
                        Much More Dungeons. Changes apply after a restart and only to chunks generated afterwards.
                        Spacing, separation and biomes are datapack data: see the README on GitHub.""")
                .comment("guardians", "Spawn each dungeon's named guardian when the dungeon generates.")
                .comment("dungeons", """
                        Per dungeon: "enabled" turns it off entirely (it can then not be located either), "chance"
                        (0 to 1) is the share of valid spots that get one; 0.5 halves how many generate.""");
        return spec;
    }

    public static Values read(JsonObject root) {
        Map<Dungeon, Settings> dungeons = new EnumMap<>(Dungeon.class);
        for (Dungeon dungeon : Dungeon.values()) {
            String path = "dungeons." + dungeon.id();
            double chance = Json.num(root, path + ".chance", 1.0);
            if (Double.isNaN(chance)) {
                chance = 1.0;
            }
            dungeons.put(dungeon, new Settings(Json.bool(root, path + ".enabled", true), Math.max(0.0, Math.min(1.0, chance))));
        }
        return new Values(Json.bool(root, "guardians", true), dungeons);
    }

    public static void load(Path configDir) {
        values = read(spec().load(configDir.resolve(FILE)));
    }

    public static Values get() {
        return values;
    }
}
