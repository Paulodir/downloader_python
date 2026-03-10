from __future__ import annotations

from tkinter import ttk

import customtkinter as ctk

from app.services.edital_service import EditalSummary


class EditalTree(ctk.CTkFrame):
    def __init__(self, master: ctk.CTkFrame):
        super().__init__(master)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self._items_by_row_id: dict[str, EditalSummary] = {}

        columns = ("codigo", "titulo", "tipo", "modalidades", "vagas", "anexos", "sync")
        self.tree = ttk.Treeview(self, columns=columns, show="headings", height=18)

        headings = {
            "codigo": ("Codigo", 120),
            "titulo": ("Titulo", 320),
            "tipo": ("Tipo", 120),
            "modalidades": ("Modalidades", 100),
            "vagas": ("Vagas", 80),
            "anexos": ("Anexos", 80),
            "sync": ("Ultima sync", 150),
        }
        for column, (text, width) in headings.items():
            self.tree.heading(column, text=text)
            self.tree.column(column, width=width, anchor="w")

        scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")

    def bind(self, sequence: str | None = None, callback=None, add: str | None = None) -> None:
        self.tree.bind(sequence, callback, add)

    def set_items(self, items: list[EditalSummary]) -> None:
        self._items_by_row_id.clear()
        for row_id in self.tree.get_children():
            self.tree.delete(row_id)

        for item in items:
            synced_text = item.synced_at.strftime("%d/%m/%Y %H:%M") if item.synced_at else "-"
            row_id = self.tree.insert(
                "",
                "end",
                values=(
                    item.codigo,
                    item.titulo,
                    item.tipo_documento,
                    item.modalidades_count,
                    item.vagas_count,
                    item.anexos_count,
                    synced_text,
                ),
            )
            self._items_by_row_id[row_id] = item

    def get_selected_item(self) -> EditalSummary | None:
        selection = self.tree.selection()
        if not selection:
            return None
        return self._items_by_row_id.get(selection[0])
