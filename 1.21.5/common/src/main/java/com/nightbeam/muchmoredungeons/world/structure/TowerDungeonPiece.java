package com.nightbeam.muchmoredungeons.world.structure;

import com.nightbeam.muchmoredungeons.Constants;
import net.minecraft.core.BlockPos;
import net.minecraft.nbt.CompoundTag;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.util.RandomSource;
import net.minecraft.world.level.ServerLevelAccessor;
import net.minecraft.world.level.block.Blocks;
import net.minecraft.world.level.block.Mirror;
import net.minecraft.world.level.block.Rotation;
import net.minecraft.world.level.chunk.ChunkGenerator;
import net.minecraft.world.level.levelgen.structure.BoundingBox;
import net.minecraft.world.level.levelgen.structure.TemplateStructurePiece;
import net.minecraft.world.level.levelgen.structure.pieces.StructurePieceSerializationContext;
import net.minecraft.world.level.levelgen.structure.templatesystem.BlockIgnoreProcessor;
import net.minecraft.world.level.levelgen.structure.templatesystem.StructurePlaceSettings;
import net.minecraft.world.level.levelgen.structure.templatesystem.StructureTemplateManager;

/**
 * Structure piece for the Tower Dungeon.
 * Loads the NBT template and places it in the world.
 */
public class TowerDungeonPiece extends TemplateStructurePiece {

    private static final ResourceLocation TEMPLATE =
            ResourceLocation.fromNamespaceAndPath(Constants.MOD_ID, "tower_dungeon");

    public TowerDungeonPiece(StructureTemplateManager templateManager, BlockPos pos, Rotation rotation) {
        super(StructureRegistration.TOWER_DUNGEON_PIECE_TYPE, 0,
                templateManager, TEMPLATE, TEMPLATE.toString(),
                createPlacementSettings(rotation), pos);
    }

    /**
     * Deserialization constructor — called when loading from NBT (saved chunks).
     */
    public TowerDungeonPiece(StructurePieceSerializationContext context, CompoundTag tag) {
        super(StructureRegistration.TOWER_DUNGEON_PIECE_TYPE, tag,
                context.structureTemplateManager(),
                (id) -> createPlacementSettings(Rotation.valueOf(tag.getString("Rot").orElse("NONE"))));
    }

    private static StructurePlaceSettings createPlacementSettings(Rotation rotation) {
        return new StructurePlaceSettings()
                .setRotation(rotation)
                .setMirror(Mirror.NONE)
                .addProcessor(BlockIgnoreProcessor.STRUCTURE_BLOCK);
    }

    @Override
    protected void addAdditionalSaveData(StructurePieceSerializationContext context, CompoundTag tag) {
        super.addAdditionalSaveData(context, tag);
        tag.putString("Rot", this.placeSettings.getRotation().name());
    }

    @Override
    protected void handleDataMarker(String marker, BlockPos pos, ServerLevelAccessor level,
                                    RandomSource random, BoundingBox box) {
        // Handle any data markers in the structure template (e.g., chest, spawner markers)
        if ("chest".equals(marker)) {
            level.setBlock(pos, Blocks.AIR.defaultBlockState(), 3);
            // Could set up chest loot table here if needed
        }
    }
}
