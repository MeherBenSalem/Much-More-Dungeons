package com.nightbeam.muchmoredungeons.world;

import com.mojang.serialization.Codec;
import com.nightbeam.muchmoredungeons.dungeon.Dungeon;
import com.nightbeam.muchmoredungeons.platform.Registrar;
import java.util.EnumMap;
import java.util.Map;
import java.util.function.Supplier;
import net.minecraft.core.registries.Registries;
import net.minecraft.world.level.levelgen.structure.StructureType;
import net.minecraft.world.level.levelgen.structure.pieces.StructurePieceType;

/** One structure type and one piece type per dungeon, under the ids the mod has always used. */
public final class Structures {
    private static final Map<Dungeon, Supplier<StructureType<DungeonStructure>>> TYPES = new EnumMap<>(Dungeon.class);
    private static final Map<Dungeon, Supplier<StructurePieceType>> PIECES = new EnumMap<>(Dungeon.class);

    private Structures() {
    }

    public static void register(Registrar registrar) {
        for (Dungeon dungeon : Dungeon.values()) {
            Codec<DungeonStructure> codec = DungeonStructure.codec(dungeon);
            StructureType<DungeonStructure> type = () -> codec;
            StructurePieceType piece = (context, tag) -> new DungeonPiece(dungeon, context, tag);
            TYPES.put(dungeon, registrar.register(Registries.STRUCTURE_TYPE, dungeon.id(), () -> type));
            PIECES.put(dungeon, registrar.register(Registries.STRUCTURE_PIECE, dungeon.pieceId(), () -> piece));
        }
    }

    public static StructureType<DungeonStructure> type(Dungeon dungeon) {
        return TYPES.get(dungeon).get();
    }

    public static StructurePieceType piece(Dungeon dungeon) {
        return PIECES.get(dungeon).get();
    }
}
