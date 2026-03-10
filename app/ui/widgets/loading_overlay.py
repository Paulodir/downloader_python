from __future__ import annotations

import customtkinter as ctk


class LoadingOverlay(ctk.CTkFrame):
    def __init__(self, master: ctk.CTkFrame):
        super().__init__(master, fg_color=("gray88", "gray18"), corner_radius=18)
        self.place_forget()

        self.grid_columnconfigure(0, weight=1)

        self.label = ctk.CTkLabel(
            self,
            text="Carregando...",
            font=ctk.CTkFont(size=18, weight="bold"),
        )
        self.label.grid(row=0, column=0, padx=32, pady=(28, 12))

        self.progress = ctk.CTkProgressBar(self, mode="indeterminate", width=220)
        self.progress.grid(row=1, column=0, padx=32, pady=(0, 28))

    def show(self, message: str) -> None:
        self.label.configure(text=message)
        self.place(relx=0.5, rely=0.5, anchor="center")
        self.lift()
        self.progress.start()

    def hide(self) -> None:
        self.progress.stop()
        self.place_forget()
