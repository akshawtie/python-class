
import json
from datetime import datetime
from pathlib import Path
from typing import Any

from base_abc import BaseConsoleApp, BaseEntry
from calendar_module import main as calendar_app_main
from food_sets import get_food_sets
from upcoming_calendar import main as upcoming_calendar_main

LOG_FILE = Path(__file__).with_name("macro_log.json")


class MacroEntry(BaseEntry):
	def __init__(
		self,
		first_name: str,
		carbs: int,
		fat: int,
		protein: int,
		timestamp: str | None = None,
	) -> None:
		self.first_name = first_name
		self.carbs = carbs
		self.fat = fat
		self.protein = protein
		self.total_calories = (carbs * 4) + (fat * 9) + (protein * 4)
		self.timestamp = timestamp or datetime.now().isoformat(timespec="seconds")

	def to_dict(self) -> dict[str, Any]:
		return {
			"first_name": self.first_name,
			"timestamp": self.timestamp,
			"carbs": self.carbs,
			"fat": self.fat,
			"protein": self.protein,
			"total_calories": self.total_calories,
		}


class CalorieTrackerApp(BaseConsoleApp):
	def __init__(self, log_file: Path | None = None) -> None:
		self.log_file = log_file or LOG_FILE

	@property
	def app_title(self) -> str:
		return "Macro Tracker Menu"

	def load_entries(self) -> list[dict[str, Any]]:
		if not self.log_file.exists():
			return []

		try:
			data = json.loads(self.log_file.read_text(encoding="utf-8"))
		except json.JSONDecodeError:
			return []

		if isinstance(data, list):
			return data

		return []

	def save_entries(self, entries: list[dict[str, Any]]) -> None:
		self.log_file.write_text(json.dumps(entries, indent=2), encoding="utf-8")

	def build_entry_map(self, entries: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
		entry_map: dict[str, dict[str, Any]] = {}
		for entry in entries:
			first_name = entry.get("first_name")
			if isinstance(first_name, str):
				entry_map[first_name.lower()] = entry
		return entry_map

	def prompt_positive_integer(self, message: str) -> int:
		return self.prompt_positive_int(message)

	def add_entry(self) -> None:
		first_name = self.prompt_non_empty("What is your first name? ")
		carbs = self.prompt_positive_int("How many carbs did you eat? ")
		fat = self.prompt_positive_int("How much fat did you eat? ")
		protein = self.prompt_positive_int("How much protein did you eat? ")

		entry = MacroEntry(first_name, carbs, fat, protein)
		entries = self.load_entries()
		entries.append(entry.to_dict())
		self.save_entries(entries)

		print(f"Saved {first_name}'s carbs, fat, and protein to {self.log_file.name}.")

	def search_entry(self) -> None:
		entries = self.load_entries()
		entry_map = self.build_entry_map(entries)
		search_key = input("Enter a first name to search for: ").strip()
		result = entry_map.get(search_key.lower()) if search_key else None

		if result is None:
			print("No entry found for that first name.")
			return

		print("Entry found:")
		for key, value in result.items():
			print(f"{key}: {value}")

	def show_food_sets(self) -> None:
		look_at_foods = input("Do you want to look at foods? (y/n): ").strip().lower()
		if look_at_foods not in {"y", "yes"}:
			print("Okay, returning to the menu.")
			return

		food_sets = get_food_sets()
		print("Choose a food category:")
		print("1. Protein Rich Foods")
		print("2. Well Balanced Foods")
		print("3. Booster Foods")

		category_choice = input("Choose 1, 2, or 3: ").strip()
		category_lookup = {
			"1": "Protein Rich Foods",
			"2": "Well Balanced Foods",
			"3": "Booster Foods",
		}
		title = category_lookup.get(category_choice)
		if title is None:
			print("Please choose 1, 2, or 3.")
			return

		foods = food_sets[title]
		print(f"\n{title}:")
		for food in sorted(foods):
			print(f"- {food}")

	def display_menu(self) -> None:
		print("1. Add a new entry")
		print("2. Search an entry by first name")
		print("3. Show food sets")
		print("4. Exit")

	def handle_choice(self, choice: str) -> bool:
		if choice == "1":
			self.add_entry()
		elif choice == "2":
			self.search_entry()
		elif choice == "3":
			self.show_food_sets()
		elif choice == "4":
			print("Goodbye.")
			return False
		else:
			print("Please choose 1, 2, 3, or 4.")
		return True


def calorie_tracker_main() -> None:
	CalorieTrackerApp().run()


def main() -> None:
	while True:
		print("\nWelcome Sweet Child O Mine")
		print("1. Open calorie tracker app")
		print("2. Open calendar app")
		print("3. View upcoming 15-day calendar")
		print("4. Exit")

		choice = input("Choose an option: ").strip()
		if choice == "1":
			calorie_tracker_main()
		elif choice == "2":
			calendar_app_main()
		elif choice == "3":
			upcoming_calendar_main()
		elif choice == "4":
			print("Goodbye.")
			break
		else:
			print("Please choose 1, 2, 3, or 4.")


if __name__ == "__main__":
	main()
