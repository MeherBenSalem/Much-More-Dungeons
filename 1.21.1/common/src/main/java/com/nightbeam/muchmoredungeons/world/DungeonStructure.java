package com.nightbeam.muchmoredungeons.world;

import com.mojang.serialization.MapCodec;
import com.nightbeam.muchmoredungeons.MuchMoreDungeons;
import com.nightbeam.muchmoredungeons.config.DungeonsConfig;
import com.nightbeam.muchmoredungeons.dungeon.Dungeon;
import com.nightbeam.muchmoredungeons.dungeon.Placement;
import java.util.Optional;
import java.util.OptionalInt;
import net.minecraft.core.BlockPos;
import net.minecraft.world.level.ChunkPos;
import net.minecraft.world.level.block.Rotation;
import net.minecraft.world.level.levelgen.Heightmap;
import net.minecraft.world.level.levelgen.structure.BoundingBox;
import net.minecraft.world.level.levelgen.structure.Structure;
import net.minecraft.world.level.levelgen.structure.StructureType;
import net.minecraft.world.level.levelgen.structure.templatesystem.StructurePlaceSettings;
import net.minecraft.world.level.levelgen.structure.templatesystem.StructureTemplate;

/**
 * A dungeon built from one template, centred on its chunk and placed only on reasonably flat, dry ground. Biomes,
 * spacing and spawn overrides come from the structure and structure set JSON files.
 */
public class DungeonStructure extends Structure {
    private static final int SAMPLES = 4;

    private final Dungeon dungeon;

    public DungeonStructure(StructureSettings settings, Dungeon dungeon) {
        super(settings);
        this.dungeon = dungeon;
    }

    public static MapCodec<DungeonStructure> codec(Dungeon dungeon) {
        return simpleCodec(settings -> new DungeonStructure(settings, dungeon));
    }

    @Override
    public Optional<GenerationStub> findGenerationPoint(GenerationContext context) {
        DungeonsConfig.Settings config = DungeonsConfig.get().of(dungeon);
        if (!config.enabled() || !Placement.passes(context.random().nextDouble(), config.chance())) {
            return Optional.empty();
        }
        Rotation rotation = Rotation.getRandom(context.random());
        StructureTemplate template = context.structureTemplateManager().getOrCreate(MuchMoreDungeons.id(dungeon.id()));
        BoundingBox local = template.getBoundingBox(new StructurePlaceSettings().setRotation(rotation), BlockPos.ZERO);
        ChunkPos chunk = context.chunkPos();
        int originX = chunk.getMiddleBlockX() - (local.minX() + local.maxX()) / 2;
        int originZ = chunk.getMiddleBlockZ() - (local.minZ() + local.maxZ()) / 2;
        int x1 = originX + local.minX();
        int x2 = originX + local.maxX();
        int z1 = originZ + local.minZ();
        int z2 = originZ + local.maxZ();
        // A 4 x 4 grid over the footprint, corners included, catches ponds and ledges a few samples would miss.
        int[] surface = new int[SAMPLES * SAMPLES];
        int[] ground = new int[SAMPLES * SAMPLES];
        for (int i = 0; i < SAMPLES; i++) {
            for (int j = 0; j < SAMPLES; j++) {
                int[] column = {x1 + (x2 - x1) * i / (SAMPLES - 1), z1 + (z2 - z1) * j / (SAMPLES - 1)};
                surface[i * SAMPLES + j] = height(context, column, Heightmap.Types.WORLD_SURFACE_WG);
                ground[i * SAMPLES + j] = height(context, column, Heightmap.Types.OCEAN_FLOOR_WG);
            }
        }
        // Terrain adaptation carves the ground around the dungeon down to its floor; below sea level that floods.
        int minY = Math.max(context.chunkGenerator().getSeaLevel(), context.heightAccessor().getMinBuildHeight() + 8);
        OptionalInt y = Placement.baseY(surface, ground, dungeon.maxSlope(), dungeon.yOffset(), minY);
        if (y.isEmpty()) {
            return Optional.empty();
        }
        BlockPos origin = new BlockPos(originX, y.getAsInt(), originZ);
        BlockPos centre = new BlockPos(chunk.getMiddleBlockX(), y.getAsInt(), chunk.getMiddleBlockZ());
        return Optional.of(new GenerationStub(centre, pieces -> pieces.addPiece(
                new DungeonPiece(dungeon, context.structureTemplateManager(), origin, rotation))));
    }

    private static int height(GenerationContext context, int[] column, Heightmap.Types heightmap) {
        return context.chunkGenerator().getFirstOccupiedHeight(column[0], column[1], heightmap,
                context.heightAccessor(), context.randomState());
    }

    @Override
    public StructureType<?> type() {
        return Structures.type(dungeon);
    }
}
