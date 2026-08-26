package com.nightbeam.muchmoredungeons;

import com.nightbeam.muchmoredungeons.world.structure.Dungeon2Piece;
import com.nightbeam.muchmoredungeons.world.structure.Dungeon2Structure;
import com.nightbeam.muchmoredungeons.world.structure.OutdoorVillaPiece;
import com.nightbeam.muchmoredungeons.world.structure.OutdoorVillaStructure;
import com.nightbeam.muchmoredungeons.world.structure.SoulfireCryptPiece;
import com.nightbeam.muchmoredungeons.world.structure.SoulfireCryptStructure;
import com.nightbeam.muchmoredungeons.world.structure.StructureRegistration;
import com.nightbeam.muchmoredungeons.world.structure.TowerDungeonPiece;
import com.nightbeam.muchmoredungeons.world.structure.TowerDungeonStructure;
import net.minecraft.core.registries.Registries;
import net.minecraft.world.level.levelgen.structure.StructureType;
import net.minecraft.world.level.levelgen.structure.pieces.StructurePieceType;
import net.neoforged.bus.api.IEventBus;
import net.neoforged.fml.common.Mod;
import net.neoforged.fml.event.lifecycle.FMLCommonSetupEvent;
import net.neoforged.neoforge.registries.DeferredHolder;
import net.neoforged.neoforge.registries.DeferredRegister;

@Mod(Constants.MOD_ID)
public class MuchMoreDungeons {

    private static final DeferredRegister<StructureType<?>> STRUCTURE_TYPES =
            DeferredRegister.create(Registries.STRUCTURE_TYPE, Constants.MOD_ID);
    private static final DeferredRegister<StructurePieceType> STRUCTURE_PIECES =
            DeferredRegister.create(Registries.STRUCTURE_PIECE, Constants.MOD_ID);

    private static final DeferredHolder<StructureType<?>, StructureType<TowerDungeonStructure>> TOWER_DUNGEON_TYPE =
            STRUCTURE_TYPES.register("tower_dungeon", () -> () -> TowerDungeonStructure.CODEC);
    private static final DeferredHolder<StructurePieceType, StructurePieceType> TOWER_DUNGEON_PIECE_TYPE =
            STRUCTURE_PIECES.register("tower_dungeon_piece", () -> TowerDungeonPiece::new);
    private static final DeferredHolder<StructureType<?>, StructureType<Dungeon2Structure>> DUNGEON2_TYPE =
            STRUCTURE_TYPES.register("dungeon_t2", () -> () -> Dungeon2Structure.CODEC);
    private static final DeferredHolder<StructurePieceType, StructurePieceType> DUNGEON2_PIECE_TYPE =
            STRUCTURE_PIECES.register("dungeon_t2_piece", () -> Dungeon2Piece::new);
    private static final DeferredHolder<StructureType<?>, StructureType<OutdoorVillaStructure>> OUTDOOR_VILLA_TYPE =
            STRUCTURE_TYPES.register("outdoor_villa", () -> () -> OutdoorVillaStructure.CODEC);
    private static final DeferredHolder<StructurePieceType, StructurePieceType> OUTDOOR_VILLA_PIECE_TYPE =
            STRUCTURE_PIECES.register("outdoor_villa_piece", () -> OutdoorVillaPiece::new);
    private static final DeferredHolder<StructureType<?>, StructureType<SoulfireCryptStructure>> SOULFIRE_CRYPT_TYPE =
            STRUCTURE_TYPES.register("soulfire_crypt", () -> () -> SoulfireCryptStructure.CODEC);
    private static final DeferredHolder<StructurePieceType, StructurePieceType> SOULFIRE_CRYPT_PIECE_TYPE =
            STRUCTURE_PIECES.register("soulfire_crypt_piece", () -> SoulfireCryptPiece::new);

    public MuchMoreDungeons(IEventBus eventBus) {
        STRUCTURE_TYPES.register(eventBus);
        STRUCTURE_PIECES.register(eventBus);
        eventBus.addListener(this::onCommonSetup);
    }

    private void onCommonSetup(FMLCommonSetupEvent event) {
        StructureRegistration.TOWER_DUNGEON_TYPE = TOWER_DUNGEON_TYPE.get();
        StructureRegistration.TOWER_DUNGEON_PIECE_TYPE = TOWER_DUNGEON_PIECE_TYPE.get();
        StructureRegistration.DUNGEON2_TYPE = DUNGEON2_TYPE.get();
        StructureRegistration.DUNGEON2_PIECE_TYPE = DUNGEON2_PIECE_TYPE.get();
        StructureRegistration.OUTDOOR_VILLA_TYPE = OUTDOOR_VILLA_TYPE.get();
        StructureRegistration.OUTDOOR_VILLA_PIECE_TYPE = OUTDOOR_VILLA_PIECE_TYPE.get();
        StructureRegistration.SOULFIRE_CRYPT_TYPE = SOULFIRE_CRYPT_TYPE.get();
        StructureRegistration.SOULFIRE_CRYPT_PIECE_TYPE = SOULFIRE_CRYPT_PIECE_TYPE.get();
        CommonClass.init();
    }
}
