from __future__ import annotations

from tkinter import ttk

import customtkinter as ctk


class AnexoTable(ctk.CTkFrame):
    def __init__(self, master: ctk.CTkFrame):
        super().__init__(master)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.table = ttk.Treeview(
            self,
            columns=("nome", "tipo", "url"),
            show="headings",
            height=8,
        )
        self.table.heading("nome", text="Nome")
        self.table.heading("tipo", text="Tipo")
        self.table.heading("url", text="URL")

        self.table.column("nome", width=220, anchor="w")
        self.table.column("tipo", width=120, anchor="w")
        self.table.column("url", width=320, anchor="w")

        scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.table.yview)
        self.table.configure(yscrollcommand=scrollbar.set)

        self.table.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")

    def set_items(self, anexos: list[dict[str, str]]) -> None:
        for row_id in self.table.get_children():
            self.table.delete(row_id)
        for anexo in anexos:
            self.table.insert(
                "",
                "end",
                values=(
                    anexo.get("nome", ""),
                    anexo.get("tipo_documento", ""),
                    anexo.get("url", ""),
                ),
            )
