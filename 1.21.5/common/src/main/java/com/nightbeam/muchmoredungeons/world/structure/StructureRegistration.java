package com.nightbeam.muchmoredungeons.world.structure;

import com.nightbeam.muchmoredungeons.Constants;
import net.minecraft.core.Registry;
import net.minecraft.core.registries.BuiltInRegistries;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.world.level.levelgen.structure.StructureType;
import net.minecraft.world.level.levelgen.structure.pieces.StructurePieceType;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

/**
 * Registers all custom structure types and structure piece types for Much More Dungeons.
 * Must be called during mod initialization BEFORE world generation happens.
 */
public class StructureRegistration {

    private static final Logger LOGGER = LoggerFactory.getLogger("MuchMoreDungeons/Structure");

    // Structure Type — tells Minecraft how to deserialize our custom Structure from JSON
    public static final StructureType<TowerDungeonStructure> TOWER_DUNGEON_TYPE =
            Registry.register(
                    BuiltInRegistries.STRUCTURE_TYPE,
                    ResourceLocation.fromNamespaceAndPath(Constants.MOD_ID, "tower_dungeon"),
                    () -> TowerDungeonStructure.CODEC
            );

    // Structure Piece Type — tells Minecraft how to deserialize our StructurePiece from NBT (saved chunks)
    public static final StructurePieceType TOWER_DUNGEON_PIECE_TYPE =
            Registry.register(
                    BuiltInRegistries.STRUCTURE_PIECE,
                    ResourceLocation.fromNamespaceAndPath(Constants.MOD_ID, "tower_dungeon_piece"),
                    TowerDungeonPiece::new
            );

    public static void init() {
        LOGGER.info("Registering structure types for {}", Constants.MOD_ID);
        // Static fields above are initialized when this class is loaded,
        // which triggers the Registry.register calls.
    }
}
