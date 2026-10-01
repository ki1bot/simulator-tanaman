import tkinter as tk
from random import Random
from tkinter import (
    messagebox,
    simpledialog,
    ttk,
)

from constants import (
    ACCENT,
    ACCENT_HOVER,
    APP_TITLE,
    BG_MAIN,
    BUTTON_BG,
    BUTTON_HOVER,
    CANVAS_HEIGHT,
    CANVAS_WIDTH,
    MAX_ENERGY,
    PANEL_ALT,
    PANEL_BG,
    PLANT_TYPES,
    SAVE_FILE,
    SAVE_VERSION,
    SUCCESS,
    SUCCESS_HOVER,
    TEXT_DARK,
    TEXT_MUTED,
    WARNING,
    WARNING_HOVER,
)
from drawing import (
    draw_garden,
    pixel_to_plot,
)
from exceptions import (
    GameError,
    SaveGameError,
)
from garden import Garden
from player import Player
from save_manager import SaveManager
from shop_dialog import ShopDialog


class GardenApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title(APP_TITLE)
        self.geometry("1120x720")
        self.minsize(
            1040,
            680,
        )
        self.configure(
            bg=BG_MAIN
        )

        self.player = None
        self.garden = None
        self.day = 1
        self.selected_plot = None
        self.rng = Random()

        self.save_manager = (
            SaveManager(
                SAVE_FILE
            )
        )

        self.log_lines = []

        self.display_to_key = {
            info["name"]: key
            for key, info in (
                PLANT_TYPES.items()
            )
        }

        self.seed_var = (
            tk.StringVar(
                value=next(
                    iter(
                        self.display_to_key
                    )
                )
            )
        )

        self.name_var = tk.StringVar(
            value="-"
        )

        self.day_var = tk.StringVar(
            value="-"
        )

        self.coins_var = tk.StringVar(
            value="-"
        )

        self.energy_var = tk.StringVar(
            value="-"
        )

        self.inventory_var = (
            tk.StringVar(
                value="-"
            )
        )

        self.plot_info_var = (
            tk.StringVar(
                value=(
                    "Klik salah satu "
                    "petak taman."
                )
            )
        )

        self._build_ui()

        self.protocol(
            "WM_DELETE_WINDOW",
            self.on_close,
        )

        self.after(
            50,
            self._startup_flow,
        )

    def _build_ui(self):
        header = tk.Frame(
            self,
            bg=BG_MAIN,
        )

        header.pack(
            fill="x",
            padx=18,
            pady=(14, 8),
        )

        tk.Label(
            header,
            text="Simulator Taman",
            font=(
                "Arial",
                23,
                "bold",
            ),
            bg=BG_MAIN,
            fg=TEXT_DARK,
        ).pack()

        tk.Label(
            header,
            text=(
                "Tanam, rawat, dan "
                "panen tanaman virtual "
                "dari taman 3×3."
            ),
            font=(
                "Arial",
                10,
            ),
            bg=BG_MAIN,
            fg=TEXT_MUTED,
        ).pack(
            pady=(3, 0)
        )

        body = tk.Frame(
            self,
            bg=BG_MAIN,
        )

        body.pack(
            fill="both",
            expand=True,
            padx=16,
            pady=(0, 14),
        )

        left = tk.Frame(
            body,
            bg=PANEL_BG,
        )

        left.pack(
            side="left",
            fill="y",
            padx=(0, 12),
        )

        right = tk.Frame(
            body,
            bg=PANEL_BG,
        )

        right.pack(
            side="right",
            fill="both",
            expand=True,
        )

        tk.Label(
            left,
            text="Taman",
            font=(
                "Arial",
                15,
                "bold",
            ),
            bg=PANEL_BG,
            fg=TEXT_DARK,
        ).pack(
            pady=(14, 4)
        )

        self.canvas = tk.Canvas(
            left,
            width=CANVAS_WIDTH,
            height=CANVAS_HEIGHT,
            bg=PANEL_BG,
            highlightthickness=0,
            cursor="hand2",
        )

        self.canvas.pack(
            padx=14,
            pady=(0, 14),
        )

        self.canvas.bind(
            "<Button-1>",
            self.on_canvas_click,
        )

        status = tk.Frame(
            right,
            bg=PANEL_BG,
        )

        status.pack(
            fill="x",
            padx=14,
            pady=(14, 8),
        )

        tk.Label(
            status,
            text="Status Pemain",
            font=(
                "Arial",
                15,
                "bold",
            ),
            bg=PANEL_BG,
            fg=TEXT_DARK,
        ).grid(
            row=0,
            column=0,
            columnspan=4,
            sticky="w",
            pady=(0, 6),
        )

        self._status_item(
            status,
            "Nama",
            self.name_var,
            1,
            0,
        )

        self._status_item(
            status,
            "Hari",
            self.day_var,
            1,
            1,
        )

        self._status_item(
            status,
            "Koin",
            self.coins_var,
            2,
            0,
        )

        self._status_item(
            status,
            "Energi",
            self.energy_var,
            2,
            1,
        )

        status.grid_columnconfigure(
            0,
            weight=1,
        )

        status.grid_columnconfigure(
            1,
            weight=1,
        )

        controls = tk.Frame(
            right,
            bg=PANEL_BG,
        )

        controls.pack(
            fill="x",
            padx=14,
            pady=(2, 8),
        )

        tk.Label(
            controls,
            text="Pilih Bibit",
            font=(
                "Arial",
                11,
                "bold",
            ),
            bg=PANEL_BG,
            fg=TEXT_DARK,
        ).pack(
            anchor="w"
        )

        self.seed_combo = (
            ttk.Combobox(
                controls,
                textvariable=(
                    self.seed_var
                ),
                state="readonly",
                values=list(
                    self.display_to_key.keys()
                ),
                font=(
                    "Arial",
                    10,
                ),
            )
        )

        self.seed_combo.pack(
            fill="x",
            pady=(4, 8),
        )

        action_grid = tk.Frame(
            controls,
            bg=PANEL_BG,
        )

        action_grid.pack(
            fill="x"
        )

        actions = (
            (
                "Tanam",
                "plant",
                0,
                0,
            ),
            (
                "Siram",
                "water",
                0,
                1,
            ),
            (
                "Rawat",
                "care",
                1,
                0,
            ),
            (
                "Panen",
                "harvest",
                1,
                1,
            ),
            (
                "Bersihkan",
                "clear",
                2,
                0,
            ),
        )

        for (
            text,
            action,
            row,
            col,
        ) in actions:
            tk.Button(
                action_grid,
                text=text,
                font=(
                    "Arial",
                    10,
                    "bold",
                ),
                bg=BUTTON_BG,
                fg=TEXT_DARK,
                activebackground=(
                    BUTTON_HOVER
                ),
                relief="flat",
                pady=8,
                command=(
                    lambda a=action:
                    self.perform_action(a)
                ),
            ).grid(
                row=row,
                column=col,
                sticky="ew",
                padx=4,
                pady=4,
            )

        tk.Button(
            action_grid,
            text="Toko Bibit",
            font=(
                "Arial",
                10,
                "bold",
            ),
            bg="#ddc38f",
            fg=TEXT_DARK,
            activebackground="#cfae71",
            relief="flat",
            pady=8,
            command=self.open_shop,
        ).grid(
            row=2,
            column=1,
            sticky="ew",
            padx=4,
            pady=4,
        )

        action_grid.grid_columnconfigure(
            0,
            weight=1,
        )

        action_grid.grid_columnconfigure(
            1,
            weight=1,
        )

        middle = tk.Frame(
            right,
            bg=PANEL_BG,
        )

        middle.pack(
            fill="x",
            padx=14,
            pady=(2, 8),
        )

        info_panel = tk.Frame(
            middle,
            bg=PANEL_ALT,
        )

        info_panel.pack(
            side="left",
            fill="both",
            expand=True,
            padx=(0, 5),
        )

        tk.Label(
            info_panel,
            text="Info Petak",
            font=(
                "Arial",
                11,
                "bold",
            ),
            bg=PANEL_ALT,
            fg=TEXT_DARK,
        ).pack(
            anchor="w",
            padx=10,
            pady=(8, 2),
        )

        tk.Label(
            info_panel,
            textvariable=(
                self.plot_info_var
            ),
            justify="left",
            anchor="nw",
            wraplength=245,
            font=(
                "Arial",
                9,
            ),
            bg=PANEL_ALT,
            fg=TEXT_MUTED,
        ).pack(
            fill="both",
            expand=True,
            padx=10,
            pady=(0, 8),
        )

        inventory_panel = (
            tk.Frame(
                middle,
                bg=PANEL_ALT,
            )
        )

        inventory_panel.pack(
            side="left",
            fill="both",
            expand=True,
            padx=(5, 0),
        )

        tk.Label(
            inventory_panel,
            text="Inventaris Bibit",
            font=(
                "Arial",
                11,
                "bold",
            ),
            bg=PANEL_ALT,
            fg=TEXT_DARK,
        ).pack(
            anchor="w",
            padx=10,
            pady=(8, 2),
        )

        tk.Label(
            inventory_panel,
            textvariable=(
                self.inventory_var
            ),
            justify="left",
            anchor="nw",
            font=(
                "Arial",
                9,
            ),
            bg=PANEL_ALT,
            fg=TEXT_MUTED,
        ).pack(
            fill="both",
            expand=True,
            padx=10,
            pady=(0, 8),
        )

        log_frame = tk.Frame(
            right,
            bg=PANEL_BG,
        )

        log_frame.pack(
            fill="both",
            expand=True,
            padx=14,
            pady=(0, 8),
        )

        tk.Label(
            log_frame,
            text="Kegiatan",
            font=(
                "Arial",
                11,
                "bold",
            ),
            bg=PANEL_BG,
            fg=TEXT_DARK,
        ).pack(
            anchor="w"
        )

        self.log_text = tk.Text(
            log_frame,
            height=7,
            wrap="word",
            font=(
                "Consolas",
                9,
            ),
            bg="#fbf6ec",
            fg=TEXT_DARK,
            relief="flat",
            padx=8,
            pady=8,
        )

        self.log_text.pack(
            fill="both",
            expand=True,
            pady=(4, 0),
        )

        self.log_text.config(
            state="disabled"
        )

        bottom = tk.Frame(
            right,
            bg=PANEL_BG,
        )

        bottom.pack(
            fill="x",
            padx=14,
            pady=(0, 14),
        )

        tk.Button(
            bottom,
            text="Hari Berikutnya",
            font=(
                "Arial",
                10,
                "bold",
            ),
            bg=SUCCESS,
            fg="white",
            activebackground=(
                SUCCESS_HOVER
            ),
            relief="flat",
            pady=8,
            command=self.end_day,
        ).pack(
            side="left",
            fill="x",
            expand=True,
            padx=(0, 4),
        )

        tk.Button(
            bottom,
            text="Simpan",
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
            pady=8,
            command=self.save_game,
        ).pack(
            side="left",
            fill="x",
            expand=True,
            padx=4,
        )

        tk.Button(
            bottom,
            text="Muat",
            font=(
                "Arial",
                10,
                "bold",
            ),
            bg="#8b7664",
            fg="white",
            activebackground="#756252",
            relief="flat",
            pady=8,
            command=self.load_game,
        ).pack(
            side="left",
            fill="x",
            expand=True,
            padx=4,
        )

        tk.Button(
            bottom,
            text="Game Baru",
            font=(
                "Arial",
                10,
                "bold",
            ),
            bg=WARNING,
            fg="white",
            activebackground=(
                WARNING_HOVER
            ),
            relief="flat",
            pady=8,
            command=(
                self.start_new_game
            ),
        ).pack(
            side="left",
            fill="x",
            expand=True,
            padx=(4, 0),
        )

    def _status_item(
        self,
        parent,
        label,
        variable,
        row,
        column,
    ):
        box = tk.Frame(
            parent,
            bg=PANEL_ALT,
        )

        box.grid(
            row=row,
            column=column,
            sticky="ew",
            padx=4,
            pady=3,
        )

        tk.Label(
            box,
            text=f"{label}:",
            font=(
                "Arial",
                9,
                "bold",
            ),
            bg=PANEL_ALT,
            fg=TEXT_DARK,
        ).pack(
            side="left",
            padx=(8, 4),
            pady=6,
        )

        tk.Label(
            box,
            textvariable=variable,
            font=(
                "Arial",
                9,
            ),
            bg=PANEL_ALT,
            fg=TEXT_MUTED,
        ).pack(
            side="left",
            pady=6,
        )

    def _startup_flow(self):
        if self.save_manager.exists():
            use_save = (
                messagebox.askyesno(
                    "Muat Permainan",
                    (
                        "Ditemukan save game. "
                        "Lanjutkan permainan "
                        "sebelumnya?"
                    ),
                    parent=self,
                )
            )

            if (
                use_save
                and self._load_state(
                    show_message=False
                )
            ):
                self.log(
                    "Save game berhasil "
                    "dimuat."
                )
                return

        self.start_new_game(
            show_message=False,
            ask_confirmation=False,
        )

    def start_new_game(
        self,
        show_message=True,
        ask_confirmation=True,
    ):
        if (
            ask_confirmation
            and self.player is not None
        ):
            proceed = (
                messagebox.askyesno(
                    "Game Baru",
                    (
                        "Memulai game baru "
                        "akan mengganti progres "
                        "yang sedang aktif. "
                        "Lanjutkan?"
                    ),
                    parent=self,
                )
            )

            if not proceed:
                return

        name = simpledialog.askstring(
            "Nama Pemain",
            "Masukkan nama pemain:",
            parent=self,
        )

        if name is None:
            if self.player is not None:
                return

            name = "Pemain"

        name = (
            name.strip()
            or "Pemain"
        )

        self.player = Player(
            name=name
        )

        self.garden = Garden()
        self.day = 1
        self.selected_plot = None

        self.clear_log()

        self.log(
            f"Permainan baru dimulai. "
            f"Selamat datang, "
            f"{self.player.name}."
        )

        self.refresh_ui()

        if show_message:
            messagebox.showinfo(
                "Game Baru",
                (
                    "Permainan baru "
                    "berhasil dimulai."
                ),
                parent=self,
            )

    def on_canvas_click(
        self,
        event,
    ):
        if not self._game_ready():
            return

        position = pixel_to_plot(
            event.x,
            event.y,
        )

        if position is None:
            return

        self.selected_plot = position
        self.refresh_ui()

    def perform_action(
        self,
        action,
    ):
        if not self._game_ready():
            return

        if self.selected_plot is None:
            messagebox.showwarning(
                "Pilih Petak",
                (
                    "Pilih salah satu "
                    "petak taman "
                    "terlebih dahulu."
                ),
                parent=self,
            )
            return

        try:
            if action == "plant":
                self._plant_selected()

            elif action == "water":
                self._water_selected()

            elif action == "care":
                self._care_selected()

            elif action == "harvest":
                self._harvest_selected()

            elif action == "clear":
                self._clear_selected()

        except (
            GameError,
            ValueError,
            KeyError,
        ) as exc:
            messagebox.showwarning(
                "Aksi Gagal",
                str(exc),
                parent=self,
            )

            self.log(
                f"Gagal: {exc}"
            )

        self.refresh_ui()

    def _plant_selected(self):
        self.player.require_energy()

        kind = self.display_to_key[
            self.seed_var.get()
        ]

        plot = self.garden.get_plot(
            self.selected_plot
        )

        if not plot.is_empty:
            raise GameError(
                f"Petak "
                f"{self.selected_plot} "
                f"sudah terisi."
            )

        self.player.use_seed(
            kind
        )

        try:
            plant = (
                self.garden.plant_seed(
                    self.selected_plot,
                    kind,
                )
            )

        except Exception:
            self.player.seeds[kind] = (
                self.player.seed_count(
                    kind
                )
                + 1
            )
            raise

        self.player.consume_energy()

        self.log(
            f"{plant.name} ditanam "
            f"di petak "
            f"{self.selected_plot}."
        )

    def _water_selected(self):
        self.player.require_energy()

        plant = (
            self.garden.water_plot(
                self.selected_plot
            )
        )

        self.player.consume_energy()

        self.log(
            f"{plant.name} di petak "
            f"{self.selected_plot} "
            f"disiram."
        )

    def _care_selected(self):
        self.player.require_energy()

        plant = (
            self.garden.care_plot(
                self.selected_plot
            )
        )

        self.player.consume_energy()

        self.log(
            f"{plant.name} di petak "
            f"{self.selected_plot} "
            f"dirawat."
        )

    def _harvest_selected(self):
        self.player.require_energy()

        plant = (
            self.garden.harvest_plot(
                self.selected_plot
            )
        )

        self.player.consume_energy()

        self.player.receive_harvest(
            plant.harvest_value
        )

        self.log(
            f"{plant.name} dipanen "
            f"dari petak "
            f"{self.selected_plot}. "
            f"+{plant.harvest_value} "
            f"koin."
        )

    def _clear_selected(self):
        self.player.require_energy()

        name = (
            self.garden.clear_dead_plot(
                self.selected_plot
            )
        )

        self.player.consume_energy()

        self.log(
            f"Tanaman mati {name} "
            f"dibersihkan dari petak "
            f"{self.selected_plot}."
        )

    def end_day(self):
        if not self._game_ready():
            return

        proceed = (
            messagebox.askyesno(
                "Hari Berikutnya",
                (
                    f"Akhiri hari "
                    f"ke-{self.day} dan "
                    f"lanjut ke hari "
                    f"berikutnya?"
                ),
                parent=self,
            )
        )

        if not proceed:
            return

        events = (
            self.garden.advance_day(
                self.rng
            )
        )

        self.day += 1

        self.player.reset_energy()

        if self.rng.random() < 0.15:
            kind = self.rng.choice(
                list(
                    PLANT_TYPES.keys()
                )
            )

            self.player.seeds[kind] = (
                self.player.seed_count(
                    kind
                )
                + 1
            )

            events.append(
                f"Bonus harian: "
                f"mendapat 1 bibit "
                f"{PLANT_TYPES[kind]['name']}."
            )

        self.log(
            f"Memasuki hari "
            f"ke-{self.day}. "
            f"Energi dipulihkan "
            f"menjadi {MAX_ENERGY}."
        )

        if events:
            for event in events:
                self.log(event)
        else:
            self.log(
                "Tidak ada peristiwa "
                "khusus hari ini."
            )

        self.refresh_ui()

    def open_shop(self):
        if not self._game_ready():
            return

        ShopDialog(
            self,
            self.player,
            self._after_purchase,
        )

    def _after_purchase(
        self,
        kind,
        quantity,
    ):
        self.log(
            f"Membeli {quantity} "
            f"bibit "
            f"{PLANT_TYPES[kind]['name']}."
        )

        self.refresh_ui()

    def save_game(self):
        if not self._game_ready():
            return False

        return self._save_state(
            show_message=True
        )

    def _save_state(
        self,
        show_message=False,
    ):
        data = {
            "version": SAVE_VERSION,
            "day": self.day,
            "player": (
                self.player.to_dict()
            ),
            "garden": (
                self.garden.to_dict()
            ),
        }

        try:
            self.save_manager.save(
                data
            )

        except SaveGameError as exc:
            messagebox.showerror(
                "Gagal Menyimpan",
                str(exc),
                parent=self,
            )

            return False

        self.log(
            "Permainan berhasil "
            "disimpan."
        )

        if show_message:
            messagebox.showinfo(
                "Simpan",
                (
                    "Permainan berhasil "
                    "disimpan."
                ),
                parent=self,
            )

        return True

    def load_game(self):
        if self.player is not None:
            proceed = (
                messagebox.askyesno(
                    "Muat Permainan",
                    (
                        "Progres yang sedang "
                        "aktif akan diganti "
                        "dengan save game. "
                        "Lanjutkan?"
                    ),
                    parent=self,
                )
            )

            if not proceed:
                return

        self._load_state(
            show_message=True
        )

    def _load_state(
        self,
        show_message=False,
    ):
        try:
            data = (
                self.save_manager.load()
            )

            version = int(
                data.get(
                    "version",
                    0,
                )
            )

            if version != SAVE_VERSION:
                raise SaveGameError(
                    f"Versi save game "
                    f"{version} tidak "
                    f"didukung. Versi "
                    f"aplikasi saat ini "
                    f"adalah "
                    f"{SAVE_VERSION}."
                )

            player = (
                Player.from_dict(
                    data["player"]
                )
            )

            garden = (
                Garden.from_dict(
                    data["garden"]
                )
            )

            day = max(
                1,
                int(
                    data.get(
                        "day",
                        1,
                    )
                ),
            )

        except SaveGameError as exc:
            messagebox.showerror(
                "Gagal Memuat",
                str(exc),
                parent=self,
            )

            return False

        except (
            KeyError,
            TypeError,
            ValueError,
        ) as exc:
            messagebox.showerror(
                "Gagal Memuat",
                (
                    "Data save game "
                    "rusak atau tidak "
                    f"lengkap: {exc}"
                ),
                parent=self,
            )

            return False

        self.player = player
        self.garden = garden
        self.day = day
        self.selected_plot = None

        self.refresh_ui()

        self.log(
            "Permainan berhasil "
            "dimuat."
        )

        if show_message:
            messagebox.showinfo(
                "Muat",
                (
                    "Permainan berhasil "
                    "dimuat."
                ),
                parent=self,
            )

        return True

    def refresh_ui(self):
        if not self._game_ready(
            show_error=False
        ):
            return

        self.name_var.set(
            self.player.name
        )

        self.day_var.set(
            str(self.day)
        )

        self.coins_var.set(
            str(self.player.coins)
        )

        self.energy_var.set(
            f"{self.player.energy}/"
            f"{MAX_ENERGY}"
        )

        self.inventory_var.set(
            self._inventory_text()
        )

        self.plot_info_var.set(
            self._plot_info_text()
        )

        draw_garden(
            self.canvas,
            self.garden,
            self.selected_plot,
        )

    def _inventory_text(self):
        return "\n".join(
            (
                f"{info['name']}: "
                f"{self.player.seed_count(kind)}"
            )
            for kind, info in (
                PLANT_TYPES.items()
            )
        )

    def _plot_info_text(self):
        if self.selected_plot is None:
            return (
                "Klik salah satu petak "
                "untuk memilihnya."
            )

        plot = self.garden.get_plot(
            self.selected_plot
        )

        if plot.is_empty:
            return (
                f"Petak "
                f"{plot.position}\n"
                f"Status: Kosong\n"
                f"Siap ditanami."
            )

        plant = plot.plant

        watered = (
            "Ya"
            if plant.watered_today
            else "Belum"
        )

        cared = (
            "Ya"
            if plant.cared_today
            else "Belum"
        )

        return (
            f"Petak "
            f"{plot.position}\n"
            f"Tanaman: "
            f"{plant.name}\n"
            f"Tahap: "
            f"{plant.stage_name}\n"
            f"Pertumbuhan: "
            f"{plant.growth}/"
            f"{plant.grow_days}\n"
            f"Kesehatan: "
            f"{plant.health}/"
            f"{plant.max_health}\n"
            f"Disiram: "
            f"{watered}\n"
            f"Dirawat: "
            f"{cared}"
        )

    def log(self, text):
        self.log_lines.append(
            text
        )

        self.log_lines = (
            self.log_lines[-80:]
        )

        self.log_text.config(
            state="normal"
        )

        self.log_text.delete(
            "1.0",
            "end",
        )

        self.log_text.insert(
            "end",
            "\n".join(
                self.log_lines
            ),
        )

        self.log_text.see(
            "end"
        )

        self.log_text.config(
            state="disabled"
        )

    def clear_log(self):
        self.log_lines = []

        self.log_text.config(
            state="normal"
        )

        self.log_text.delete(
            "1.0",
            "end",
        )

        self.log_text.config(
            state="disabled"
        )

    def _game_ready(
        self,
        show_error=True,
    ):
        ready = (
            self.player is not None
            and self.garden is not None
        )

        if (
            not ready
            and show_error
        ):
            messagebox.showwarning(
                "Game Belum Siap",
                (
                    "Mulai game baru "
                    "terlebih dahulu."
                ),
                parent=self,
            )

        return ready

    def on_close(self):
        if self.player is None:
            self.destroy()
            return

        choice = (
            messagebox.askyesnocancel(
                "Keluar",
                (
                    "Simpan permainan "
                    "sebelum keluar?"
                ),
                parent=self,
            )
        )

        if choice is None:
            return

        if (
            choice
            and not self._save_state(
                show_message=False
            )
        ):
            return

        self.destroy()