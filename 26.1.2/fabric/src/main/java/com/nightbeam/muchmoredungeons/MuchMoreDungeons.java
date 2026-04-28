package com.nightbeam.muchmoredungeons;

import com.nightbeam.muchmoredungeons.world.structure.StructureRegistration;
import net.fabricmc.api.ModInitializer;

public class MuchMoreDungeons implements ModInitializer {

    @Override
    public void onInitialize() {
        StructureRegistration.registerAll();
        CommonClass.init();
    }
}
