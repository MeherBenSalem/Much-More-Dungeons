package com.nightbeam.muchmoredungeons.world.structure;

import com.mojang.serialization.Codec;
import com.mojang.serialization.codecs.RecordCodecBuilder;
import net.minecraft.world.level.levelgen.Heightmap;
import net.minecraft.world.level.levelgen.structure.Structure;
import net.minecraft.world.level.levelgen.structure.StructureType;
import net.minecraft.world.level.levelgen.structure.pieces.StructurePiecesBuilder;

import java.util.Optional;

/**
 * Structure for the Tower Dungeon.
 * Uses NBT template structures for generation.
 */
public class TowerDungeonStructure extends Structure {

    static final byte PALETTE_ID = 0;

    private final Structure.StructureSettings towerSettings;

    public static final Codec<TowerDungeonStructure> CODEC = RecordCodecBuilder.<TowerDungeonStructure>mapCodec(
        instance -> instance.group(
            Structure.StructureSettings.CODEC.forGetter((TowerDungeonStructure s) -> s.towerSettings)
        ).apply(instance, TowerDungeonStructure::new)
    ).codec();

    public TowerDungeonStructure(Structure.StructureSettings settings) {
        super(settings);
        this.towerSettings = settings;
    }

    @Override
    public Optional<GenerationStub> findGenerationPoint(GenerationContext context) {
        return onTopOfChunkCenter(context, Heightmap.Types.WORLD_SURFACE_WG, piecesBuilder -> {
            // Structure pieces are added here during world generation
        });
    }

    @Override
    public StructureType<?> type() {
        return StructureRegistration.TOWER_DUNGEON_TYPE.get();
    }
}
