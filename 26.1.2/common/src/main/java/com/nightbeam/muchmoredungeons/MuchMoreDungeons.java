package com.nightbeam.muchmoredungeons;

import com.nightbeam.muchmoredungeons.config.DungeonsConfig;
import com.nightbeam.muchmoredungeons.platform.Platform;
import com.nightbeam.muchmoredungeons.platform.Registrar;
import com.nightbeam.muchmoredungeons.world.Structures;
import net.minecraft.resources.Identifier;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

public final class MuchMoreDungeons {
    public static final String MOD_ID = "muchmoredungeons";
    public static final String MOD_NAME = "Much More Dungeons";
    public static final Logger LOG = LoggerFactory.getLogger(MOD_NAME);

    private static boolean initialized;

    private MuchMoreDungeons() {
    }

    /** Called once by each loader's entry point, before registries freeze. */
    public static void init(Platform platform, Registrar registrar) {
        if (initialized) {
            return;
        }
        initialized = true;
        DungeonsConfig.load(platform.configDir());
        Structures.register(registrar);
    }

    public static Identifier id(String path) {
        return Identifier.fromNamespaceAndPath(MOD_ID, path);
    }
}
