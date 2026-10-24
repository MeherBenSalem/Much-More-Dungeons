package com.nightbeam.muchmoredungeons.world;

import com.nightbeam.muchmoredungeons.MuchMoreDungeons;
import com.nightbeam.muchmoredungeons.config.DungeonsConfig;
import com.nightbeam.muchmoredungeons.dungeon.Dungeon;
import net.minecraft.core.BlockPos;
import net.minecraft.core.registries.Registries;
import net.minecraft.nbt.CompoundTag;
import net.minecraft.resources.ResourceKey;
import net.minecraft.util.RandomSource;
import net.minecraft.world.level.ServerLevelAccessor;
import net.minecraft.world.level.block.Block;
import net.minecraft.world.level.block.Blocks;
import net.minecraft.world.level.block.Mirror;
import net.minecraft.world.level.block.Rotation;
import net.minecraft.world.level.block.entity.RandomizableContainerBlockEntity;
import net.minecraft.world.level.levelgen.structure.BoundingBox;
import net.minecraft.world.level.levelgen.structure.TemplateStructurePiece;
import net.minecraft.world.level.levelgen.structure.pieces.StructurePieceSerializationContext;
import net.minecraft.world.level.levelgen.structure.templatesystem.BlockIgnoreProcessor;
import net.minecraft.world.level.levelgen.structure.templatesystem.StructurePlaceSettings;
import net.minecraft.world.level.levelgen.structure.templatesystem.StructureTemplateManager;
import net.minecraft.world.level.storage.loot.LootTable;

/**
 * The placed template. Chests and spawners carry their loot tables and mobs in the template itself; data markers
 * ({@code chest}, {@code vault}, {@code guardian}) are resolved here.
 */
public class DungeonPiece extends TemplateStructurePiece {
    private final Dungeon dungeon;

    public DungeonPiece(Dungeon dungeon, StructureTemplateManager templates, BlockPos origin, Rotation rotation) {
        super(Structures.piece(dungeon), 0, templates, MuchMoreDungeons.id(dungeon.id()),
                MuchMoreDungeons.id(dungeon.id()).toString(), settings(rotation), origin);
        this.dungeon = dungeon;
    }

    public DungeonPiece(Dungeon dungeon, StructurePieceSerializationContext context, CompoundTag tag) {
        super(Structures.piece(dungeon), tag, context.structureTemplateManager(),
                id -> settings(Rotation.valueOf(tag.getString("Rot"))));
        this.dungeon = dungeon;
    }

    private static StructurePlaceSettings settings(Rotation rotation) {
        return new StructurePlaceSettings()
                .setRotation(rotation)
                .setMirror(Mirror.NONE)
                .addProcessor(BlockIgnoreProcessor.STRUCTURE_BLOCK);
    }

    @Override
    protected void addAdditionalSaveData(StructurePieceSerializationContext context, CompoundTag tag) {
        super.addAdditionalSaveData(context, tag);
        tag.putString("Rot", placeSettings.getRotation().name());
    }

    @Override
    protected void handleDataMarker(String marker, BlockPos pos, ServerLevelAccessor level, RandomSource random,
                                    BoundingBox box) {
        switch (marker) {
            case "chest" -> chest(level, pos, random, dungeon.lootTable());
            case "vault" -> chest(level, pos, random, dungeon.vaultLootTable());
            case "guardian" -> {
                level.setBlock(pos, Blocks.AIR.defaultBlockState(), Block.UPDATE_CLIENTS);
                if (DungeonsConfig.get().guardians()) {
                    Guardians.spawn(dungeon, level, pos, random);
                }
            }
            default -> level.setBlock(pos, Blocks.AIR.defaultBlockState(), Block.UPDATE_CLIENTS);
        }
    }

    private static void chest(ServerLevelAccessor level, BlockPos pos, RandomSource random, String table) {
        level.setBlock(pos, Blocks.CHEST.defaultBlockState(), Block.UPDATE_CLIENTS);
        if (level.getBlockEntity(pos) instanceof RandomizableContainerBlockEntity chest) {
            chest.setLootTable(ResourceKey.create(Registries.LOOT_TABLE, MuchMoreDungeons.id(table)), random.nextLong());
        }
    }
}
