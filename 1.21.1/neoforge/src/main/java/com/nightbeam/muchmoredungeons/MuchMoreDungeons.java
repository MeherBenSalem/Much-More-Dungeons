package com.nightbeam.muchmoredungeons;

import net.neoforged.bus.api.IEventBus;
import net.neoforged.fml.common.Mod;

@Mod(Constants.MOD_ID)
public class MuchMoreDungeons {

    public MuchMoreDungeons(IEventBus eventBus) {
        CommonClass.init();
    }
}
