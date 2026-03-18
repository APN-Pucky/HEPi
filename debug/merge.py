#!/usr/bin/env python
import argparse
import json
import sys
from contextlib import ExitStack

from hepi.load import load_json_with_metadata


def _normalize_parameters(parameters):
    return tuple(tuple(group) for group in parameters)


def _top_level_sorted_data(data):
    def sort_key(item):
        key = item[0]
        try:
            return (0, float(key))
        except (TypeError, ValueError):
            return (1, str(key))

    return {key: value for key, value in sorted(data.items(), key=sort_key)}


def _merge_data_blocks(target, source):
    for key, value in source.items():
        if (
            key in target
            and isinstance(target[key], dict)
            and isinstance(value, dict)
        ):
            _merge_data_blocks(target[key], value)
        else:
            target[key] = value
    return target


def merge_json_objects(files):
    merged_object = None
    reference_parameters = None

    for file in files:
        data_object = json.load(file)
        file.seek(0)

        _, parameters, _ = load_json_with_metadata(file)
        normalized_parameters = _normalize_parameters(parameters)

        if merged_object is None:
            merged_object = data_object
            reference_parameters = normalized_parameters
            continue

        if normalized_parameters != reference_parameters:
            raise ValueError(
                f"Incompatible parameter structure: expected {reference_parameters}, got {normalized_parameters}"
            )

        _merge_data_blocks(merged_object["data"], data_object["data"])

    if merged_object is None:
        raise ValueError("No input files provided.")

    merged_object["data"] = _top_level_sorted_data(merged_object["data"])
    return merged_object


def build_parser():
    parser = argparse.ArgumentParser(
        description="Load multiple xsec JSON files, keep metadata from the first file, merge only the data block, and print the result to stdout."
    )
    parser.add_argument("json", nargs="+", help="Input JSON files to merge.")
    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()

    try:
        with ExitStack() as stack:
            files = [stack.enter_context(open(path)) for path in args.json]
            merged = merge_json_objects(files)
        json.dump(merged, sys.stdout, indent=4)
        sys.stdout.write("\n")
    except Exception as exc:
        parser.exit(1, f"{exc}\n")


if __name__ == "__main__":
    main()
