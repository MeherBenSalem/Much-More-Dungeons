package com.nightbeam.muchmoredungeons.fabric;

import com.nightbeam.muchmoredungeons.MuchMoreDungeons;
import com.nightbeam.muchmoredungeons.command.DungeonsCommand;
import com.nightbeam.muchmoredungeons.platform.Platform;
import com.nightbeam.muchmoredungeons.platform.Registrar;
import java.nio.file.Path;
import java.util.function.Supplier;
import net.fabricmc.api.ModInitializer;
import net.fabricmc.fabric.api.command.v2.CommandRegistrationCallback;
import net.fabricmc.loader.api.FabricLoader;
import net.minecraft.core.Registry;
import net.minecraft.core.registries.BuiltInRegistries;
import net.minecraft.resources.ResourceKey;

public final class MuchMoreDungeonsFabric implements ModInitializer {
    @Override
    public void onInitialize() {
        MuchMoreDungeons.init(new FabricPlatform(), new FabricRegistrar());
        CommandRegistrationCallback.EVENT.register((dispatcher, context, environment) -> DungeonsCommand.register(dispatcher));
    }

    private static final class FabricRegistrar implements Registrar {
        @Override
        @SuppressWarnings({"unchecked", "rawtypes"})
        public <R, T extends R> Supplier<T> register(ResourceKey<? extends Registry<R>> registry, String path, Supplier<T> factory) {
            Registry<R> target = (Registry<R>) BuiltInRegistries.REGISTRY.getOrThrow((ResourceKey) registry);
            T value = Registry.register(target, MuchMoreDungeons.id(path), factory.get());
            return () -> value;
        }
    }

    private static final class FabricPlatform implements Platform {
        @Override
        public Path configDir() {
            return FabricLoader.getInstance().getConfigDir();
        }
    }
}
