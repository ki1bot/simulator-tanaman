import tkinter as tk
from tkinter import messagebox

from constants import (
    ACCENT,
    ACCENT_HOVER,
    PANEL_ALT,
    PANEL_BG,
    PLANT_TYPES,
    TEXT_DARK,
    TEXT_MUTED,
)
from exceptions import GameError


class ShopDialog(tk.Toplevel):
    def __init__(
        self,
        master,
        player,
        on_change,
    ):
        super().__init__(master)

        self.player = player
        self.on_change = on_change
        self.coins_var = tk.StringVar()

        self.title("Toko Bibit")
        self.configure(bg=PANEL_BG)
        self.resizable(False, False)
        self.transient(master)
        self.grab_set()

        self._build_ui()
        self._refresh_coins()

    def _build_ui(self):
        tk.Label(
            self,
            text="Toko Bibit",
            font=(
                "Arial",
                17,
                "bold",
            ),
            bg=PANEL_BG,
            fg=TEXT_DARK,
        ).pack(
            anchor="w",
            padx=18,
            pady=(18, 4),
        )

        tk.Label(
            self,
            textvariable=self.coins_var,
            font=(
                "Arial",
                11,
                "bold",
            ),
            bg=PANEL_BG,
            fg=TEXT_MUTED,
        ).pack(
            anchor="w",
            padx=18,
            pady=(0, 12),
        )

        body = tk.Frame(
            self,
            bg=PANEL_BG,
        )

        body.pack(
            fill="both",
            expand=True,
            padx=18,
            pady=(0, 12),
        )

        for row, (
            kind,
            info,
        ) in enumerate(
            PLANT_TYPES.items()
        ):
            card = tk.Frame(
                body,
                bg=PANEL_ALT,
            )

            card.grid(
                row=row,
                column=0,
                sticky="ew",
                pady=4,
            )

            tk.Label(
                card,
                text=info["name"],
                width=16,
                anchor="w",
                font=(
                    "Arial",
                    10,
                    "bold",
                ),
                bg=PANEL_ALT,
                fg=TEXT_DARK,
                padx=10,
                pady=9,
            ).pack(
                side="left"
            )

            tk.Label(
                card,
                text=(
                    f"Harga "
                    f"{info['seed_price']} | "
                    f"Panen "
                    f"{info['harvest_value']} | "
                    f"{info['grow_days']} hari"
                ),
                width=32,
                anchor="w",
                font=(
                    "Arial",
                    10,
                ),
                bg=PANEL_ALT,
                fg=TEXT_MUTED,
            ).pack(
                side="left",
                padx=(0, 8),
            )

            tk.Button(
                card,
                text="Beli 1",
                font=(
                    "Arial",
                    9,
                    "bold",
                ),
                bg="#e6d1ab",
                fg=TEXT_DARK,
                activebackground=(
                    "#d8bd8e"
                ),
                relief="flat",
                command=(
                    lambda k=kind:
                    self._buy(k, 1)
                ),
            ).pack(
                side="left",
                padx=3,
            )

            tk.Button(
                card,
                text="Beli 3",
                font=(
                    "Arial",
                    9,
                    "bold",
                ),
                bg="#ddc18c",
                fg=TEXT_DARK,
                activebackground=(
                    "#cfad70"
                ),
                relief="flat",
                command=(
                    lambda k=kind:
                    self._buy(k, 3)
                ),
            ).pack(
                side="left",
                padx=(3, 8),
            )

        tk.Button(
            self,
            text="Tutup",
            font=(
                "Arial",
                10,
                "bold",
            ),
            bg=ACCENT,
            fg="white",
            activebackground=(
                ACCENT_HOVER
            ),
            relief="flat",
            padx=16,
            pady=8,
            command=self.destroy,
        ).pack(
            anchor="e",
            padx=18,
            pady=(0, 18),
        )

    def _refresh_coins(self):
        self.coins_var.set(
            f"Koin Anda: "
            f"{self.player.coins}"
        )

    def _buy(
        self,
        kind,
        quantity,
    ):
        try:
            self.player.buy_seed(
                kind,
                quantity,
            )

        except (
            GameError,
            ValueError,
        ) as exc:
            messagebox.showwarning(
                "Pembelian Gagal",
                str(exc),
                parent=self,
            )
            return

        self._refresh_coins()

        self.on_change(
            kind,
            quantity,
        )