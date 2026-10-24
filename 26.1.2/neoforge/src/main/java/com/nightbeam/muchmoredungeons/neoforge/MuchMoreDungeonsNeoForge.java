package com.nightbeam.muchmoredungeons.neoforge;

import com.nightbeam.muchmoredungeons.MuchMoreDungeons;
import com.nightbeam.muchmoredungeons.command.DungeonsCommand;
import com.nightbeam.muchmoredungeons.platform.Registrar;
import com.nightbeam.muchmoredungeons.world.Guardians;
import java.nio.file.Path;
import java.util.HashMap;
import java.util.Map;
import java.util.function.Supplier;
import net.minecraft.core.Registry;
import net.minecraft.resources.ResourceKey;
import net.neoforged.bus.api.IEventBus;
import net.neoforged.fml.common.Mod;
import net.neoforged.fml.loading.FMLPaths;
import net.neoforged.neoforge.common.NeoForge;
import net.neoforged.neoforge.event.RegisterCommandsEvent;
import net.neoforged.neoforge.event.entity.EntityJoinLevelEvent;
import net.neoforged.neoforge.registries.DeferredRegister;

@Mod(MuchMoreDungeons.MOD_ID)
public final class MuchMoreDungeonsNeoForge {
    private final Map<ResourceKey<?>, DeferredRegister<?>> registers = new HashMap<>();

    public MuchMoreDungeonsNeoForge(IEventBus modBus) {
        MuchMoreDungeons.init(FMLPaths.CONFIGDIR::get, new Registrar() {
            @Override
            public <R, T extends R> Supplier<T> register(ResourceKey<? extends Registry<R>> registry, String path, Supplier<T> factory) {
                return deferred(registry).register(path, factory);
            }
        });
        registers.values().forEach(deferred -> deferred.register(modBus));
        NeoForge.EVENT_BUS.addListener((RegisterCommandsEvent event) -> DungeonsCommand.register(event.getDispatcher()));
        NeoForge.EVENT_BUS.addListener((EntityJoinLevelEvent event) -> {
            if (!event.getLevel().isClientSide()) {
                Guardians.restoreWeapon(event.getEntity());
            }
        });
    }

    @SuppressWarnings("unchecked")
    private <R> DeferredRegister<R> deferred(ResourceKey<? extends Registry<R>> registry) {
        return (DeferredRegister<R>) registers.computeIfAbsent(registry,
                key -> DeferredRegister.create((ResourceKey<? extends Registry<R>>) key, MuchMoreDungeons.MOD_ID));
    }
}
