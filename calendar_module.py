import json
from datetime import datetime, date, timedelta
from pathlib import Path


__all__ = ["CalendarEventEntry", "CalendarEventApp", "main"]


_EVENTS_FILE = Path(__file__).with_name("calendar_events.json")


class CalendarEventEntry:
	def __init__(
		self,
		title: str,
		event_date: str | None = None,
		description: str = "",
		created_at: str | None = None,
	) -> None:
		self.title = title
		self.event_date = event_date or (date.today() + timedelta(days=1)).isoformat()
		self.description = description
		self.created_at = created_at or datetime.now().isoformat(timespec="seconds")

	def to_dict(self) -> dict:
		return {
			"title": self.title,
			"date": self.event_date,
			"description": self.description,
			"created_at": self.created_at,
		}


class CalendarEventApp:
	def __init__(self, events_file: Path | None = None) -> None:
		self.events_file = events_file or _EVENTS_FILE

	def _load_events(self) -> list[dict]:
		if not self.events_file.exists():
			return []

		try:
			data = json.loads(self.events_file.read_text(encoding="utf-8"))
		except json.JSONDecodeError:
			return []

		if isinstance(data, list):
			return [event for event in data if isinstance(event, dict)]

		return []

	def _save_events(self, events: list[dict]) -> None:
		self.events_file.write_text(json.dumps(events, indent=2), encoding="utf-8")

	def _parse_event_date(self, raw_value: str) -> date | None:
		try:
			return datetime.strptime(raw_value, "%Y-%m-%d").date()
		except ValueError:
			return None

	def _prompt_event_date(self, message: str) -> str:
		while True:
			raw_value = input(message).strip()
			if not raw_value:
				return (date.today() + timedelta(days=1)).isoformat()
			parsed_date = self._parse_event_date(raw_value)
			if parsed_date is None:
				print("Please enter a valid date in YYYY-MM-DD format.")
				continue
			return parsed_date.isoformat()

	def _prompt_non_empty(self, message: str) -> str:
		while True:
			value = input(message).strip()
			if value:
				return value
			print("Please enter a value.")

	def _sort_events(self, events: list[dict]) -> list[dict]:
		def event_sort_key(event: dict) -> tuple[str, str]:
			return (
				str(event.get("date", "9999-12-31")),
				str(event.get("title", "")),
			)

		return sorted(events, key=event_sort_key)

	def _matches_search(self, event: dict, search_term: str) -> bool:
		search_term = search_term.strip().lower()
		if not search_term:
			return True

		fields = (
			str(event.get("title", "")),
			str(event.get("date", "")),
			str(event.get("description", "")),
		)
		return any(search_term in field.lower() for field in fields)

	def add_event(self) -> None:
		title = self._prompt_non_empty("Event title: ")
		event_date = self._prompt_event_date("Event date (YYYY-MM-DD, press Enter for tomorrow): ")
		description = input("Optional description: ").strip()

		events = self._load_events()
		events.append(CalendarEventEntry(title, event_date, description).to_dict())
		self._save_events(self._sort_events(events))

		print(f"Saved '{title}' for {event_date} in {self.events_file.name}.")

	def show_upcoming_events(self) -> None:
		events = self._sort_events(self._load_events())
		today = date.today()

		upcoming_events = []
		for event in events:
			parsed_date = self._parse_event_date(str(event.get("date", "")))
			if parsed_date is not None and parsed_date >= today:
				upcoming_events.append((parsed_date, event))

		if not upcoming_events:
			print("No upcoming events found.")
			return

		print("Upcoming events:")
		for index, (event_date, event) in enumerate(upcoming_events, start=1):
			title = event.get("title", "Untitled event")
			description = event.get("description", "")
			print(f"{index}. {event_date.isoformat()} - {title}")
			if description:
				print(f"   {description}")

	def display_events(self, search_term: str | None = None) -> None:
		events = self._sort_events(self._load_events())
		if search_term:
			events = [event for event in events if self._matches_search(event, search_term)]

		if not events:
			message = "No matching events found." if search_term else "No events found."
			print(message)
			return

		heading = "Matching events:" if search_term else "All events:"
		print(heading)
		for index, event in enumerate(events, start=1):
			title = event.get("title", "Untitled event")
			event_date = event.get("date", "Unknown date")
			description = event.get("description", "")
			print(f"{index}. {event_date} - {title}")
			if description:
				print(f"   {description}")

	def search_events(self) -> None:
		search_term = self._prompt_non_empty("Search events by title, date, or description: ")
		self.display_events(search_term)

	def delete_event(self) -> None:
		events = self._sort_events(self._load_events())
		if not events:
			print("No events to delete.")
			return

		print("Events:")
		for index, event in enumerate(events, start=1):
			title = event.get("title", "Untitled event")
			event_date = event.get("date", "Unknown date")
			print(f"{index}. {event_date} - {title}")

		raw_choice = input("Choose an event number to delete: ").strip()
		try:
			choice = int(raw_choice)
			if choice < 1 or choice > len(events):
				raise ValueError
		except ValueError:
			print("Please choose a valid event number.")
			return

		removed_event = events.pop(choice - 1)
		self._save_events(events)
		print(f"Deleted '{removed_event.get('title', 'Untitled event')}'.")

	def run(self) -> None:
		while True:
			print("\nCalendar Menu")
			print("1. Add an event")
			print("2. Delete an event")
			print("3. See upcoming events")
			print("4. Display all events")
			print("5. Search events")
			print("6. Exit")

			choice = input("Choose an option: ").strip()
			if choice == "1":
				self.add_event()
			elif choice == "2":
				self.delete_event()
			elif choice == "3":
				self.show_upcoming_events()
			elif choice == "4":
				self.display_events()
			elif choice == "5":
				self.search_events()
			elif choice == "6":
				print("Goodbye.")
				break
			else:
				print("Please choose 1, 2, 3, 4, 5, or 6.")


def main() -> None:
	CalendarEventApp().run()


if __name__ == "__main__":
	main()