package com.nightbeam.muchmoredungeons.command;

import com.mojang.brigadier.CommandDispatcher;
import com.mojang.brigadier.context.CommandContext;
import com.mojang.brigadier.exceptions.CommandSyntaxException;
import com.nightbeam.muchmoredungeons.MuchMoreDungeons;
import com.nightbeam.muchmoredungeons.world.Guardians;
import java.util.Map;
import java.util.TreeMap;
import net.minecraft.commands.CommandSourceStack;
import net.minecraft.commands.Commands;
import net.minecraft.commands.arguments.coordinates.BlockPosArgument;
import net.minecraft.core.BlockPos;
import net.minecraft.core.registries.BuiltInRegistries;
import net.minecraft.core.registries.Registries;
import net.minecraft.network.chat.Component;
import net.minecraft.resources.ResourceKey;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.world.entity.Entity;
import net.minecraft.world.entity.Mob;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.Items;
import net.minecraft.world.level.block.entity.BlockEntity;
import net.minecraft.world.level.block.entity.RandomizableContainerBlockEntity;
import net.minecraft.world.level.block.entity.SpawnerBlockEntity;
import net.minecraft.world.level.levelgen.structure.BoundingBox;
import net.minecraft.world.level.levelgen.structure.Structure;
import net.minecraft.world.level.levelgen.structure.StructureStart;
import net.minecraft.world.phys.AABB;

/**
 * {@code /muchmoredungeons inspect [pos] [fill]} and {@code inspect area <from> <to> [fill]} (operators): what a
 * dungeon holds. Lists its loot chests by table, its spawners by mob, its living guardians and where its vault is;
 * {@code fill} rolls the chests' loot first and counts the stacks and treasure maps. Without a position, the
 * executor's column is searched. Meant for modpack makers checking their datapack changes, and for the QA scripts.
 */
public final class DungeonsCommand {
    private DungeonsCommand() {
    }

    public static void register(CommandDispatcher<CommandSourceStack> dispatcher) {
        dispatcher.register(Commands.literal(MuchMoreDungeons.MOD_ID)
                .requires(Commands.hasPermission(Commands.LEVEL_GAMEMASTERS))
                .then(Commands.literal("inspect")
                        .executes(c -> inspect(c, BlockPos.containing(c.getSource().getPosition()), false))
                        .then(Commands.literal("area")
                                .then(Commands.argument("from", BlockPosArgument.blockPos())
                                        .then(Commands.argument("to", BlockPosArgument.blockPos())
                                                .executes(c -> area(c, false))
                                                .then(Commands.literal("fill").executes(c -> area(c, true))))))
                        .then(Commands.argument("pos", BlockPosArgument.blockPos())
                                .executes(c -> inspect(c, BlockPosArgument.getLoadedBlockPos(c, "pos"), false))
                                .then(Commands.literal("fill")
                                        .executes(c -> inspect(c, BlockPosArgument.getLoadedBlockPos(c, "pos"), true))))));
    }

    private static int inspect(CommandContext<CommandSourceStack> context, BlockPos pos, boolean fill) {
        CommandSourceStack source = context.getSource();
        ServerLevel level = source.getLevel();
        // Every structure of the mod at this spot (a labyrinth can lie under a dungeon): the four dungeons, the
        // labyrinths, and any a datapack adds to the namespace. One line each.
        int found = 0;
        for (Map.Entry<ResourceKey<Structure>, Structure> entry : level.registryAccess().lookupOrThrow(Registries.STRUCTURE).entrySet()) {
            if (!entry.getKey().identifier().getNamespace().equals(MuchMoreDungeons.MOD_ID)) {
                continue;
            }
            StructureStart start = startAt(level, pos, entry.getValue());
            if (start == null) {
                continue;
            }
            String id = entry.getKey().identifier().getPath();
            report(source, id, start.getBoundingBox(), Guardians.TAG + "." + id, fill);
            found++;
        }
        if (found > 0) {
            return found;
        }
        source.sendFailure(Component.literal("MMD inspect none: no Much More Dungeons dungeon at " + pos.toShortString()));
        return 0;
    }

    /** Inspects a box regardless of structure data: /place structure places blocks without recording a dungeon. */
    private static int area(CommandContext<CommandSourceStack> context, boolean fill) throws CommandSyntaxException {
        BoundingBox box = BoundingBox.fromCorners(BlockPosArgument.getBlockPos(context, "from"), BlockPosArgument.getBlockPos(context, "to"));
        report(context.getSource(), "area", box, Guardians.TAG, fill);
        return 1;
    }

    private static void report(CommandSourceStack source, String label, BoundingBox box, String guardianTag, boolean fill) {
        ServerLevel level = source.getLevel();
        Map<String, Integer> chests = new TreeMap<>();
        Map<String, Integer> spawners = new TreeMap<>();
        int stacks = 0;
        int maps = 0;
        BlockPos vault = null;
        for (int cx = box.minX() >> 4; cx <= box.maxX() >> 4; cx++) {
            for (int cz = box.minZ() >> 4; cz <= box.maxZ() >> 4; cz++) {
                if (!level.hasChunk(cx, cz)) {
                    continue;
                }
                for (BlockEntity be : level.getChunk(cx, cz).getBlockEntities().values()) {
                    if (!box.isInside(be.getBlockPos())) {
                        continue;
                    }
                    if (be instanceof RandomizableContainerBlockEntity chest) {
                        String table = chest.getLootTable() == null ? "none" : chest.getLootTable().identifier().toString();
                        if (fill) {
                            chest.unpackLootTable(null);
                            for (int i = 0; i < chest.getContainerSize(); i++) {
                                ItemStack stack = chest.getItem(i);
                                stacks += stack.isEmpty() ? 0 : 1;
                                maps += stack.is(Items.FILLED_MAP) ? 1 : 0;
                            }
                        }
                        if (!"none".equals(table)) {
                            chests.merge(table, 1, Integer::sum);
                        }
                        if (table.endsWith("_vault")) {
                            vault = be.getBlockPos();
                        }
                    } else if (be instanceof SpawnerBlockEntity spawner) {
                        Entity shown = spawner.getSpawner().getOrCreateDisplayEntity(level, be.getBlockPos());
                        String mob = shown == null ? "none" : BuiltInRegistries.ENTITY_TYPE.getKey(shown.getType()).toString();
                        if (shown != null && shown.hasCustomName()) {
                            mob += "[" + shown.getCustomName().getString().replace(' ', '_') + "]";
                        }
                        spawners.merge(mob, 1, Integer::sum);
                    }
                }
            }
        }
        int guardians = level.getEntitiesOfClass(Mob.class, AABB.of(box).inflate(8),
                mob -> mob.entityTags().contains(guardianTag)).size();
        String line = String.format("MMD inspect id=%s box=%d,%d,%d,%d,%d,%d chests=%s spawners=%s guardians=%d%s%s",
                label, box.minX(), box.minY(), box.minZ(), box.maxX(), box.maxY(), box.maxZ(),
                join(chests), join(spawners), guardians, fill ? " stacks=" + stacks + " maps=" + maps : "",
                vault == null ? "" : " vault=" + vault.getX() + "," + vault.getY() + "," + vault.getZ());
        source.sendSuccess(() -> Component.literal(line), false);
    }

    /**
     * The dungeon with a piece at {@code pos}, or anywhere in the columns around it (so a /locate result can be
     * inspected: a labyrinth's first piece starts at the chunk's corner, the handcrafted dungeons at its middle).
     */
    private static StructureStart startAt(ServerLevel level, BlockPos pos, Structure structure) {
        StructureStart start = level.structureManager().getStructureWithPieceAt(pos, structure);
        for (int dx = -8; dx <= 8 && !start.isValid(); dx += 4) {
            for (int dz = -8; dz <= 8 && !start.isValid(); dz += 4) {
                int x = pos.getX() + dx;
                int z = pos.getZ() + dz;
                for (int y = level.getMinY(); !start.isValid() && y < level.getMaxY(); y += 4) {
                    start = level.structureManager().getStructureWithPieceAt(new BlockPos(x, y, z), structure);
                }
            }
        }
        return start.isValid() ? start : null;
    }

    private static String join(Map<String, Integer> counts) {
        if (counts.isEmpty()) {
            return "-";
        }
        StringBuilder out = new StringBuilder();
        counts.forEach((key, count) -> out.append(out.isEmpty() ? "" : ",").append(key).append('*').append(count));
        return out.toString();
    }
}
