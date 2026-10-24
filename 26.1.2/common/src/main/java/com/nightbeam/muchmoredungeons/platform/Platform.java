package com.nightbeam.muchmoredungeons.platform;

import java.nio.file.Path;

/** What common code needs from the loader. Each loader passes an implementation to {@code MuchMoreDungeons.init}. */
public interface Platform {
    Path configDir();
}
