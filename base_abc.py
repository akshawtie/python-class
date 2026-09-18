from __future__ import annotations

import json
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any


class BaseEntry(ABC):
	@abstractmethod
	def to_dict(self) -> dict[str, Any]:
		pass

	def __repr__(self) -> str:
		fields = ", ".join(f"{k}={v!r}" for k, v in self.to_dict().items())
		return f"{self.__class__.__name__}({fields})"


class BaseDataManager(ABC):
	def __init__(self, file_path: Path) -> None:
		self.file_path = file_path

	@abstractmethod
	def load_entries(self) -> list[dict[str, Any]]:
		pass

	@abstractmethod
	def save_entries(self, entries: list[dict[str, Any]]) -> None:
		pass

	@abstractmethod
	def search_entries(self, query: str) -> list[dict[str, Any]]:
		pass


class JSONDataManager(BaseDataManager):
	def load_entries(self) -> list[dict[str, Any]]:
		if not self.file_path.exists():
			return []

		try:
			data = json.loads(self.file_path.read_text(encoding="utf-8"))
		except (json.JSONDecodeError, OSError):
			return []

		if isinstance(data, list):
			return [item for item in data if isinstance(item, dict)]

		return []

	def save_entries(self, entries: list[dict[str, Any]]) -> None:
		self.file_path.write_text(json.dumps(entries, indent=2), encoding="utf-8")

	def search_entries(self, query: str) -> list[dict[str, Any]]:
		clean_query = query.strip().lower()
		if not clean_query:
			return self.load_entries()

		results: list[dict[str, Any]] = []
		for entry in self.load_entries():
			values_str = " ".join(str(v).lower() for v in entry.values())
			if clean_query in values_str:
				results.append(entry)
		return results


class BaseApp(ABC):
	@abstractmethod
	def run(self) -> None:
		pass


class BaseConsoleApp(BaseApp):
	@property
	@abstractmethod
	def app_title(self) -> str:
		pass

	@abstractmethod
	def display_menu(self) -> None:
		pass

	@abstractmethod
	def handle_choice(self, choice: str) -> bool:
		pass

	def run(self) -> None:
		while True:
			print(f"\n{self.app_title}")
			self.display_menu()
			choice = input("Choose an option: ").strip()
			should_continue = self.handle_choice(choice)
			if not should_continue:
				break

	@staticmethod
	def prompt_non_empty(prompt_message: str) -> str:
		while True:
			value = input(prompt_message).strip()
			if value:
				return value
			print("Please enter a non-empty value.")

	@staticmethod
	def prompt_positive_int(prompt_message: str) -> int:
		while True:
			raw = input(prompt_message).strip()
			try:
				val = int(raw)
				if val < 0:
					raise ValueError
				return val
			except ValueError:
				print("Please enter a whole number, 0 or higher.")


class BaseGUIApp(BaseApp):
	@abstractmethod
	def _build_layout(self) -> None:
		pass

	@abstractmethod
	def run(self) -> None:
		pass


class BaseAuthService(ABC):
	@abstractmethod
	def register_user(self, email: str, password: str) -> tuple[bool, str]:
		pass

	@abstractmethod
	def authenticate_user(self, email: str, password: str) -> tuple[bool, str]:
		pass


class BaseSubscriberManager(ABC):
	@abstractmethod
	def add_subscriber(self, name: str, g1: int, g2: int, g3: int) -> None:
		pass

	@abstractmethod
	def get_all_subscribers(self) -> dict[int, dict[str, Any]]:
		pass
