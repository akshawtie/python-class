"""
macro_reader.py - Macro Log Reader Application

Refactored to implement Python's ABC model and Object-Oriented Inheritance:
  - MacroReaderApp inherits from BaseConsoleApp (ABC) and uses JSONDataManager.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from base_abc import BaseConsoleApp, JSONDataManager

LOG_FILE = Path(__file__).with_name("macro_log.json")


class MacroReaderApp(BaseConsoleApp):
	"""Application to search and inspect nutrition macro logs.

	Inherits from `BaseConsoleApp` (ABC) and utilizes `JSONDataManager`.
	"""

	def __init__(self, log_file: Path | None = None) -> None:
		self.log_file = log_file or LOG_FILE
		self.data_manager = JSONDataManager(self.log_file)

	@property
	def app_title(self) -> str:
		return "Macro Reader Menu"

	def load_entries(self) -> list[dict[str, Any]]:
		"""Load macro records from file."""
		return self.data_manager.load_entries()

	def build_entry_map(self, entries: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
		"""Index entries by lowercased first name."""
		entry_map: dict[str, dict[str, Any]] = {}
		for entry in entries:
			first_name = entry.get("first_name")
			if isinstance(first_name, str):
				entry_map[first_name.lower()] = entry
		return entry_map

	def search_entry(self, entry_map: dict[str, dict[str, Any]], key: str) -> dict[str, Any] | None:
		"""Find an entry by name key."""
		return entry_map.get(key.lower())

	def perform_search(self) -> None:
		"""Interactive search prompt and display."""
		entries = self.load_entries()
		entry_map = self.build_entry_map(entries)

		print(f"Loaded {len(entry_map)} entries from {self.log_file.name}.")
		search_key = self.prompt_non_empty("Enter a first name to search for: ")
		result = self.search_entry(entry_map, search_key)

		if result is None:
			print("No entry found for that first name.")
			return

		print("\nEntry found:")
		for key, value in result.items():
			print(f"  {key}: {value}")

	def list_all_entries(self) -> None:
		"""List all names present in the macro log."""
		entries = self.load_entries()
		if not entries:
			print("No entries recorded in macro log.")
			return

		print(f"\nRecorded Entries ({len(entries)} total):")
		for idx, entry in enumerate(entries, start=1):
			name = entry.get("first_name", "Unknown")
			calories = entry.get("total_calories", "N/A")
			timestamp = entry.get("timestamp", "N/A")
			print(f"{idx}. {name} - {calories} kcal ({timestamp})")

	def display_menu(self) -> None:
		print("1. Search an entry by first name")
		print("2. List all recorded entries")
		print("3. Exit")

	def handle_choice(self, choice: str) -> bool:
		if choice == "1":
			self.perform_search()
		elif choice == "2":
			self.list_all_entries()
		elif choice == "3":
			print("Goodbye.")
			return False
		else:
			print("Please choose 1, 2, or 3.")
		return True


def main() -> None:
	MacroReaderApp().run()


if __name__ == "__main__":
	main()