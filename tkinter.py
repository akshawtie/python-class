from __future__ import annotations

import os
import sys
from datetime import datetime


# This file is named tkinter.py, so temporarily remove this folder from sys.path
# to import the standard library tkinter module instead of this file.
_CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
_REMOVED = False
if _CURRENT_DIR in sys.path:
	sys.path.remove(_CURRENT_DIR)
	_REMOVED = True

import tkinter as tk
from tkinter import messagebox, ttk

if _REMOVED:
	sys.path.insert(0, _CURRENT_DIR)

from food_sets import get_food_sets
from test import CalorieTrackerApp


class MacroTrackerGUI:
	def __init__(self) -> None:
		self.app = CalorieTrackerApp()
		self.root = tk.Tk()
		self.root.title("Macro Tracker")
		self.root.geometry("760x520")
		self.root.minsize(680, 460)

		self.status_var = tk.StringVar(value="Ready")

		self._build_layout()
		self._refresh_entries_table()

	def _build_layout(self) -> None:
		container = ttk.Frame(self.root, padding=14)
		container.pack(fill="both", expand=True)

		title = ttk.Label(container, text="Macro Tracker Dashboard", font=("Segoe UI", 16, "bold"))
		title.pack(anchor="w", pady=(0, 10))

		notebook = ttk.Notebook(container)
		notebook.pack(fill="both", expand=True)

		self.tab_add = ttk.Frame(notebook, padding=12)
		self.tab_search = ttk.Frame(notebook, padding=12)
		self.tab_foods = ttk.Frame(notebook, padding=12)
		self.tab_entries = ttk.Frame(notebook, padding=12)

		notebook.add(self.tab_add, text="Add Entry")
		notebook.add(self.tab_search, text="Search")
		notebook.add(self.tab_foods, text="Food Sets")
		notebook.add(self.tab_entries, text="All Entries")

		self._build_add_tab()
		self._build_search_tab()
		self._build_food_tab()
		self._build_entries_tab()

		status_bar = ttk.Label(container, textvariable=self.status_var, relief="sunken", anchor="w")
		status_bar.pack(fill="x", pady=(10, 0))

	def _build_add_tab(self) -> None:
		self.first_name_var = tk.StringVar()
		self.carbs_var = tk.StringVar()
		self.fat_var = tk.StringVar()
		self.protein_var = tk.StringVar()

		fields = [
			("First name", self.first_name_var),
			("Carbs (g)", self.carbs_var),
			("Fat (g)", self.fat_var),
			("Protein (g)", self.protein_var),
		]

		for idx, (label_text, var) in enumerate(fields):
			ttk.Label(self.tab_add, text=label_text).grid(row=idx, column=0, sticky="w", pady=6)
			ttk.Entry(self.tab_add, textvariable=var, width=28).grid(row=idx, column=1, sticky="w", pady=6)

		button_row = ttk.Frame(self.tab_add)
		button_row.grid(row=len(fields), column=0, columnspan=2, sticky="w", pady=(12, 0))

		ttk.Button(button_row, text="Save Entry", command=self._save_entry).pack(side="left")
		ttk.Button(button_row, text="Clear", command=self._clear_add_form).pack(side="left", padx=8)

		note = ttk.Label(
			self.tab_add,
			text="Calories are calculated as carbs*4 + fat*9 + protein*4.",
			foreground="#444",
		)
		note.grid(row=len(fields) + 1, column=0, columnspan=2, sticky="w", pady=(12, 0))

	def _build_search_tab(self) -> None:
		self.search_name_var = tk.StringVar()

		ttk.Label(self.tab_search, text="First name").grid(row=0, column=0, sticky="w", pady=6)
		ttk.Entry(self.tab_search, textvariable=self.search_name_var, width=28).grid(row=0, column=1, sticky="w", pady=6)
		ttk.Button(self.tab_search, text="Search", command=self._search_entry).grid(row=0, column=2, padx=8)

		self.search_result = tk.Text(self.tab_search, height=14, width=80)
		self.search_result.grid(row=1, column=0, columnspan=3, sticky="nsew", pady=(10, 0))

		self.tab_search.grid_columnconfigure(1, weight=1)
		self.tab_search.grid_rowconfigure(1, weight=1)

	def _build_food_tab(self) -> None:
		self.food_sets = get_food_sets()
		self.food_category_var = tk.StringVar()

		ttk.Label(self.tab_foods, text="Category").grid(row=0, column=0, sticky="w")
		self.food_combo = ttk.Combobox(
			self.tab_foods,
			textvariable=self.food_category_var,
			values=list(self.food_sets.keys()),
			state="readonly",
			width=30,
		)
		self.food_combo.grid(row=0, column=1, sticky="w")
		self.food_combo.bind("<<ComboboxSelected>>", self._update_food_list)

		self.food_listbox = tk.Listbox(self.tab_foods, height=16, width=60)
		self.food_listbox.grid(row=1, column=0, columnspan=2, sticky="nsew", pady=(10, 0))

		self.tab_foods.grid_rowconfigure(1, weight=1)
		self.tab_foods.grid_columnconfigure(1, weight=1)

		if self.food_combo["values"]:
			self.food_combo.current(0)
			self._update_food_list()

	def _build_entries_tab(self) -> None:
		columns = ("first_name", "timestamp", "carbs", "fat", "protein", "total_calories")
		self.entries_table = ttk.Treeview(self.tab_entries, columns=columns, show="headings", height=14)

		headings = {
			"first_name": "First Name",
			"timestamp": "Timestamp",
			"carbs": "Carbs",
			"fat": "Fat",
			"protein": "Protein",
			"total_calories": "Total Calories",
		}
		for key in columns:
			self.entries_table.heading(key, text=headings[key])
			self.entries_table.column(key, width=110, anchor="center")

		self.entries_table.column("timestamp", width=170, anchor="center")
		self.entries_table.pack(fill="both", expand=True)

		ttk.Button(self.tab_entries, text="Refresh", command=self._refresh_entries_table).pack(anchor="e", pady=(8, 0))

	def _parse_non_negative_int(self, label: str, raw_value: str) -> int:
		try:
			value = int(raw_value)
		except ValueError as exc:
			raise ValueError(f"{label} must be a whole number.") from exc

		if value < 0:
			raise ValueError(f"{label} must be 0 or higher.")

		return value

	def _save_entry(self) -> None:
		first_name = self.first_name_var.get().strip()
		if not first_name:
			messagebox.showerror("Missing Name", "Please enter a first name.")
			return

		try:
			carbs = self._parse_non_negative_int("Carbs", self.carbs_var.get().strip())
			fat = self._parse_non_negative_int("Fat", self.fat_var.get().strip())
			protein = self._parse_non_negative_int("Protein", self.protein_var.get().strip())
		except ValueError as err:
			messagebox.showerror("Invalid Input", str(err))
			return

		total_calories = (carbs * 4) + (fat * 9) + (protein * 4)
		entries = self.app.load_entries()
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
		self.app.save_entries(entries)

		self._clear_add_form()
		self._refresh_entries_table()
		self.status_var.set(f"Saved entry for {first_name}.")
		messagebox.showinfo("Saved", f"Entry saved for {first_name}.")

	def _clear_add_form(self) -> None:
		self.first_name_var.set("")
		self.carbs_var.set("")
		self.fat_var.set("")
		self.protein_var.set("")

	def _search_entry(self) -> None:
		self.search_result.delete("1.0", tk.END)
		query = self.search_name_var.get().strip()
		if not query:
			self.search_result.insert(tk.END, "Please enter a first name to search.")
			return

		entries = self.app.load_entries()
		entry_map = self.app.build_entry_map(entries)
		entry = entry_map.get(query.lower())

		if entry is None:
			self.search_result.insert(tk.END, "No entry found for that first name.")
			self.status_var.set(f"No match for {query}.")
			return

		for key, value in entry.items():
			self.search_result.insert(tk.END, f"{key}: {value}\n")

		self.status_var.set(f"Found entry for {query}.")

	def _update_food_list(self, _event: object | None = None) -> None:
		self.food_listbox.delete(0, tk.END)
		selected = self.food_category_var.get()
		foods = self.food_sets.get(selected, set())
		for food in sorted(foods):
			self.food_listbox.insert(tk.END, food)

	def _refresh_entries_table(self) -> None:
		for item_id in self.entries_table.get_children():
			self.entries_table.delete(item_id)

		entries = self.app.load_entries()
		for entry in entries:
			self.entries_table.insert(
				"",
				tk.END,
				values=(
					entry.get("first_name", ""),
					entry.get("timestamp", ""),
					entry.get("carbs", ""),
					entry.get("fat", ""),
					entry.get("protein", ""),
					entry.get("total_calories", ""),
				),
			)

		self.status_var.set(f"Loaded {len(entries)} entries.")

	def run(self) -> None:
		self.root.mainloop()


def main() -> None:
	MacroTrackerGUI().run()


if __name__ == "__main__":
	main()
