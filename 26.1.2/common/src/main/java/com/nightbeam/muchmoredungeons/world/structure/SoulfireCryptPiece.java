package com.nightbeam.muchmoredungeons.world.structure;

import com.nightbeam.muchmoredungeons.Constants;
import net.minecraft.core.BlockPos;
import net.minecraft.core.registries.Registries;
import net.minecraft.nbt.CompoundTag;
import net.minecraft.network.chat.Component;
import net.minecraft.resources.Identifier;
import net.minecraft.resources.ResourceKey;
import net.minecraft.util.RandomSource;
import net.minecraft.world.entity.EntityType;
import net.minecraft.world.entity.EquipmentSlot;
import net.minecraft.world.entity.monster.WitherSkeleton;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.Items;
import net.minecraft.world.level.ServerLevelAccessor;
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
import net.minecraft.world.phys.AABB;

public class SoulfireCryptPiece extends TemplateStructurePiece {

    private static final Identifier TEMPLATE =
            Identifier.fromNamespaceAndPath(Constants.MOD_ID, "soulfire_crypt");
    private static final ResourceKey<LootTable> LOOT = ResourceKey.create(
            Registries.LOOT_TABLE,
            Identifier.fromNamespaceAndPath(Constants.MOD_ID, "chests/soulfire_crypt"));

    public SoulfireCryptPiece(StructureTemplateManager templateManager, BlockPos pos, Rotation rotation) {
        super(StructureRegistration.SOULFIRE_CRYPT_PIECE_TYPE, 0,
                templateManager, TEMPLATE, TEMPLATE.toString(),
                createPlacementSettings(rotation), pos);
    }

    public SoulfireCryptPiece(StructurePieceSerializationContext context, CompoundTag tag) {
        super(StructureRegistration.SOULFIRE_CRYPT_PIECE_TYPE, tag,
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
        if ("chest".equals(marker)) {
            level.setBlock(pos, Blocks.CHEST.defaultBlockState(), 2);
            if (level.getBlockEntity(pos) instanceof RandomizableContainerBlockEntity container) {
                container.setLootTable(LOOT, random.nextLong());
            }
        } else if ("guardian".equals(marker)) {
            level.setBlock(pos, Blocks.AIR.defaultBlockState(), 3);
            if (level.getEntitiesOfClass(WitherSkeleton.class, new AABB(pos).inflate(2.0)).isEmpty()) {
                WitherSkeleton warden = EntityType.WITHER_SKELETON.create(level.getLevel());
                if (warden != null) {
                    warden.moveTo(pos.getX() + 0.5, pos.getY(), pos.getZ() + 0.5, random.nextFloat() * 360f, 0f);
                    warden.setCustomName(Component.literal("Cinder Warden"));
                    warden.setCustomNameVisible(true);
                    warden.setPersistenceRequired();
                    warden.setItemSlot(EquipmentSlot.MAINHAND, new ItemStack(Items.STONE_SWORD));
                    warden.setItemSlot(EquipmentSlot.CHEST, new ItemStack(Items.CHAINMAIL_CHESTPLATE));
                    level.addFreshEntity(warden);
                }
            }
        }
    }
}
