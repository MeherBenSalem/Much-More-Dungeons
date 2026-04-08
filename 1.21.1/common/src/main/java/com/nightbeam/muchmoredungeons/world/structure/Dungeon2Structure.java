package com.nightbeam.muchmoredungeons.world.structure;

import com.mojang.serialization.MapCodec;
import com.mojang.serialization.codecs.RecordCodecBuilder;
import net.minecraft.core.BlockPos;
import net.minecraft.world.level.block.Rotation;
import net.minecraft.world.level.levelgen.Heightmap;
import net.minecraft.world.level.levelgen.structure.Structure;
import net.minecraft.world.level.levelgen.structure.StructureType;

import java.util.Optional;

public class Dungeon2Structure extends Structure {

    public static final MapCodec<Dungeon2Structure> CODEC = RecordCodecBuilder.mapCodec(
            instance -> instance.group(
                    Structure.StructureSettings.CODEC.forGetter(s -> s.settings)
            ).apply(instance, Dungeon2Structure::new)
    );

    private final Structure.StructureSettings settings;

    public Dungeon2Structure(Structure.StructureSettings settings) {
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

            piecesBuilder.addPiece(new Dungeon2Piece(
                    context.structureTemplateManager(), pos, rotation));
        });
    }

    @Override
    public StructureType<?> type() {
        return StructureRegistration.DUNGEON2_TYPE;
    }
}
