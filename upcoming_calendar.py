from __future__ import annotations

import json
import os
import sys
from abc import ABC, abstractmethod
from datetime import date, datetime, timedelta
from pathlib import Path
from typing import Any

if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
	try:
		sys.stdout.reconfigure(encoding="utf-8")
	except Exception:
		pass

DEFAULT_EVENTS_FILE = Path(__file__).with_name("calendar_events.json")


class TerminalColors:
	RESET = "\033[0m"
	BOLD = "\033[1m"
	DIM = "\033[2m"
	UNDERLINE = "\033[4m"

	FG_BLACK = "\033[30m"
	FG_RED = "\033[31m"
	FG_GREEN = "\033[32m"
	FG_YELLOW = "\033[33m"
	FG_BLUE = "\033[34m"
	FG_MAGENTA = "\033[35m"
	FG_CYAN = "\033[36m"
	FG_WHITE = "\033[37m"
	FG_BRIGHT_GREEN = "\033[92m"
	FG_BRIGHT_YELLOW = "\033[93m"
	FG_BRIGHT_CYAN = "\033[96m"
	FG_BRIGHT_WHITE = "\033[97m"

	BG_BLUE = "\033[44m"
	BG_MAGENTA = "\033[45m"
	BG_CYAN = "\033[46m"
	BG_GREEN = "\033[42m"
	BG_DARK_GRAY = "\033[100m"

	@classmethod
	def enable_windows_ansi(cls) -> None:
		if os.name == "nt":
			try:
				import ctypes
				kernel32 = ctypes.windll.kernel32
				handle = kernel32.GetStdHandle(-11)
				mode = ctypes.c_ulong()
				kernel32.GetConsoleMode(handle, ctypes.byref(mode))
				mode.value |= 0x0004
				kernel32.SetConsoleMode(handle, mode)
			except Exception:
				pass


class BaseEventProvider(ABC):
	@abstractmethod
	def get_all_events(self) -> list[dict[str, Any]]:
		pass

	@abstractmethod
	def get_events_for_date(self, target_date: date) -> list[dict[str, Any]]:
		pass

	@abstractmethod
	def get_events_in_range(self, start_date: date, end_date: date) -> dict[str, list[dict[str, Any]]]:
		pass


class JSONEventProvider(BaseEventProvider):
	def __init__(self, file_path: Path | str | None = None) -> None:
		self.file_path = Path(file_path) if file_path else DEFAULT_EVENTS_FILE

	def get_all_events(self) -> list[dict[str, Any]]:
		if not self.file_path.exists():
			return []

		try:
			data = json.loads(self.file_path.read_text(encoding="utf-8"))
		except (json.JSONDecodeError, OSError):
			return []

		if isinstance(data, list):
			return [item for item in data if isinstance(item, dict)]

		return []

	def _parse_date(self, raw_date_str: str) -> date | None:
		try:
			return datetime.strptime(raw_date_str.strip(), "%Y-%m-%d").date()
		except (ValueError, TypeError, AttributeError):
			return None

	def get_events_for_date(self, target_date: date) -> list[dict[str, Any]]:
		target_iso = target_date.isoformat()
		matching_events: list[dict[str, Any]] = []

		for event in self.get_all_events():
			if str(event.get("date", "")).strip() == target_iso:
				matching_events.append(event)

		return matching_events

	def get_events_in_range(self, start_date: date, end_date: date) -> dict[str, list[dict[str, Any]]]:
		events_map: dict[str, list[dict[str, Any]]] = {}
		all_events = self.get_all_events()

		for event in all_events:
			event_date = self._parse_date(str(event.get("date", "")))
			if event_date is not None and start_date <= event_date <= end_date:
				iso_key = event_date.isoformat()
				events_map.setdefault(iso_key, []).append(event)

		return events_map


class BaseCalendarRenderer(ABC):
	def __init__(self, event_provider: BaseEventProvider) -> None:
		self.event_provider = event_provider

	@abstractmethod
	def render(self, start_date: date | None = None, days_count: int = 15) -> None:
		pass

	@abstractmethod
	def format_day_entry(
		self,
		day_date: date,
		events: list[dict[str, Any]],
		is_today: bool,
	) -> str:
		pass


class Terminal15DayCalendar(BaseCalendarRenderer):
	def __init__(self, event_provider: BaseEventProvider | None = None) -> None:
		provider = event_provider or JSONEventProvider()
		super().__init__(provider)
		TerminalColors.enable_windows_ansi()

	def format_day_entry(
		self,
		day_date: date,
		events: list[dict[str, Any]],
		is_today: bool,
	) -> str:
		c = TerminalColors
		day_name = day_date.strftime("%A")
		date_str = day_date.isoformat()

		today_badge = f"{c.BG_CYAN}{c.FG_BLACK}{c.BOLD} TODAY {c.RESET} " if is_today else ""

		if events:
			event_count = len(events)
			event_badge = f"{c.BG_GREEN}{c.FG_BLACK}{c.BOLD} [EVENT: {event_count}] {c.RESET}"
			header = f"{c.BOLD}{c.FG_BRIGHT_YELLOW}> {date_str} ({day_name[:3]}){c.RESET} {today_badge}{event_badge}"

			event_lines = []
			for idx, ev in enumerate(events, start=1):
				title = ev.get("title", "Untitled Event")
				desc = ev.get("description", "").strip()
				desc_part = f" {c.DIM}- {desc}{c.RESET}" if desc else ""
				event_lines.append(f"    {c.FG_BRIGHT_GREEN}* [{idx}] {c.BOLD}{title}{c.RESET}{desc_part}")

			return f"{header}\n" + "\n".join(event_lines)
		else:
			color = c.FG_BRIGHT_WHITE if is_today else c.FG_WHITE
			dim_indicator = f"{c.DIM}(No events scheduled){c.RESET}"
			return f"{color}  {date_str} ({day_name[:3]}){c.RESET} {today_badge}{dim_indicator}"

	def _render_mini_grid(
		self,
		start_date: date,
		days_count: int,
		events_by_date: dict[str, list[dict[str, Any]]],
	) -> None:
		c = TerminalColors
		print(f"\n{c.BOLD}{c.FG_BRIGHT_CYAN}--- 15-DAY OVERVIEW STRIP ---{c.RESET}")

		top_row: list[str] = []
		day_row: list[str] = []

		today = date.today()
		for offset in range(days_count):
			current_date = start_date + timedelta(days=offset)
			iso_key = current_date.isoformat()
			has_events = iso_key in events_by_date
			is_today = current_date == today

			day_num = f"{current_date.day:02d}"
			weekday_letter = current_date.strftime("%a")[:2]

			if has_events:
				top_cell = f"{c.BG_GREEN}{c.FG_BLACK}{c.BOLD}{weekday_letter}{c.RESET}"
				day_cell = f"{c.BG_GREEN}{c.FG_BLACK}{c.BOLD}{day_num}*{c.RESET}"
			elif is_today:
				top_cell = f"{c.BG_CYAN}{c.FG_BLACK}{c.BOLD}{weekday_letter}{c.RESET}"
				day_cell = f"{c.BG_CYAN}{c.FG_BLACK}{c.BOLD}{day_num}T{c.RESET}"
			else:
				top_cell = f"{c.DIM}{weekday_letter}{c.RESET}"
				day_cell = f"{c.FG_WHITE}{day_num} {c.RESET}"

			top_row.append(top_cell)
			day_row.append(day_cell)

		print("  " + " | ".join(top_row))
		print("  " + " | ".join(day_row))
		print(f"  {c.DIM}Legend: {c.BG_GREEN}{c.FG_BLACK} * Event {c.RESET}  {c.BG_CYAN}{c.FG_BLACK} T Today {c.RESET}{c.RESET}\n")

	def render(self, start_date: date | None = None, days_count: int = 15) -> None:
		c = TerminalColors
		if start_date is None:
			start_date = date.today()

		end_date = start_date + timedelta(days=days_count - 1)
		events_by_date = self.event_provider.get_events_in_range(start_date, end_date)
		total_events_in_range = sum(len(evs) for evs in events_by_date.values())

		print(f"\n{c.BG_BLUE}{c.FG_BRIGHT_WHITE}{c.BOLD}  UPCOMING 15-DAY CALENDAR SCHEDULE  {c.RESET}")
		print(
			f"{c.DIM}Range: {c.BOLD}{start_date.isoformat()}{c.RESET}{c.DIM} to "
			f"{c.BOLD}{end_date.isoformat()}{c.RESET} | "
			f"Upcoming Events: {c.FG_BRIGHT_GREEN}{c.BOLD}{total_events_in_range}{c.RESET}"
		)

		self._render_mini_grid(start_date, days_count, events_by_date)

		print(f"{c.BOLD}{c.FG_BRIGHT_CYAN}--- DETAILED DAY-BY-DAY SCHEDULE ---{c.RESET}")
		today = date.today()
		for offset in range(days_count):
			current_date = start_date + timedelta(days=offset)
			iso_key = current_date.isoformat()
			events = events_by_date.get(iso_key, [])
			is_today = current_date == today

			day_output = self.format_day_entry(current_date, events, is_today)
			print(day_output)

		print(f"{c.DIM}{'-' * 52}{c.RESET}\n")


def main() -> None:
	provider = JSONEventProvider(DEFAULT_EVENTS_FILE)
	calendar_app = Terminal15DayCalendar(provider)
	calendar_app.render()


if __name__ == "__main__":
	main()
