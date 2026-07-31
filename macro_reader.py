import json
from pathlib import Path


LOG_FILE = Path(__file__).with_name("macro_log.json")


class MacroReaderApp:
	def __init__(self, log_file: Path | None = None) -> None:
		self.log_file = log_file or LOG_FILE

	def load_entries(self) -> list[dict]:
		if not self.log_file.exists():
			return []

		try:
			data = json.loads(self.log_file.read_text(encoding="utf-8"))
		except json.JSONDecodeError:
			return []

		if isinstance(data, list):
			return data

		return []

	def build_entry_map(self, entries: list[dict]) -> dict[str, dict]:
		entry_map: dict[str, dict] = {}
		for entry in entries:
			first_name = entry.get("first_name")
			if isinstance(first_name, str):
				entry_map[first_name.lower()] = entry
		return entry_map

	def search_entry(self, entry_map: dict[str, dict], key: str) -> dict | None:
		return entry_map.get(key.lower())

	def run(self) -> None:
		entries = self.load_entries()
		entry_map = self.build_entry_map(entries)

		print(f"Loaded {len(entry_map)} entries from {self.log_file.name}.")

		search_key = input("Enter a first name to search for: ").strip()
		result = self.search_entry(entry_map, search_key)

		if result is None:
			print("No entry found for that first name.")
			return

		print("Entry found:")
		for key, value in result.items():
			print(f"{key}: {value}")


def main() -> None:
	MacroReaderApp().run()


if __name__ == "__main__":
	main()