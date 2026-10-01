import tkinter as tk
from random import Random
from tkinter import messagebox, simpledialog, ttk

from constants import (
    ACCENT,
    APP_TITLE,
    BG_MAIN,
    CANVAS_HEIGHT,
    CANVAS_WIDTH,
    MAX_ENERGY,
    PANEL_BG,
    PLANT_TYPES,
    SAVE_FILE,
    SAVE_VERSION,
    SUCCESS,
    TEXT_DARK,
    TEXT_LIGHT,
    WARNING,
)
from drawing import draw_garden, pixel_to_plot
from exceptions import GameError, SaveGameError
from garden import Garden
from player import Player
from save_manager import SaveManager


class GardenApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title(APP_TITLE)
        self.geometry("1180x760")
        self.minsize(1120, 740)
        self.configure(bg=BG_MAIN)

        self.save_manager = SaveManager(SAVE_FILE)
        self.rng = Random()

        self.player = None
        self.garden = None
        self.day = 1

        self.selected_tool = "plant"
        self.selected_plot = None

        self.display_to_key = {
            PLANT_TYPES[key]["name"]: key
            for key in PLANT_TYPES
        }
        self.key_to_display = {
            key: PLANT_TYPES[key]["name"]
            for key in PLANT_TYPES
        }

        first_seed_display = self.key_to_display[list(PLANT_TYPES.keys())[0]]
        self.seed_var = tk.StringVar(value=first_seed_display)

        self.name_var = tk.StringVar(value="-")
        self.day_var = tk.StringVar(value="-")
        self.coins_var = tk.StringVar(value="-")
        self.energy_var = tk.StringVar(value="-")
        self.tool_var = tk.StringVar(value="Mode: Tanam")
        self.inventory_var = tk.StringVar(value="-")
        self.plot_info_var = tk.StringVar(value="Klik petak taman untuk berinteraksi.")

        self.tool_buttons = {}
        self.log_lines = []

        self._build_ui()
        self._startup_flow()

        self.protocol("WM_DELETE_WINDOW", self.on_close)

    # UI BUILD
    def _build_ui(self):
        title_label = tk.Label(
            self,
            text="Simulator Taman",
            font=("Arial", 24, "bold"),
            bg=BG_MAIN,
            fg=TEXT_DARK,
        )
        title_label.pack(pady=(18, 6))

        subtitle = tk.Label(
            self,
            text="Game UI Python dengan taman 3×3, tanam, siram, rawat, panen, dan simpan progres.",
            font=("Arial", 11),
            bg=BG_MAIN,
            fg=TEXT_LIGHT,
        )
        subtitle.pack(pady=(0, 14))

        root_frame = tk.Frame(self, bg=BG_MAIN)
        root_frame.pack(fill="both", expand=True, padx=16, pady=10)

        left_panel = tk.Frame(root_frame, bg=PANEL_BG, bd=0, highlightthickness=0)
        left_panel.pack(side="left", fill="both", expand=False, padx=(0, 12))

        right_panel = tk.Frame(root_frame, bg=PANEL_BG, bd=0, highlightthickness=0)
        right_panel.pack(side="right", fill="both", expand=True)

        # Canvas taman
        garden_title = tk.Label(
            left_panel,
            text="Taman",
            font=("Arial", 16, "bold"),
            bg=PANEL_BG,
            fg=TEXT_DARK,
        )
        garden_title.pack(pady=(16, 8))

        self.canvas = tk.Canvas(
            left_panel,
            width=CANVAS_WIDTH,
            height=CANVAS_HEIGHT,
            bg=PANEL_BG,
            highlightthickness=0,
        )
        self.canvas.pack(padx=16, pady=(0, 16))
        self.canvas.bind("<Button-1>", self.on_canvas_click)

        # Panel kanan
        info_frame = tk.Frame(right_panel, bg=PANEL_BG)
        info_frame.pack(fill="x", padx=16, pady=(16, 10))

        tk.Label(
            info_frame,
            text="Status Pemain",
            font=("Arial", 16, "bold"),
            bg=PANEL_BG,
            fg=TEXT_DARK,
        ).pack(anchor="w")

        self._stat_row(info_frame, "Nama", self.name_var)
        self._stat_row(info_frame, "Hari", self.day_var)
        self._stat_row(info_frame, "Koin", self.coins_var)
        self._stat_row(info_frame, "Energi", self.energy_var)
        self._stat_row(info_frame, "Mode", self.tool_var)

        seed_frame = tk.Frame(right_panel, bg=PANEL_BG)
        seed_frame.pack(fill="x", padx=16, pady=(0, 10))

        tk.Label(
            seed_frame,
            text="Bibit untuk Mode Tanam",
            font=("Arial", 13, "bold"),
            bg=PANEL_BG,
            fg=TEXT_DARK,
        ).pack(anchor="w", pady=(0, 6))

        self.seed_combo = ttk.Combobox(
            seed_frame,
            textvariable=self.seed_var,
            state="readonly",
            values=list(self.display_to_key.keys()),
            font=("Arial", 11),
        )
        self.seed_combo.pack(fill="x")

        action_frame = tk.Frame(right_panel, bg=PANEL_BG)
        action_frame.pack(fill="x", padx=16, pady=(6, 10))

        tk.Label(
            action_frame,
            text="Pilih Aksi",
            font=("Arial", 13, "bold"),
            bg=PANEL_BG,
            fg=TEXT_DARK,
        ).grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 8))

        self._make_tool_button(action_frame, "Tanam", "plant", 1, 0)
        self._make_tool_button(action_frame, "Siram", "water", 1, 1)
        self._make_tool_button(action_frame, "Rawat", "care", 2, 0)
        self._make_tool_button(action_frame, "Panen", "harvest", 2, 1)
        self._make_tool_button(action_frame, "Bersihkan", "clear", 3, 0)

        command_frame = tk.Frame(action_frame, bg=PANEL_BG)
        command_frame.grid(row=3, column=1, sticky="ew", padx=(6, 0), pady=6)

        self.shop_button = tk.Button(
            command_frame,
            text="Toko Bibit",
            font=("Arial", 11, "bold"),
            bg="#ead8b0",
            fg=TEXT_DARK,
            activebackground="#ddc48a",
            relief="flat",
            padx=12,
            pady=10,
            command=self.open_shop,
        )
        self.shop_button.pack(fill="x")

        action_frame.grid_columnconfigure(0, weight=1)
        action_frame.grid_columnconfigure(1, weight=1)

        selected_plot_frame = tk.Frame(right_panel, bg=PANEL_BG)
        selected_plot_frame.pack(fill="x", padx=16, pady=(0, 10))

        tk.Label(
            selected_plot_frame,
            text="Info Petak",
            font=("Arial", 13, "bold"),
            bg=PANEL_BG,
            fg=TEXT_DARK,
        ).pack(anchor="w")

        self.plot_info_label = tk.Label(
            selected_plot_frame,
            textvariable=self.plot_info_var,
            justify="left",
            anchor="w",
            bg="#fff5e6",
            fg=TEXT_DARK,
            font=("Arial", 10),
            padx=10,
            pady=10,
            wraplength=420,
        )
        self.plot_info_label.pack(fill="x", pady=(6, 0))

        inventory_frame = tk.Frame(right_panel, bg=PANEL_BG)
        inventory_frame.pack(fill="x", padx=16, pady=(0, 10))

        tk.Label(
            inventory_frame,
            text="Inventaris Bibit",
            font=("Arial", 13, "bold"),
            bg=PANEL_BG,
            fg=TEXT_DARK,
        ).pack(anchor="w")

        self.inventory_label = tk.Label(
            inventory_frame,
            textvariable=self.inventory_var,
            justify="left",
            anchor="w",
            bg="#f8efe0",
            fg=TEXT_DARK,
            font=("Arial", 10),
            padx=10,
            pady=10,
        )
        self.inventory_label.pack(fill="x", pady=(6, 0))

        log_frame = tk.Frame(right_panel, bg=PANEL_BG)
        log_frame.pack(fill="both", expand=True, padx=16, pady=(0, 10))

        tk.Label(
            log_frame,
            text="Log Kegiatan",
            font=("Arial", 13, "bold"),
            bg=PANEL_BG,
            fg=TEXT_DARK,
        ).pack(anchor="w")

        self.log_text = tk.Text(
            log_frame,
            height=12,
            wrap="word",
            font=("Consolas", 10),
            bg="#fbf6eb",
            fg=TEXT_DARK,
            relief="flat",
            padx=10,
            pady=10,
        )
        self.log_text.pack(fill="both", expand=True, pady=(6, 0))
        self.log_text.config(state="disabled")

        bottom_buttons = tk.Frame(right_panel, bg=PANEL_BG)
        bottom_buttons.pack(fill="x", padx=16, pady=(0, 16))

        self.end_day_button = tk.Button(
            bottom_buttons,
            text="Hari Berikutnya",
            font=("Arial", 11, "bold"),
            bg=SUCCESS,
            fg="white",
            activebackground="#5e975e",
            relief="flat",
            padx=12,
            pady=10,
            command=self.end_day,
        )
        self.end_day_button.pack(side="left", fill="x", expand=True, padx=(0, 6))

        self.save_button = tk.Button(
            bottom_buttons,
            text="Simpan",
            font=("Arial", 11, "bold"),
            bg=ACCENT,
            fg="white",
            activebackground="#734b27",
            relief="flat",
            padx=12,
            pady=10,
            command=self.save_game,
        )
        self.save_button.pack(side="left", fill="x", expand=True, padx=6)

        self.load_button = tk.Button(
            bottom_buttons,
            text="Muat",
            font=("Arial", 11, "bold"),
            bg="#90755d",
            fg="white",
            activebackground="#7b624c",
            relief="flat",
            padx=12,
            pady=10,
            command=self.load_game,
        )
        self.load_button.pack(side="left", fill="x", expand=True, padx=6)

        self.new_button = tk.Button(
            bottom_buttons,
            text="Game Baru",
            font=("Arial", 11, "bold"),
            bg=WARNING,
            fg="white",
            activebackground="#b45d42",
            relief="flat",
            padx=12,
            pady=10,
            command=self.start_new_game,
        )
        self.new_button.pack(side="left", fill="x", expand=True, padx=(6, 0))

    def _stat_row(self, parent, label, variable):
        frame = tk.Frame(parent, bg=PANEL_BG)
        frame.pack(fill="x", pady=2)

        tk.Label(
            frame,
            text=f"{label}:",
            width=10,
            anchor="w",
            font=("Arial", 11, "bold"),
            bg=PANEL_BG,
            fg=TEXT_DARK,
        ).pack(side="left")

        tk.Label(
            frame,
            textvariable=variable,
            anchor="w",
            font=("Arial", 11),
            bg=PANEL_BG,
            fg=TEXT_LIGHT,
        ).pack(side="left")

    def _make_tool_button(self, parent, text, tool_key, row, col):
        button = tk.Button(
            parent,
            text=text,
            font=("Arial", 11, "bold"),
            relief="flat",
            padx=12,
            pady=10,
            command=lambda key=tool_key: self.set_tool(key),
        )
        button.grid(row=row, column=col, sticky="ew", padx=6, pady=6)
        self.tool_buttons[tool_key] = button

    # FLOW
    def _startup_flow(self):
        if self.save_manager.exists():
            load = messagebox.askyesno(
                "Muat Permainan",
                "Ditemukan save game.\nApakah Anda ingin melanjutkan permainan sebelumnya?",
                parent=self,
            )
            if load:
                try:
                    self.load_game(show_message=False)
                    self.log("Save game berhasil dimuat.")
                    return
                except SaveGameError as exc:
                    messagebox.showerror("Gagal Memuat", str(exc), parent=self)

        self.start_new_game(show_message=False)

    def start_new_game(self, show_message=True):
        name = simpledialog.askstring(
            "Nama Pemain",
            "Masukkan nama pemain:",
            parent=self,
        )

        if name is None or not name.strip():
            name = "Pemain"

        self.player = Player(name=name.strip())
        self.garden = Garden()
        self.day = 1
        self.selected_plot = None
        self.set_tool("plant", silent=True)
        self.clear_log()
        self.log(f"Permainan baru dimulai. Selamat datang, {self.player.name}!")
        self.refresh_ui()

        if show_message:
            messagebox.showinfo(
                "Game Baru",
                f"Permainan baru dimulai untuk {self.player.name}.",
                parent=self,
            )

    def save_game(self):
        self.ensure_game_ready()

        data = {
            "version": SAVE_VERSION,
            "day": self.day,
            "player": self.player.to_dict(),
            "garden": self.garden.to_dict(),
        }

        self.save_manager.save(data)
        self.log("Permainan berhasil disimpan.")
        messagebox.showinfo("Simpan", "Permainan berhasil disimpan.", parent=self)

    def load_game(self, show_message=True):
        data = self.save_manager.load()

        version = int(data.get("version", 0))
        if version != SAVE_VERSION:
            raise SaveGameError(
                f"Versi save game tidak didukung ({version})."
            )

        self.player = Player.from_dict(data["player"])
        self.garden = Garden.from_dict(data["garden"])
        self.day = max(1, int(data.get("day", 1)))
        self.selected_plot = None
        self.set_tool("plant", silent=True)
        self.refresh_ui()

        if show_message:
            self.log("Permainan berhasil dimuat.")
            messagebox.showinfo("Muat", "Permainan berhasil dimuat.", parent=self)

    def on_close(self):
        if self.player is None:
            self.destroy()
            return

        save = messagebox.askyesnocancel(
            "Keluar",
            "Simpan permainan sebelum keluar?",
            parent=self,
        )

        if save is None:
            return

        if save:
            try:
                self.save_game()
            except SaveGameError as exc:
                messagebox.showerror("Gagal Menyimpan", str(exc), parent=self)
                return

        self.destroy()

    # STATE + UI UPDATE
    def refresh_ui(self):
        self.ensure_game_ready()

        self.name_var.set(self.player.name)
        self.day_var.set(str(self.day))
        self.coins_var.set(str(self.player.coins))
        self.energy_var.set(f"{self.player.energy}/{MAX_ENERGY}")
        self.tool_var.set(f"Mode: {self.tool_display_name(self.selected_tool)}")
        self.inventory_var.set(self.build_inventory_text())
        self.plot_info_var.set(self.build_plot_info_text())

        self.refresh_tool_buttons()
        draw_garden(self.canvas, self.garden, self.selected_plot)

    def build_inventory_text(self):
        lines = []

        for key, info in PLANT_TYPES.items():
            lines.append(
                f"• {info['name']}: {self.player.seed_count(key)} bibit"
            )

        return "\n".join(lines)

    def build_plot_info_text(self):
        if self.selected_plot is None:
            return "Klik salah satu petak untuk melihat detail dan menjalankan aksi sesuai mode yang dipilih."

        plot = self.garden.get_plot(self.selected_plot)

        if plot.is_empty:
            return (
                f"Petak {plot.position}\n"
                f"Status: Kosong\n"
                f"Gunakan mode Tanam untuk menanam bibit."
            )

        plant = plot.plant
        watered = "Ya" if plant.watered_today else "Belum"
        cared = "Ya" if plant.cared_today else "Belum"

        return (
            f"Petak {plot.position}\n"
            f"Tanaman: {plant.name}\n"
            f"Tahap: {plant.stage_name}\n"
            f"Pertumbuhan: {plant.growth}/{plant.grow_days}\n"
            f"Kesehatan: {plant.health}/{plant.max_health}\n"
            f"Disiram hari ini: {watered}\n"
            f"Dirawat hari ini: {cared}\n"
            f"Nilai panen: {plant.harvest_value} koin"
        )

    def refresh_tool_buttons(self):
        for key, button in self.tool_buttons.items():
            if key == self.selected_tool:
                button.config(
                    bg="#e3a44b",
                    fg="white",
                    activebackground="#d29138",
                )
            else:
                button.config(
                    bg="#efe4d1",
                    fg=TEXT_DARK,
                    activebackground="#e2d1b5",
                )

    def set_tool(self, tool_key, silent=False):
        self.selected_tool = tool_key
        self.tool_var.set(f"Mode: {self.tool_display_name(tool_key)}")
        self.refresh_tool_buttons()
        if not silent:
            self.log(f"Mode diubah ke: {self.tool_display_name(tool_key)}")

    def tool_display_name(self, tool_key):
        names = {
            "plant": "Tanam",
            "water": "Siram",
            "care": "Rawat",
            "harvest": "Panen",
            "clear": "Bersihkan",
        }
        return names.get(tool_key, tool_key)

    # CANVAS / ACTIONS
    def on_canvas_click(self, event):
        self.ensure_game_ready()

        plot_number = pixel_to_plot(event.x, event.y)
        if plot_number is None:
            return

        self.selected_plot = plot_number

        try:
            self.apply_current_tool(plot_number)
        except GameError as exc:
            self.refresh_ui()
            self.log(f"Gagal: {exc}")
            messagebox.showwarning("Aksi Gagal", str(exc), parent=self)
            return

        self.refresh_ui()

    def apply_current_tool(self, plot_number):
        if self.selected_tool == "plant":
            self.action_plant(plot_number)
        elif self.selected_tool == "water":
            self.action_water(plot_number)
        elif self.selected_tool == "care":
            self.action_care(plot_number)
        elif self.selected_tool == "harvest":
            self.action_harvest(plot_number)
        elif self.selected_tool == "clear":
            self.action_clear(plot_number)

    def action_plant(self, plot_number):
        self.player.require_energy()

        display_name = self.seed_var.get()
        kind = self.display_to_key[display_name]

        if not self.player.has_seed(kind):
            raise GameError(f"Bibit {PLANT_TYPES[kind]['name']} habis.")

        plant = self.garden.plant_seed(plot_number, kind)
        self.player.use_seed(kind)
        self.player.consume_energy()

        self.log(
            f"Menanam {plant.name} di petak {plot_number}. "
            f"Energi tersisa: {self.player.energy}."
        )

    def action_water(self, plot_number):
        self.player.require_energy()

        plant = self.garden.water_plot(plot_number)
        self.player.consume_energy()

        self.log(
            f"Menyiram {plant.name} di petak {plot_number}. "
            f"Energi tersisa: {self.player.energy}."
        )

    def action_care(self, plot_number):
        self.player.require_energy()

        plant = self.garden.care_plot(plot_number)
        self.player.consume_energy()

        self.log(
            f"Merawat {plant.name} di petak {plot_number}. "
            f"Kesehatan sekarang: {plant.health}/{plant.max_health}. "
            f"Energi tersisa: {self.player.energy}."
        )

    def action_harvest(self, plot_number):
        self.player.require_energy()

        plant = self.garden.harvest_plot(plot_number)
        self.player.consume_energy()
        self.player.receive_harvest(plant.harvest_value)

        self.log(
            f"Memanen {plant.name} dari petak {plot_number}. "
            f"Mendapat {plant.harvest_value} koin. "
            f"Koin sekarang: {self.player.coins}."
        )

    def action_clear(self, plot_number):
        self.player.require_energy()

        dead_name = self.garden.clear_dead_plot(plot_number)
        self.player.consume_energy()

        self.log(
            f"Membersihkan tanaman mati ({dead_name}) dari petak {plot_number}. "
            f"Energi tersisa: {self.player.energy}."
        )

    def end_day(self):
        self.ensure_game_ready()

        proceed = messagebox.askyesno(
            "Hari Berikutnya",
            f"Akhiri hari ke-{self.day} dan lanjut ke hari berikutnya?",
            parent=self,
        )

        if not proceed:
            return

        events = self.garden.advance_day(self.rng)
        self.day += 1
        self.player.reset_energy()

        if self.rng.random() < 0.15:
            random_kind = self.rng.choice(list(PLANT_TYPES.keys()))
            self.player.seeds[random_kind] = self.player.seed_count(random_kind) + 1
            events.append(
                f"Bonus harian: mendapat 1 bibit {PLANT_TYPES[random_kind]['name']}."
            )

        self.log(f"Masuk ke hari ke-{self.day}. Energi dipulihkan menjadi {self.player.energy}/{MAX_ENERGY}.")

        if events:
            for item in events:
                self.log(item)
        else:
            self.log("Tidak ada peristiwa khusus hari ini.")

        self.refresh_ui()

    # SHOP
    def open_shop(self):
        self.ensure_game_ready()

        shop = tk.Toplevel(self)
        shop.title("Toko Bibit")
        shop.configure(bg=PANEL_BG)
        shop.resizable(False, False)
        shop.transient(self)
        shop.grab_set()

        coins_var = tk.StringVar(value=f"Koin Anda: {self.player.coins}")

        tk.Label(
            shop,
            text="Toko Bibit",
            font=("Arial", 16, "bold"),
            bg=PANEL_BG,
            fg=TEXT_DARK,
        ).pack(anchor="w", padx=16, pady=(16, 6))

        tk.Label(
            shop,
            textvariable=coins_var,
            font=("Arial", 11, "bold"),
            bg=PANEL_BG,
            fg=TEXT_LIGHT,
        ).pack(anchor="w", padx=16, pady=(0, 10))

        content = tk.Frame(shop, bg=PANEL_BG)
        content.pack(fill="both", expand=True, padx=16, pady=(0, 10))

        tk.Label(
            content,
            text="Jenis Bibit",
            font=("Arial", 11, "bold"),
            bg=PANEL_BG,
            fg=TEXT_DARK,
            width=18,
            anchor="w",
        ).grid(row=0, column=0, sticky="w", padx=(0, 6), pady=4)

        tk.Label(
            content,
            text="Info",
            font=("Arial", 11, "bold"),
            bg=PANEL_BG,
            fg=TEXT_DARK,
            width=32,
            anchor="w",
        ).grid(row=0, column=1, sticky="w", padx=6, pady=4)

        tk.Label(
            content,
            text="Aksi",
            font=("Arial", 11, "bold"),
            bg=PANEL_BG,
            fg=TEXT_DARK,
            width=14,
            anchor="w",
        ).grid(row=0, column=2, sticky="w", padx=6, pady=4)

        row_index = 1

        for key, info in PLANT_TYPES.items():
            tk.Label(
                content,
                text=info["name"],
                bg="#f9f0e1",
                fg=TEXT_DARK,
                font=("Arial", 10, "bold"),
                padx=8,
                pady=8,
                anchor="w",
                width=16,
            ).grid(row=row_index, column=0, sticky="ew", padx=(0, 6), pady=4)

            info_text = (
                f"Harga: {info['seed_price']} | "
                f"Panen: {info['harvest_value']} | "
                f"Tumbuh: {info['grow_days']} hari"
            )

            tk.Label(
                content,
                text=info_text,
                bg="#fdf8ef",
                fg=TEXT_LIGHT,
                font=("Arial", 10),
                padx=8,
                pady=8,
                anchor="w",
                width=34,
            ).grid(row=row_index, column=1, sticky="ew", padx=6, pady=4)

            action_wrap = tk.Frame(content, bg=PANEL_BG)
            action_wrap.grid(row=row_index, column=2, sticky="ew", padx=(6, 0), pady=4)

            buy1 = tk.Button(
                action_wrap,
                text="Beli 1",
                font=("Arial", 9, "bold"),
                bg="#ead8b0",
                fg=TEXT_DARK,
                relief="flat",
                command=lambda k=key: self._buy_seed_from_shop(k, 1, coins_var),
            )
            buy1.pack(side="left", padx=(0, 4))

            buy3 = tk.Button(
                action_wrap,
                text="Beli 3",
                font=("Arial", 9, "bold"),
                bg="#e0c487",
                fg=TEXT_DARK,
                relief="flat",
                command=lambda k=key: self._buy_seed_from_shop(k, 3, coins_var),
            )
            buy3.pack(side="left")

            row_index += 1

        close_button = tk.Button(
            shop,
            text="Tutup",
            font=("Arial", 10, "bold"),
            bg=ACCENT,
            fg="white",
            activebackground="#734b27",
            relief="flat",
            padx=14,
            pady=8,
            command=shop.destroy,
        )
        close_button.pack(anchor="e", padx=16, pady=(0, 16))

    def _buy_seed_from_shop(self, kind, quantity, coins_var):
        self.player.buy_seed(kind, quantity)
        coins_var.set(f"Koin Anda: {self.player.coins}")
        self.log(
            f"Membeli {quantity} bibit {PLANT_TYPES[kind]['name']}. "
            f"Koin tersisa: {self.player.coins}."
        )
        self.refresh_ui()

    # LOG
    def log(self, text):
        self.log_lines.append(text)

        if len(self.log_lines) > 80:
            self.log_lines = self.log_lines[-80:]

        self.log_text.config(state="normal")
        self.log_text.delete("1.0", "end")
        self.log_text.insert("end", "\n".join(self.log_lines))
        self.log_text.see("end")
        self.log_text.config(state="disabled")

    def clear_log(self):
        self.log_lines = []
        self.log_text.config(state="normal")
        self.log_text.delete("1.0", "end")
        self.log_text.config(state="disabled")

    # UTILS
    def ensure_game_ready(self):
        if self.player is None or self.garden is None:
            raise RuntimeError("Game belum diinisialisasi.")