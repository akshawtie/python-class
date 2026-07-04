import json
from datetime import datetime
from pathlib import Path

from food_sets import get_food_sets


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


def save_entries(entries: list[dict]) -> None:
	LOG_FILE.write_text(json.dumps(entries, indent=2), encoding="utf-8")


def build_entry_map(entries: list[dict]) -> dict[str, dict]:
	entry_map: dict[str, dict] = {}
	for entry in entries:
		first_name = entry.get("first_name")
		if isinstance(first_name, str):
			entry_map[first_name.lower()] = entry
	return entry_map


def prompt_positive_integer(message: str) -> int:
	while True:
		raw_value = input(message).strip()
		try:
			value = int(raw_value)
			if value < 0:
				raise ValueError
			return value
		except ValueError:
			print("Please enter a whole number, 0 or higher.")


def add_entry() -> None:
	while True:
		first_name = input("What is your first name? ").strip()
		if not first_name:
			print("Please enter a first name.")
			continue

		carbs = prompt_positive_integer("How many carbs did you eat? ")
		fat = prompt_positive_integer("How much fat did you eat? ")
		protein = prompt_positive_integer("How much protein did you eat? ")
		break

	entries = load_entries()
	entries.append(
		{
			"first_name": first_name,
			"timestamp": datetime.now().isoformat(timespec="seconds"),
			"carbs": carbs,
			"fat": fat,
			"protein": protein,
		}
	)
	save_entries(entries)

	print(f"Saved {first_name}'s carbs, fat, and protein to {LOG_FILE.name}.")


def search_entry() -> None:
	entries = load_entries()
	entry_map = build_entry_map(entries)
	search_key = input("Enter a first name to search for: ").strip()
	result = entry_map.get(search_key.lower()) if search_key else None

	if result is None:
		print("No entry found for that first name.")
		return

	print("Entry found:")
	for key, value in result.items():
		print(f"{key}: {value}")


def show_food_sets() -> None:
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


def main() -> None:
	while True:
		print("\nMacro Tracker Menu")
		print("1. Add a new entry")
		print("2. Search an entry by first name")
		print("3. Show food sets")
		print("4. Exit")

		choice = input("Choose an option: ").strip()
		if choice == "1":
			add_entry()
		elif choice == "2":
			search_entry()
		elif choice == "3":
			show_food_sets()
		elif choice == "4":
			print("Goodbye.")
			break
		else:
			print("Please choose 1, 2, 3, or 4.")


if __name__ == "__main__":
	main()
