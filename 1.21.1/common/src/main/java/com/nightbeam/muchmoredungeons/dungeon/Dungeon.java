package com.nightbeam.muchmoredungeons.dungeon;

/**
 * The four dungeons. Ids are the structure, structure type, template and loot table names and never change, so
 * worlds made with older versions keep working. Everything that is not Minecraft code lives here so it can be tested.
 */
public enum Dungeon {
    OUTDOOR_VILLA("outdoor_villa", "Smuggler's Villa", 1, -1, 7,
            new Guardian("minecraft:vindicator", "Smuggler Chief", 60, 6, 8, "minecraft:iron_axe", "", "")),
    TOWER_DUNGEON("tower_dungeon", "Arcane Spire", 2, -1, 14,
            new Guardian("minecraft:illusioner", "Spire Illusionist", 70, 6, 6, "minecraft:bow", "", "")),
    DUNGEON_T2("dungeon_t2", "Cursed Keep", 3, -1, 10,
            new Guardian("minecraft:zombie", "Keep Warlord", 100, 12, 9, "minecraft:diamond_sword",
                    "minecraft:iron_helmet", "minecraft:iron_chestplate")),
    SOULFIRE_CRYPT("soulfire_crypt", "Soulfire Crypt", 4, -1, 8,
            new Guardian("minecraft:wither_skeleton", "Cinder Warden", 140, 12, 11, "minecraft:diamond_axe",
                    "minecraft:netherite_helmet", "minecraft:chainmail_chestplate"));

    private final String id;
    private final String title;
    private final int tier;
    private final int yOffset;
    private final int maxSlope;
    private final Guardian guardian;

    Dungeon(String id, String title, int tier, int yOffset, int maxSlope, Guardian guardian) {
        this.id = id;
        this.title = title;
        this.tier = tier;
        this.yOffset = yOffset;
        this.maxSlope = maxSlope;
        this.guardian = guardian;
    }

    /** Structure, structure type, template and loot table name. */
    public String id() {
        return id;
    }

    /** Structure piece type name. */
    public String pieceId() {
        return id + "_piece";
    }

    public String title() {
        return title;
    }

    /** Loot tier, 1 (early game) to 4 (late game). */
    public int tier() {
        return tier;
    }

    /** How far the template's floor sits below the ground it is placed on. */
    public int yOffset() {
        return yOffset;
    }

    /** The largest height difference between the footprint's corners the dungeon is still placed on. */
    public int maxSlope() {
        return maxSlope;
    }

    public Guardian guardian() {
        return guardian;
    }

    /** The chest loot table names: the regular chests and the vault (the guarded chest). */
    public String lootTable() {
        return "chests/" + id;
    }

    public String vaultLootTable() {
        return "chests/" + id + "_vault";
    }

    public static Dungeon byId(String id) {
        for (Dungeon dungeon : values()) {
            if (dungeon.id.equals(id)) {
                return dungeon;
            }
        }
        return null;
    }
}
