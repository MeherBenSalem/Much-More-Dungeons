package com.nightbeam.muchmoredungeons.world.structure;

import com.mojang.serialization.MapCodec;
import com.mojang.serialization.codecs.RecordCodecBuilder;
import net.minecraft.core.BlockPos;
import net.minecraft.world.level.block.Rotation;
import net.minecraft.world.level.levelgen.Heightmap;
import net.minecraft.world.level.levelgen.structure.Structure;
import net.minecraft.world.level.levelgen.structure.StructureType;

import java.util.Optional;

public class TowerDungeonStructure extends Structure {

    public static final MapCodec<TowerDungeonStructure> CODEC = RecordCodecBuilder.mapCodec(
            instance -> instance.group(
                    Structure.StructureSettings.CODEC.forGetter(s -> s.settings)
            ).apply(instance, TowerDungeonStructure::new)
    );

    private final Structure.StructureSettings settings;

    public TowerDungeonStructure(Structure.StructureSettings settings) {
        super(settings);
        this.settings = settings;
    }

    @Override
    public Optional<GenerationStub> findGenerationPoint(GenerationContext context) {
        return onTopOfChunkCenter(context, Heightmap.Types.WORLD_SURFACE_WG, piecesBuilder -> {
            int x = context.chunkPos().getMiddleBlockX();
            int z = context.chunkPos().getMiddleBlockZ();
            int y = context.chunkGenerator().getFirstOccupiedHeight(
                    x, z, Heightmap.Types.WORLD_SURFACE_WG,
                    context.heightAccessor(), context.randomState());

            BlockPos pos = new BlockPos(x, y, z);
            Rotation rotation = Rotation.getRandom(context.random());

            piecesBuilder.addPiece(new TowerDungeonPiece(
                    context.structureTemplateManager(), pos, rotation));
        });
    }

    @Override
    public StructureType<?> type() {
        return StructureRegistration.TOWER_DUNGEON_TYPE;
    }
}
