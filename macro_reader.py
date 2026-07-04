import json
from pathlib import Path


LOG_FILE = Path(__file__).with_name("macro_log.json")


def load_entries() -> list[dict]:
	if not LOG_FILE.exists():
		return []

	try:
		data = json.loads(LOG_FILE.read_text(encoding="utf-8"))
	except json.JSONDecodeError:
		return []

	if isinstance(data, list):
		return data

	return []


def build_entry_map(entries: list[dict]) -> dict[str, dict]:
	entry_map: dict[str, dict] = {}
	for entry in entries:
		first_name = entry.get("first_name")
		if isinstance(first_name, str):
			entry_map[first_name.lower()] = entry
	return entry_map


def search_entry(entry_map: dict[str, dict], key: str) -> dict | None:
	return entry_map.get(key.lower())


def main() -> None:
	entries = load_entries()
	entry_map = build_entry_map(entries)

	print(f"Loaded {len(entry_map)} entries from {LOG_FILE.name}.")

	search_key = input("Enter a first name to search for: ").strip()
	result = search_entry(entry_map, search_key)

	if result is None:
		print("No entry found for that first name.")
		return

	print("Entry found:")
	for key, value in result.items():
		print(f"{key}: {value}")


if __name__ == "__main__":
	main()