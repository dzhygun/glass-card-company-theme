#!/usr/bin/env python3
from __future__ import annotations

import copy
import json
import logging
from dataclasses import dataclass
from pathlib import Path

JSONType = dict[str, dict | list] | list[dict[str, dict | list]]
MainConfigType = JSONType
CustomConfigType = list[dict[str, dict | list]]
OrderingDataType = list[str]

LOG_FILE_NAME = "compile_config_json.log"

logger = logging.getLogger("__name__")


def setup_logging() -> None:
    logger.setLevel(logging.INFO)
    formatter = logging.Formatter("%(asctime)s %(levelname)s: %(message)s")
    fh = logging.FileHandler(LOG_FILE_NAME, mode="w")
    fh.setFormatter(formatter)
    ch = logging.StreamHandler()
    ch.setFormatter(formatter)

    logger.addHandler(fh)
    logger.addHandler(ch)


@dataclass
class GroupOrderingDataItem:
    first_item_index: int | None = None
    last_item_index: int | None = None

    @property
    def is_found(self):
        return self.first_item_index is not None and self.last_item_index is not None


class CustomConfigSorter:
    def __init__(self, custom_config: CustomConfigType, ordering_data: OrderingDataType):
        self._custom_config = copy.deepcopy(custom_config)
        self._ordering_data = ordering_data

    def get_sorted_custom_config(self) -> CustomConfigType:
        for group_name_1, group_name_2 in zip(self._ordering_data, self._ordering_data[1:]):
            group_2 = self._pop_group_2(group_name_2=group_name_2)
            self._insert_group_2_after_group_1(group_name_1=group_name_1, group_2=group_2)
        logger.info("Sorted custom config groups: %s", ", ".join(self._ordering_data))
        return self._custom_config

    def _pop_group_2(self, group_name_2: str) -> CustomConfigType:
        group_ordering_data_item_2 = self._collect_group_ordering_data_item(group_name=group_name_2)

        before_group_2 = self._custom_config[:group_ordering_data_item_2.first_item_index]
        group_2 = self._custom_config[
                  group_ordering_data_item_2.first_item_index: group_ordering_data_item_2.last_item_index + 1]
        after_group_2 = self._custom_config[group_ordering_data_item_2.last_item_index + 1:]
        self._custom_config = before_group_2 + after_group_2
        return group_2

    def _insert_group_2_after_group_1(self, group_name_1: str, group_2: CustomConfigType) -> None:
        group_ordering_data_item_1 = self._collect_group_ordering_data_item(group_name=group_name_1)
        before_group_2 = self._custom_config[:group_ordering_data_item_1.last_item_index + 1]
        after_group_2 = self._custom_config[group_ordering_data_item_1.last_item_index + 1:]
        self._custom_config = before_group_2 + group_2 + after_group_2

    def _collect_group_ordering_data_item(self, group_name: str) -> GroupOrderingDataItem:
        group_ordering_data_item = GroupOrderingDataItem()
        for i, data_obj in enumerate(self._custom_config):
            try:
                data_obj_group = data_obj["group"]
            except KeyError:
                logger.error("Malformed custom config object - 'group' key is missing:\n%s",
                             json.dumps(data_obj, indent=4, ensure_ascii=False))
                raise
            if group_ordering_data_item.first_item_index is None and data_obj_group == group_name:
                group_ordering_data_item.first_item_index = i
            if data_obj_group == group_name:
                group_ordering_data_item.last_item_index = i
        if not group_ordering_data_item.is_found:
            raise ValueError(f"Group '{group_name}' is not found in custom config' ")
        return group_ordering_data_item


class JsonMerger:
    _ORDERING_KEYS = ["place_before", "place_after"]

    def __init__(self) -> None:
        self._root_dir = self._get_theme_root()
        self._config_dir = self._root_dir / "config"
        self._custom_config_dir = self._config_dir / "custom"

        self._main_config: MainConfigType = {}
        self._custom_config: CustomConfigType = []

        logger.info("Theme root: %s", self._root_dir)

    def run(self) -> None:
        self._load_main_config()
        self._load_custom_config()
        self._sort_custom_config()
        config = self._get_joined_main_and_custom_config()
        self._replace_config_in_root(config)

    # ---------------- private helpers ----------------

    @staticmethod
    def _get_theme_root() -> Path:
        cwd = Path(__file__).resolve()
        for candidate in [cwd] + list(cwd.parents):
            cfg = candidate / ".publii_theme_root"
            if cfg.is_file():
                return candidate
        raise FileNotFoundError(
            "Unable to locate theme root (expected a '.publii_theme_root' file in some parent)."
        )

    def _load_main_config(self) -> None:
        main_path = self._config_dir / "main.json"
        if not main_path.is_file():
            raise FileNotFoundError(f"Missing main config: {main_path}")
        with main_path.open("r") as fh:
            self._main_config = json.load(fh)
        if not isinstance(self._main_config, dict):
            raise TypeError(
                f"JSON in config/custom_main.json must be an object (dict), got {type(self._main_config).__name__}")
        logger.info("Loaded main config: %s", main_path)

    def _load_custom_config(self) -> None:
        if not self._custom_config_dir.exists():
            logger.info("No custom directory found: %s (skipping)", self._custom_config_dir)
            return

        custom_config_files = sorted(self._custom_config_dir.glob("*.json"))
        if not custom_config_files:
            logger.info("No custom JSON files in: %s", self._custom_config_dir)
            return

        for file in custom_config_files:
            with file.open("r") as fh:
                data: CustomConfigType = json.load(fh)
            if not isinstance(data, list):
                raise TypeError(f"JSON in custom config {file} must be an array (list), got {type(data).__name__}")
            self._custom_config.extend(data)
            logger.info("Loaded custom config: %s", file)

    def _sort_custom_config(self):
        group_order_file = self._custom_config_dir / "group_order" / "order.json"
        if not group_order_file.is_file():
            logger.info("Group order json is not found: %s (skipping)", group_order_file)
            return
        with group_order_file.open("r") as fh:
            ordering_data: OrderingDataType = json.load(fh)
        if len(ordering_data) == 0:
            logger.info("Group order json is empty (skipping)")
            return
        if len(ordering_data) < 2:
            raise ValueError("Group order json must have at least 2 group names")

        self._custom_config = CustomConfigSorter(custom_config=self._custom_config,
                                                 ordering_data=ordering_data).get_sorted_custom_config()

    def _get_joined_main_and_custom_config(self) -> JSONType:
        merged = copy.deepcopy(self._main_config)
        merged["customConfig"] = self._custom_config
        return merged

    def _replace_config_in_root(self, config: JSONType) -> None:
        out_path = self._root_dir / "config.json"
        with out_path.open("w", encoding="utf-8") as fh:
            json.dump(config,
                      fh,  # type: ignore
                      ensure_ascii=True,
                      indent=4,
                      )
            fh.write("\n")
        logger.info("Wrote merged config to: %s", out_path)


if __name__ == "__main__":
    setup_logging()
    JsonMerger().run()
    logger.info("Successfully recompiled config.json and updated in the theme root.")
    print(f"Logs are saved in {LOG_FILE_NAME}")
    try:
        input("Press any key to finish...")
    except KeyboardInterrupt:
        pass
