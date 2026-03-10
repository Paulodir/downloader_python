from __future__ import annotations

from collections.abc import Callable, Sequence
from tkinter import messagebox

import customtkinter as ctk


class BuscarEditalDialog(ctk.CTkToplevel):
    def __init__(
        self,
        master: ctk.CTk,
        document_types: Sequence[str],
        on_submit: Callable[[str, str], None],
    ):
        super().__init__(master)
        self.document_types = tuple(document_types)
        self.on_submit = on_submit

        self.title("Buscar edital")
        self.geometry("420x220")
        self.resizable(False, False)
        self.transient(master)
        self.grab_set()

        self.grid_columnconfigure(0, weight=1)

        container = ctk.CTkFrame(self)
        container.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
        container.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            container,
            text="Codigo do edital",
            anchor="w",
        ).grid(row=0, column=0, sticky="ew", padx=16, pady=(16, 6))

        self.codigo_entry = ctk.CTkEntry(container, placeholder_text="Ex.: 2026-001")
        self.codigo_entry.grid(row=1, column=0, sticky="ew", padx=16)

        ctk.CTkLabel(
            container,
            text="Tipo de documento",
            anchor="w",
        ).grid(row=2, column=0, sticky="ew", padx=16, pady=(16, 6))

        self.tipo_option = ctk.CTkOptionMenu(
            container,
            values=list(self.document_types),
        )
        self.tipo_option.grid(row=3, column=0, sticky="ew", padx=16)

        action_frame = ctk.CTkFrame(container, fg_color="transparent")
        action_frame.grid(row=4, column=0, sticky="e", padx=16, pady=16)

        ctk.CTkButton(
            action_frame,
            text="Cancelar",
            fg_color="transparent",
            border_width=1,
            text_color=("gray10", "gray90"),
            command=self.destroy,
            width=110,
        ).grid(row=0, column=0, padx=(0, 8))

        ctk.CTkButton(
            action_frame,
            text="Sincronizar",
            command=self._submit,
            width=110,
        ).grid(row=0, column=1)

        self.codigo_entry.focus()

    def _submit(self) -> None:
        codigo = self.codigo_entry.get().strip()
        tipo_documento = self.tipo_option.get().strip()
        if not codigo:
            messagebox.showwarning("Validacao", "Informe o codigo do edital.", parent=self)
            return
        self.on_submit(codigo, tipo_documento)
        self.destroy()
