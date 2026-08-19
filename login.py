from __future__ import annotations

import hashlib
import json
import re
from datetime import datetime
from pathlib import Path

import tkinter as tk
from tkinter import messagebox, ttk


USERS_FILE = Path(__file__).with_name("login_users.json")


class LoginApp:
	EMAIL_REGEX = re.compile(r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$")
	PASSWORD_REGEX = re.compile(
		r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&#^()_+\-={}\[\]:;\"'<>,./\\|~`]).{8,}$"
	)

	def __init__(self, users_file: Path | None = None) -> None:
		self.users_file = users_file or USERS_FILE
		self.root = tk.Tk()
		self.root.title("Login / Signup")
		self.root.geometry("500x380")
		self.root.minsize(460, 340)

		self.status_var = tk.StringVar(value="Enter your details.")
		self.mode_var = tk.StringVar(value="login")

		self.email_var = tk.StringVar()
		self.password_var = tk.StringVar()

		self._build_ui()

	def _build_ui(self) -> None:
		frame = ttk.Frame(self.root, padding=18)
		frame.pack(fill="both", expand=True)

		title = ttk.Label(frame, text="Account Access", font=("Segoe UI", 16, "bold"))
		title.pack(anchor="w", pady=(0, 10))

		mode_frame = ttk.LabelFrame(frame, text="Mode", padding=10)
		mode_frame.pack(fill="x", pady=(0, 12))

		ttk.Radiobutton(
			mode_frame,
			text="Login",
			variable=self.mode_var,
			value="login",
			command=self._update_mode_text,
		).pack(side="left", padx=(0, 12))

		ttk.Radiobutton(
			mode_frame,
			text="Sign Up",
			variable=self.mode_var,
			value="signup",
			command=self._update_mode_text,
		).pack(side="left")

		form = ttk.Frame(frame)
		form.pack(fill="x")

		ttk.Label(form, text="Email").grid(row=0, column=0, sticky="w", pady=6)
		ttk.Entry(form, textvariable=self.email_var, width=36).grid(row=0, column=1, sticky="w", pady=6)

		ttk.Label(form, text="Password").grid(row=1, column=0, sticky="w", pady=6)
		ttk.Entry(form, textvariable=self.password_var, show="*", width=36).grid(row=1, column=1, sticky="w", pady=6)

		action_row = ttk.Frame(frame)
		action_row.pack(fill="x", pady=(12, 8))

		self.primary_button = ttk.Button(action_row, text="Login", command=self._submit)
		self.primary_button.pack(side="left")

		ttk.Button(action_row, text="Clear", command=self._clear_form).pack(side="left", padx=8)

		note_text = (
			"Password rule: at least 8 chars, with uppercase, lowercase, number, and symbol."
		)
		ttk.Label(frame, text=note_text, foreground="#444").pack(anchor="w", pady=(2, 10))

		status = ttk.Label(frame, textvariable=self.status_var, relief="sunken", anchor="w")
		status.pack(fill="x", side="bottom")

	def _update_mode_text(self) -> None:
		mode = self.mode_var.get()
		if mode == "signup":
			self.primary_button.config(text="Create Account")
			self.status_var.set("Create a new account.")
		else:
			self.primary_button.config(text="Login")
			self.status_var.set("Login with your account.")

	def _load_users(self) -> list[dict]:
		if not self.users_file.exists():
			return []

		try:
			data = json.loads(self.users_file.read_text(encoding="utf-8"))
		except json.JSONDecodeError:
			return []

		if isinstance(data, list):
			return data

		return []

	def _save_users(self, users: list[dict]) -> None:
		self.users_file.write_text(json.dumps(users, indent=2), encoding="utf-8")

	def _hash_password(self, password: str) -> str:
		return hashlib.sha256(password.encode("utf-8")).hexdigest()

	def _validate_email(self, email: str) -> bool:
		return bool(self.EMAIL_REGEX.fullmatch(email))

	def _validate_password(self, password: str) -> bool:
		return bool(self.PASSWORD_REGEX.fullmatch(password))

	def _clear_form(self) -> None:
		self.email_var.set("")
		self.password_var.set("")

	def _submit(self) -> None:
		email = self.email_var.get().strip()
		password = self.password_var.get()

		if not self._validate_email(email):
			messagebox.showerror("Invalid Email", "Please enter a valid email address.")
			self.status_var.set("Email validation failed.")
			return

		if not self._validate_password(password):
			messagebox.showerror(
				"Weak Password",
				"Password must be 8+ chars and include upper, lower, number, and symbol.",
			)
			self.status_var.set("Password validation failed.")
			return

		if self.mode_var.get() == "signup":
			self._handle_signup(email, password)
		else:
			self._handle_login(email, password)

	def _handle_signup(self, email: str, password: str) -> None:
		users = self._load_users()
		if any(str(user.get("email", "")).lower() == email.lower() for user in users):
			messagebox.showerror("Account Exists", "An account with this email already exists.")
			self.status_var.set("Signup failed: existing account.")
			return

		users.append(
			{
				"email": email,
				"password_hash": self._hash_password(password),
				"created_at": datetime.now().isoformat(timespec="seconds"),
			}
		)
		self._save_users(users)
		self._clear_form()
		self.status_var.set("Account created successfully.")
		messagebox.showinfo("Success", "Signup complete. You can now log in.")

	def _handle_login(self, email: str, password: str) -> None:
		users = self._load_users()
		target_hash = self._hash_password(password)

		for user in users:
			stored_email = str(user.get("email", "")).lower()
			stored_hash = str(user.get("password_hash", ""))
			if stored_email == email.lower() and stored_hash == target_hash:
				self.status_var.set(f"Welcome, {email}.")
				messagebox.showinfo("Login Success", f"Welcome back, {email}!")
				self._clear_form()
				return

		self.status_var.set("Login failed.")
		messagebox.showerror("Login Failed", "Invalid email or password.")

	def run(self) -> None:
		self.root.mainloop()


def main() -> None:
	LoginApp().run()


if __name__ == "__main__":
	main()
