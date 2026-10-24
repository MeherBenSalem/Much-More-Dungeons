package com.nightbeam.muchmoredungeons.platform;

import java.util.function.Supplier;
import net.minecraft.core.Registry;
import net.minecraft.resources.ResourceKey;

/**
 * Registers content the loader's way: Fabric registers immediately, (Neo)Forge through deferred registers. The
 * returned supplier is only valid once the registry has been populated.
 */
public interface Registrar {
    <R, T extends R> Supplier<T> register(ResourceKey<? extends Registry<R>> registry, String path, Supplier<T> factory);
}
