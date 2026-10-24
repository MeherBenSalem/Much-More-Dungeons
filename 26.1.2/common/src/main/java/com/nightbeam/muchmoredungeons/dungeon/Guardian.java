package com.nightbeam.muchmoredungeons.dungeon;

/**
 * The named mini-boss a dungeon spawns once, at its {@code guardian} marker, when the dungeon generates.
 *
 * @param entity     entity type id, e.g. {@code minecraft:wither_skeleton}
 * @param name       the name shown above its head
 * @param health     max health (20 = a zombie)
 * @param armor      armor points
 * @param attack     attack damage
 * @param mainhand   item id held in the main hand; it always drops on death
 * @param head       item id worn on the head (keeps undead guardians from burning in daylight), or empty
 * @param chest      item id worn on the chest, or empty
 */
public record Guardian(String entity, String name, float health, double armor, double attack,
                       String mainhand, String head, String chest) {
}
