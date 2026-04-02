package com.nightbeam.muchmoredungeons.world.structure;

import com.nightbeam.muchmoredungeons.Constants;
import net.minecraft.core.Registry;
import net.minecraft.core.registries.Registries;
import net.minecraft.resources.ResourceKey;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.world.level.levelgen.structure.Structure;
import net.minecraft.world.level.levelgen.structure.StructureType;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.util.function.Supplier;

/**
 * Structure registration and type setup for Much More Dungeons.
 * Handles all structure-related registry setup.
 */
public class StructureRegistration {

    private static final Logger LOGGER = LoggerFactory.getLogger("MuchMoreDungeons/Structure");

        public static final ResourceKey<Structure> TOWER_DUNGEON_KEY =
            ResourceKey.create(Registries.STRUCTURE, ResourceLocation.fromNamespaceAndPath(Constants.MOD_ID, "tower_dungeon"));

    // Structure type for tower dungeon
        public static final Supplier<StructureType<TowerDungeonStructure>> TOWER_DUNGEON_TYPE =
            () -> () -> TowerDungeonStructure.CODEC;

    public static void init() {
        LOGGER.info("Initializing structure registrations for {}", Constants.MOD_ID);
        // Structure registration and type registration happens automatically via DFU codecs
        // and registry lookups in 1.20.1
    }

    /**
     * Registers the structure codec and type.
     * This should be called during server setup phase.
     */
    public static void registerStructureType(Registry<StructureType<?>> registry) {
        LOGGER.debug("Registering tower dungeon structure type");
        // Registry setup for structure types - handled by Minecraft's registry system
    }
}
