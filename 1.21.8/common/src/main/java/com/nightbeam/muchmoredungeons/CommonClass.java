package com.nightbeam.muchmoredungeons;

import com.nightbeam.muchmoredungeons.platform.Services;
import com.nightbeam.muchmoredungeons.world.structure.StructureRegistration;
import net.minecraft.core.registries.BuiltInRegistries;
import net.minecraft.world.item.Items;

public class CommonClass {

    public static void init() {

        Constants.LOG.info("Hello from Common init on {}! we are currently in a {} environment!", Services.PLATFORM.getPlatformName(), Services.PLATFORM.getEnvironmentName());
        Constants.LOG.info("The ID for diamonds is {}", BuiltInRegistries.ITEM.getKey(Items.DIAMOND));

        // Initialize mod features
        StructureRegistration.init();
        Constants.LOG.info("Much More Dungeons initialized successfully!");

        if (Services.PLATFORM.isModLoaded("muchmoredungeons")) {
            Constants.LOG.info("Much More Dungeons is loaded!");
        }
    }
}
