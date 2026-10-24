package com.nightbeam.muchmoredungeons.world;

import com.nightbeam.muchmoredungeons.MuchMoreDungeons;
import com.nightbeam.muchmoredungeons.dungeon.Dungeon;
import com.nightbeam.muchmoredungeons.dungeon.Guardian;
import net.minecraft.core.BlockPos;
import net.minecraft.core.registries.BuiltInRegistries;
import net.minecraft.network.chat.Component;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.util.RandomSource;
import net.minecraft.world.entity.Entity;
import net.minecraft.world.entity.EquipmentSlot;
import net.minecraft.world.entity.Mob;
import net.minecraft.world.entity.ai.attributes.Attribute;
import net.minecraft.world.entity.ai.attributes.AttributeInstance;
import net.minecraft.world.entity.ai.attributes.Attributes;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.level.ServerLevelAccessor;

/** Spawns a dungeon's guardian: named, persistent, tougher than its kind, and tagged for the advancements. */
public final class Guardians {
    public static final String TAG = MuchMoreDungeons.MOD_ID + ".guardian";

    private Guardians() {
    }

    public static void spawn(Dungeon dungeon, ServerLevelAccessor level, BlockPos pos, RandomSource random) {
        Guardian spec = dungeon.guardian();
        Entity entity = BuiltInRegistries.ENTITY_TYPE.get(new ResourceLocation(spec.entity())).create(level.getLevel());
        if (!(entity instanceof Mob mob)) {
            MuchMoreDungeons.LOG.warn("Guardian {} of {} is not a mob", spec.entity(), dungeon.id());
            return;
        }
        mob.moveTo(pos.getX() + 0.5, pos.getY(), pos.getZ() + 0.5, random.nextFloat() * 360.0F, 0.0F);
        mob.setCustomName(Component.literal(spec.name()));
        mob.setCustomNameVisible(true);
        mob.setPersistenceRequired();
        mob.addTag(TAG);
        mob.addTag(TAG + "." + dungeon.id());
        base(mob, Attributes.MAX_HEALTH, spec.health());
        base(mob, Attributes.ARMOR, spec.armor());
        base(mob, Attributes.ATTACK_DAMAGE, spec.attack());
        base(mob, Attributes.KNOCKBACK_RESISTANCE, 0.5);
        mob.setHealth(spec.health());
        equip(mob, EquipmentSlot.MAINHAND, spec.mainhand(), 2.0F);
        equip(mob, EquipmentSlot.HEAD, spec.head(), 0.0F);
        equip(mob, EquipmentSlot.CHEST, spec.chest(), 0.0F);
        level.addFreshEntityWithPassengers(mob);
    }

    private static void base(Mob mob, Attribute attribute, double value) {
        AttributeInstance instance = mob.getAttribute(attribute);
        if (instance != null) {
            instance.setBaseValue(value);
        }
    }

    private static void equip(Mob mob, EquipmentSlot slot, String item, float dropChance) {
        if (item.isEmpty()) {
            return;
        }
        mob.setItemSlot(slot, new ItemStack(BuiltInRegistries.ITEM.get(new ResourceLocation(item))));
        mob.setDropChance(slot, dropChance);
    }
}
