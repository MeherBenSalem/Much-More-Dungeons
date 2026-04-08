package com.nightbeam.muchmoredungeons.world.structure;

import com.nightbeam.muchmoredungeons.Constants;
import net.minecraft.core.Registry;
import net.minecraft.core.registries.BuiltInRegistries;
import net.minecraft.resources.Identifier;
import net.minecraft.world.level.levelgen.structure.StructureType;
import net.minecraft.world.level.levelgen.structure.pieces.StructurePieceType;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

public class StructureRegistration {

    private static final Logger LOGGER = LoggerFactory.getLogger("MuchMoreDungeons/Structure");

    public static final StructureType<TowerDungeonStructure> TOWER_DUNGEON_TYPE =
            Registry.register(
                    BuiltInRegistries.STRUCTURE_TYPE,
                    Identifier.fromNamespaceAndPath(Constants.MOD_ID, "tower_dungeon"),
                    () -> TowerDungeonStructure.CODEC
            );

    public static final StructurePieceType TOWER_DUNGEON_PIECE_TYPE =
            Registry.register(
                    BuiltInRegistries.STRUCTURE_PIECE,
                    Identifier.fromNamespaceAndPath(Constants.MOD_ID, "tower_dungeon_piece"),
                    TowerDungeonPiece::new
            );

    public static final StructureType<Dungeon2Structure> DUNGEON2_TYPE =
            Registry.register(
                    BuiltInRegistries.STRUCTURE_TYPE,
                    Identifier.fromNamespaceAndPath(Constants.MOD_ID, "dungeon_t2"),
                    () -> Dungeon2Structure.CODEC
            );

    public static final StructurePieceType DUNGEON2_PIECE_TYPE =
            Registry.register(
                    BuiltInRegistries.STRUCTURE_PIECE,
                    Identifier.fromNamespaceAndPath(Constants.MOD_ID, "dungeon_t2_piece"),
                    Dungeon2Piece::new
            );

    public static void init() {
        LOGGER.info("Registering structure types for {}", Constants.MOD_ID);
    }
}
