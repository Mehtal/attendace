import hashlib
import sqlite3
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
from kivy.uix.screenmanager import Screen


class LoginScreen(Screen):

    def signup(self, username, password):
        if len(password) < 8:
            self.ids.password_field.error = True
            self.ids.password_field.error_text = (
                "Password should be 8 characters or longer"
            )
            return

        hashed_password = hashlib.md5(password.encode()).hexdigest()

        conn = sqlite3.connect("sqlite.db")
        cursor = conn.cursor()
        query = """
            CREATE TABLE IF NOT EXISTS users(
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
            );
        """
        cursor.execute(query)
        conn.commit()

        try:
            cursor.execute(
                "INSERT INTO users (username, password) VALUES (?, ?)",
                (username, hashed_password),
            )
            conn.commit()
            conn.close()
            self.show_success_dialog("signup")
        except sqlite3.Error as e:
            print(f"Error occurred: {e}")

            self.show_failure_dialog()

    def login(self, username, password):
        conn = sqlite3.connect("sqlite.db")
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM users WHERE username=?", (username,))
        user = cursor.fetchone()

        if user:
            hashed_password_db = user[1]

            hashed_password_input = hashlib.md5(password.encode()).hexdigest()

            if hashed_password_input == hashed_password_db:
                self.show_success_dialog("login")
                self.manager.current = "sup"
            else:
                self.show_failure_dialog()
        else:
            self.show_failure_dialog()

        conn.close()

    def show_success_dialog(self, action):
        dialog = MDDialog(
            text=f"{action} successful!",
            buttons=[
                MDFlatButton(text="OK", on_release=lambda *args: dialog.dismiss())
            ],
        )
        dialog.open()

    def show_failure_dialog(self):
        dialog = MDDialog(
            text="Login failed. Please check your credentials.",
            buttons=[
                MDFlatButton(text="OK", on_release=lambda *args: dialog.dismiss())
            ],
        )
        dialog.open()
