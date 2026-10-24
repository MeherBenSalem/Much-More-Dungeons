package com.nightbeam.muchmoredungeons.forge;

import com.nightbeam.muchmoredungeons.MuchMoreDungeons;
import com.nightbeam.muchmoredungeons.command.DungeonsCommand;
import com.nightbeam.muchmoredungeons.platform.Registrar;
import java.util.HashMap;
import java.util.Map;
import java.util.function.Supplier;
import net.minecraft.core.Registry;
import net.minecraft.resources.ResourceKey;
import net.minecraftforge.common.MinecraftForge;
import net.minecraftforge.event.RegisterCommandsEvent;
import net.minecraftforge.eventbus.api.IEventBus;
import net.minecraftforge.fml.common.Mod;
import net.minecraftforge.fml.javafmlmod.FMLJavaModLoadingContext;
import net.minecraftforge.fml.loading.FMLPaths;
import net.minecraftforge.registries.DeferredRegister;

/** The Forge 47 entry point. */
@Mod(MuchMoreDungeons.MOD_ID)
public final class MuchMoreDungeonsForge {
    private final Map<ResourceKey<?>, DeferredRegister<?>> registers = new HashMap<>();

    public MuchMoreDungeonsForge() {
        IEventBus modBus = FMLJavaModLoadingContext.get().getModEventBus();
        MuchMoreDungeons.init(FMLPaths.CONFIGDIR::get, new Registrar() {
            @Override
            public <R, T extends R> Supplier<T> register(ResourceKey<? extends Registry<R>> registry, String path, Supplier<T> factory) {
                return deferred(registry).register(path, factory);
            }
        });
        registers.values().forEach(deferred -> deferred.register(modBus));
        MinecraftForge.EVENT_BUS.addListener((RegisterCommandsEvent event) -> DungeonsCommand.register(event.getDispatcher()));
    }

    @SuppressWarnings("unchecked")
    private <R> DeferredRegister<R> deferred(ResourceKey<? extends Registry<R>> registry) {
        return (DeferredRegister<R>) registers.computeIfAbsent(registry,
                key -> DeferredRegister.create((ResourceKey<? extends Registry<R>>) key, MuchMoreDungeons.MOD_ID));
    }
}
