from __future__ import annotations

import queue
import threading
from tkinter import messagebox

import customtkinter as ctk

from app.core.config import Config
from app.services.edital_service import EditalService
from app.ui.dialogs.buscar_edital_dialog import BuscarEditalDialog
from app.ui.widgets.edital_tree import EditalTree
from app.ui.widgets.loading_overlay import LoadingOverlay


class MainWindow(ctk.CTk):
    def __init__(self, config: Config, edital_service: EditalService):
        super().__init__()
        self.config = config
        self.edital_service = edital_service
        self.sync_queue: queue.Queue[tuple[str, object]] = queue.Queue()
        self._sync_thread: threading.Thread | None = None

        self.title(self.config.app_name)
        self.geometry("1080x640")
        self.minsize(920, 560)

        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self._build_header()
        self._build_content()
        self.loading_overlay = LoadingOverlay(self.content_frame)

        self.refresh_editais()
        self.after(150, self._poll_sync_queue)

    def _build_header(self) -> None:
        header = ctk.CTkFrame(self, corner_radius=0)
        header.grid(row=0, column=0, sticky="ew")
        header.grid_columnconfigure(0, weight=1)

        title_frame = ctk.CTkFrame(header, fg_color="transparent")
        title_frame.grid(row=0, column=0, sticky="w", padx=24, pady=18)

        title = ctk.CTkLabel(
            title_frame,
            text="Editais sincronizados",
            font=ctk.CTkFont(size=24, weight="bold"),
        )
        title.grid(row=0, column=0, sticky="w")

        subtitle = ctk.CTkLabel(
            title_frame,
            text="MVP local com SQLite, SQLAlchemy e sincronizacao manual.",
            text_color="#5f6b7a",
        )
        subtitle.grid(row=1, column=0, sticky="w", pady=(4, 0))

        self.buscar_button = ctk.CTkButton(
            header,
            text="Buscar edital",
            command=self._open_buscar_dialog,
            width=160,
        )
        self.buscar_button.grid(row=0, column=1, padx=24, pady=24)

    def _build_content(self) -> None:
        self.content_frame = ctk.CTkFrame(self)
        self.content_frame.grid(row=1, column=0, sticky="nsew", padx=20, pady=(0, 20))
        self.content_frame.grid_rowconfigure(1, weight=1)
        self.content_frame.grid_columnconfigure(0, weight=1)

        info_frame = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        info_frame.grid(row=0, column=0, sticky="ew", padx=20, pady=(16, 0))
        info_frame.grid_columnconfigure(0, weight=1)

        self.status_label = ctk.CTkLabel(
            info_frame,
            text="Nenhuma sincronizacao em andamento.",
            anchor="w",
        )
        self.status_label.grid(row=0, column=0, sticky="w")

        self.tree = EditalTree(self.content_frame)
        self.tree.grid(row=1, column=0, sticky="nsew", padx=20, pady=16)
        self.tree.bind("<<TreeviewSelect>>", self._on_tree_select)

        self.selection_label = ctk.CTkLabel(
            self.content_frame,
            text="Selecione um edital para ver o resumo local.",
            anchor="w",
        )
        self.selection_label.grid(row=2, column=0, sticky="ew", padx=20, pady=(0, 16))

    def _open_buscar_dialog(self) -> None:
        BuscarEditalDialog(
            master=self,
            document_types=self.config.document_types,
            on_submit=self._start_sync,
        )

    def _start_sync(self, codigo: str, tipo_documento: str) -> None:
        if self._sync_thread and self._sync_thread.is_alive():
            messagebox.showinfo("Sincronizacao", "Ja existe uma sincronizacao em andamento.")
            return
        if not codigo.strip():
            messagebox.showwarning("Validacao", "Informe o codigo do edital.")
            return
        if not tipo_documento.strip():
            messagebox.showwarning("Validacao", "Informe o tipo de documento.")
            return

        self.buscar_button.configure(state="disabled")
        self.status_label.configure(text=f"Sincronizando edital {codigo} ({tipo_documento})...")
        self.loading_overlay.show("Sincronizando dados da API...")

        self._sync_thread = threading.Thread(
            target=self._sync_worker,
            args=(codigo, tipo_documento),
            daemon=True,
        )
        self._sync_thread.start()

    def _sync_worker(self, codigo: str, tipo_documento: str) -> None:
        try:
            result = self.edital_service.sync_edital(codigo, tipo_documento)
            self.sync_queue.put(("success", result))
        except Exception as exc:
            self.sync_queue.put(("error", str(exc)))

    def _poll_sync_queue(self) -> None:
        try:
            while True:
                status, payload = self.sync_queue.get_nowait()
                self._handle_sync_result(status, payload)
        except queue.Empty:
            pass
        finally:
            self.after(150, self._poll_sync_queue)

    def _handle_sync_result(self, status: str, payload: object) -> None:
        self.buscar_button.configure(state="normal")
        self.loading_overlay.hide()

        if status == "success":
            result = payload
            self.refresh_editais()
            self.status_label.configure(
                text=(
                    f"Edital sincronizado com sucesso: {result.codigo} | "
                    f"{result.modalidades} modalidades, {result.vagas} vagas, {result.anexos} anexos."
                )
            )
            messagebox.showinfo(
                "Sincronizacao concluida",
                f"Edital {result.codigo} atualizado no banco local.",
            )
            return

        self.status_label.configure(text="Falha na sincronizacao.")
        messagebox.showerror("Erro na sincronizacao", str(payload))

    def refresh_editais(self) -> None:
        summaries = self.edital_service.list_editais()
        self.tree.set_items(summaries)
        if not summaries:
            self.selection_label.configure(text="Nenhum edital sincronizado localmente.")

    def _on_tree_select(self, _event: object) -> None:
        selected = self.tree.get_selected_item()
        if selected is None:
            return

        synced_text = selected.synced_at.strftime("%d/%m/%Y %H:%M") if selected.synced_at else "nunca"
        self.selection_label.configure(
            text=(
                f"Codigo {selected.codigo} | Tipo {selected.tipo_documento} | "
                f"Modalidades {selected.modalidades_count} | Vagas {selected.vagas_count} | "
                f"Anexos {selected.anexos_count} | Ultima sync {synced_text}"
            )
        )
