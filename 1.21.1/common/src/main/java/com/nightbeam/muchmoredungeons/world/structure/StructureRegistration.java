package com.nightbeam.muchmoredungeons.world.structure;

import com.nightbeam.muchmoredungeons.Constants;
import net.minecraft.core.Registry;
import net.minecraft.core.registries.BuiltInRegistries;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.world.level.levelgen.structure.StructureType;
import net.minecraft.world.level.levelgen.structure.pieces.StructurePieceType;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

public class StructureRegistration {

    private static final Logger LOGGER = LoggerFactory.getLogger("MuchMoreDungeons/Structure");

    public static StructureType<TowerDungeonStructure> TOWER_DUNGEON_TYPE;
    public static StructurePieceType TOWER_DUNGEON_PIECE_TYPE;
    public static StructureType<Dungeon2Structure> DUNGEON2_TYPE;
    public static StructurePieceType DUNGEON2_PIECE_TYPE;
    public static StructureType<OutdoorVillaStructure> OUTDOOR_VILLA_TYPE;
    public static StructurePieceType OUTDOOR_VILLA_PIECE_TYPE;
    public static StructureType<SoulfireCryptStructure> SOULFIRE_CRYPT_TYPE;
    public static StructurePieceType SOULFIRE_CRYPT_PIECE_TYPE;

    /** Called by Fabric where BuiltInRegistries are not frozen during mod init. */
    public static void registerAll() {
        TOWER_DUNGEON_TYPE = Registry.register(
                BuiltInRegistries.STRUCTURE_TYPE,
                ResourceLocation.fromNamespaceAndPath(Constants.MOD_ID, "tower_dungeon"),
                () -> TowerDungeonStructure.CODEC
        );
        TOWER_DUNGEON_PIECE_TYPE = Registry.register(
                BuiltInRegistries.STRUCTURE_PIECE,
                ResourceLocation.fromNamespaceAndPath(Constants.MOD_ID, "tower_dungeon_piece"),
                TowerDungeonPiece::new
        );
        DUNGEON2_TYPE = Registry.register(
                BuiltInRegistries.STRUCTURE_TYPE,
                ResourceLocation.fromNamespaceAndPath(Constants.MOD_ID, "dungeon_t2"),
                () -> Dungeon2Structure.CODEC
        );
        DUNGEON2_PIECE_TYPE = Registry.register(
                BuiltInRegistries.STRUCTURE_PIECE,
                ResourceLocation.fromNamespaceAndPath(Constants.MOD_ID, "dungeon_t2_piece"),
                Dungeon2Piece::new
        );
        OUTDOOR_VILLA_TYPE = Registry.register(
                BuiltInRegistries.STRUCTURE_TYPE,
                ResourceLocation.fromNamespaceAndPath(Constants.MOD_ID, "outdoor_villa"),
                () -> OutdoorVillaStructure.CODEC
        );
        OUTDOOR_VILLA_PIECE_TYPE = Registry.register(
                BuiltInRegistries.STRUCTURE_PIECE,
                ResourceLocation.fromNamespaceAndPath(Constants.MOD_ID, "outdoor_villa_piece"),
                OutdoorVillaPiece::new
        );
        SOULFIRE_CRYPT_TYPE = Registry.register(
                BuiltInRegistries.STRUCTURE_TYPE,
                ResourceLocation.fromNamespaceAndPath(Constants.MOD_ID, "soulfire_crypt"),
                () -> SoulfireCryptStructure.CODEC
        );
        SOULFIRE_CRYPT_PIECE_TYPE = Registry.register(
                BuiltInRegistries.STRUCTURE_PIECE,
                ResourceLocation.fromNamespaceAndPath(Constants.MOD_ID, "soulfire_crypt_piece"),
                SoulfireCryptPiece::new
        );
        LOGGER.info("Registered structure types for {}", Constants.MOD_ID);
    }

    public static void init() {
        // Registration is handled by each loader's entry point.
    }
}
