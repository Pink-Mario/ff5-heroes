#!/usr/bin/env python3

import json
import sys
from pathlib import Path

SRAM_SIZE = 0x2000
SAVE_SIZE = 0x0600
SAVE_SLOT_OFFSET = 0x0000
CHARACTER_RECORD_SIZE = 0x0050
CHARACTER_LEVEL_OFFSET = 0x0002
CHARACTER_NOT_IN_PARTY = 0x40
AVAILABLE_JOBS_OFFSET = 0x0340
KNOWN_SPELLS_OFFSET = 0x0450
ITEM_IDS_OFFSET = 0x0140
ITEM_QTY_OFFSET = 0x0240
MAP_INDEX_OFFSET = 0x05D6
PLAYER_X_OFFSET = 0x05D8
PLAYER_Y_OFFSET = 0x05D9
PARTY_GRAPHIC_OFFSET = 0x05DA
FACING_OFFSET = 0x05DB
VEHICLE_OFFSET = 0x05DC
AIRSHIP_OFFSET = 0x05F1
NAME_OFFSET = 0x0490
SAVE_CHECKSUM_OFFSET = 0x1FF0
SAVE_SLOT_MARKER_OFFSET = 0x1FF8
WORLD3_MAP_INDEX = 0x02
WORLD3_PLAYER_X = 0x23
WORLD3_AIRSHIP_X = 0x24
WORLD3_PLAYER_Y = 0x20
AIRSHIP_VEHICLE_TYPE = 0x06
DEFAULT_CONFIG = bytes(
    (
        0x2A, 0x00, 0x40, 0x00, 0x00, 0x80, 0x40, 0x20,
        0x10, 0x08, 0x04, 0x04, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x01, 0x02, 0x03, 0x00, 0x01, 0x02, 0x03,
        0x00, 0x01, 0x02, 0x03, 0x00, 0x01, 0x02, 0x03,
    )
)


def create_save(language: str) -> bytearray:
    root = Path(__file__).resolve().parents[1]
    world_map = (root / "src/field/world_tilemap/world_tilemap_2.dat").read_bytes()
    world_tile_props = (
        root / "src/field/world_tile_prop/bartz_world.dat"
    ).read_bytes()
    if len(world_map) != 0x10000:
        raise ValueError("Unexpected World 3 map size")
    for x in (WORLD3_PLAYER_X, WORLD3_AIRSHIP_X):
        tile_id = world_map[WORLD3_PLAYER_Y * 0x100 + x]
        prop_offset = tile_id * 3
        if (
            prop_offset >= len(world_tile_props)
            or not world_tile_props[prop_offset] & 0x01
        ):
            raise ValueError(
                f"World 3 test-save tile ({x:#04x}, "
                f"{WORLD3_PLAYER_Y:#04x}) is not walkable"
            )

    character_data = (root / "src/field/char_prop.dat").read_bytes()
    if len(character_data) != 0x0140:
        raise ValueError("Unexpected character data size")

    item_data = json.loads(
        (root / "src/text/item_name_en.json").read_text(encoding="utf-8")
    )
    item_names = item_data["text"]
    if len(item_names) != 0x0100:
        raise ValueError("Expected 256 item names")

    item_ids = [
        item_id
        for item_id, name in enumerate(item_names)
        if name and item_id not in (0x00, 0x01, 0x80)
    ]
    save = bytearray(SRAM_SIZE)
    record = memoryview(save)[SAVE_SLOT_OFFSET:SAVE_SLOT_OFFSET + SAVE_SIZE]
    record[:len(character_data)] = character_data
    record[ITEM_IDS_OFFSET:ITEM_IDS_OFFSET + len(item_ids)] = bytes(item_ids)
    record[ITEM_QTY_OFFSET:ITEM_QTY_OFFSET + len(item_ids)] = bytes(
        [99] * len(item_ids)
    )
    record[AVAILABLE_JOBS_OFFSET:AVAILABLE_JOBS_OFFSET + 3] = b"\xff\xff\x3f"
    record[KNOWN_SPELLS_OFFSET:KNOWN_SPELLS_OFFSET + 0x20] = b"\xff" * 0x20
    record[0x0470:0x0490] = DEFAULT_CONFIG

    for character_offset in range(0, len(character_data), CHARACTER_RECORD_SIZE):
        record[character_offset] &= ~CHARACTER_NOT_IN_PARTY
        record[character_offset + CHARACTER_LEVEL_OFFSET] = 50
    record[0x00A0] = (record[0x00A0] & 0xF8) | 0x04

    record[MAP_INDEX_OFFSET] = WORLD3_MAP_INDEX
    record[PLAYER_X_OFFSET] = WORLD3_PLAYER_X
    record[PLAYER_Y_OFFSET] = WORLD3_PLAYER_Y
    record[PARTY_GRAPHIC_OFFSET] = 2
    record[FACING_OFFSET] = 3
    record[VEHICLE_OFFSET] = 0

    for offset in range(0x05DD, 0x05DD + 6 * 4, 4):
        record[offset:offset + 2] = b"\x00\x80"
    record[AIRSHIP_OFFSET] = (
        (WORLD3_MAP_INDEX << 5) | (AIRSHIP_VEHICLE_TYPE << 2)
    )
    record[AIRSHIP_OFFSET + 1] = 0
    record[AIRSHIP_OFFSET + 2] = WORLD3_AIRSHIP_X
    record[AIRSHIP_OFFSET + 3] = WORLD3_PLAYER_Y

    if language == "jp":
        names = (root / "src/text/char_name_jp.dat").read_bytes()
        if len(names) != 30:
            raise ValueError("Unexpected Japanese character name data size")
        record[NAME_OFFSET:NAME_OFFSET + 36] = names + b"\xFF" * 6
    elif language == "en":
        names = ("Bartz", "Lenna", "Galuf", "Faris", "Krile", "")
        for index, name in enumerate(names):
            encoded = bytes(
                0x60 + ord(char.upper()) - ord("A")
                if char.isupper()
                else 0x7A + ord(char) - ord("a")
                for char in name
            )
            start = NAME_OFFSET + index * 6
            record[start:start + 6] = encoded + b"\xFF" * (6 - len(encoded))
    else:
        raise ValueError(f"Unknown language: {language}")

    checksum = 0
    carry = 0
    for index in range(0, SAVE_SIZE, 2):
        total = checksum + int.from_bytes(record[index:index + 2], "little") + carry
        checksum = total & 0xFFFF
        carry = total >> 16
    save[SAVE_CHECKSUM_OFFSET:SAVE_CHECKSUM_OFFSET + 2] = checksum.to_bytes(
        2, "little"
    )
    save[SAVE_SLOT_MARKER_OFFSET:SAVE_SLOT_MARKER_OFFSET + 2] = b"\x1B\xE4"
    return save


def main() -> None:
    if len(sys.argv) != 3:
        raise SystemExit("Usage: create_test_save.py <en|jp> <output.srm>")
    language, output = sys.argv[1:]
    output_path = Path(output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_bytes(create_save(language))


if __name__ == "__main__":
    main()
