import json
from datetime import datetime
from pathlib import Path

from calendar_module import main as calendar_app_main
from food_sets import get_food_sets


LOG_FILE = Path(__file__).with_name("macro_log.json")


class CalorieTrackerApp:
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

	def save_entries(self, entries: list[dict]) -> None:
		self.log_file.write_text(json.dumps(entries, indent=2), encoding="utf-8")

	def build_entry_map(self, entries: list[dict]) -> dict[str, dict]:
		entry_map: dict[str, dict] = {}
		for entry in entries:
			first_name = entry.get("first_name")
			if isinstance(first_name, str):
				entry_map[first_name.lower()] = entry
		return entry_map

	def prompt_positive_integer(self, message: str) -> int:
		while True:
			raw_value = input(message).strip()
			try:
				value = int(raw_value)
				if value < 0:
					raise ValueError
				return value
			except ValueError:
				print("Please enter a whole number, 0 or higher.")

	def add_entry(self) -> None:
		while True:
			first_name = input("What is your first name? ").strip()
			if not first_name:
				print("Please enter a first name.")
				continue

			carbs = self.prompt_positive_integer("How many carbs did you eat? ")
			fat = self.prompt_positive_integer("How much fat did you eat? ")
			protein = self.prompt_positive_integer("How much protein did you eat? ")
			total_calories = (carbs * 4) + (fat * 9) + (protein * 4)
			break

		entries = self.load_entries()
		entries.append(
			{
				"first_name": first_name,
				"timestamp": datetime.now().isoformat(timespec="seconds"),
				"carbs": carbs,
				"fat": fat,
				"protein": protein,
				"total_calories": total_calories,
			}
		)
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

	def run(self) -> None:
		while True:
			print("\nMacro Tracker Menu")
			print("1. Add a new entry")
			print("2. Search an entry by first name")
			print("3. Show food sets")
			print("4. Exit")

			choice = input("Choose an option: ").strip()
			if choice == "1":
				self.add_entry()
			elif choice == "2":
				self.search_entry()
			elif choice == "3":
				self.show_food_sets()
			elif choice == "4":
				print("Goodbye.")
				break
			else:
				print("Please choose 1, 2, 3, or 4.")


def calorie_tracker_main() -> None:
	CalorieTrackerApp().run()


def main() -> None:
	while True:
		print("\nWelcome Sweet Child O Mine")
		print("1. Open calorie tracker app")
		print("2. Open calendar app")
		print("3. Exit")

		choice = input("Choose an option: ").strip()
		if choice == "1":
			calorie_tracker_main()
		elif choice == "2":
			calendar_app_main()
		elif choice == "3":
			print("Goodbye.")
			break
		else:
			print("Please choose 1, 2, or 3.")


if __name__ == "__main__":
	main()
