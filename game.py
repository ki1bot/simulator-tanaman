from random import Random

from constants import (
    GARDEN_COLS,
    GARDEN_ROWS,
    MAX_ENERGY,
    PLANT_CATALOG,
    SAVE_VERSION,
)
from exceptions import (
    GameError,
    SaveGameError,
)
from garden import Garden
from player import Player
from save_manager import SaveManager
from utils import (
    ask_int,
    ask_yes_no,
    clear_screen,
    pause,
)


class Game:
    def __init__(
        self,
        player,
        garden,
        day=1,
        save_manager=None,
        rng=None,
    ):
        self.player = player
        self.garden = garden
        self.day = max(
            1,
            int(day),
        )
        self.save_manager = (
            save_manager
            or SaveManager()
        )
        self.rng = rng or Random()
        self.running = True

    @classmethod
    def new_game(
        cls,
        player_name,
        save_manager=None,
    ):
        return cls(
            player=Player(
                name=player_name
            ),
            garden=Garden(),
            day=1,
            save_manager=save_manager,
        )

    @classmethod
    def from_save(
        cls,
        data,
        save_manager=None,
    ):
        try:
            version = int(
                data.get("version", 0)
            )

            if version != SAVE_VERSION:
                raise SaveGameError(
                    f"Versi save game "
                    f"{version} tidak didukung. "
                    f"Versi yang didukung "
                    f"adalah {SAVE_VERSION}."
                )

            player_data = data["player"]
            garden_data = data["garden"]
            day = int(
                data.get("day", 1)
            )

            player = Player.from_dict(
                player_data
            )

            garden = Garden.from_dict(
                garden_data
            )

            return cls(
                player=player,
                garden=garden,
                day=day,
                save_manager=save_manager,
            )
        except SaveGameError:
            raise
        except (
            KeyError,
            TypeError,
            ValueError,
        ) as exc:
            raise SaveGameError(
                "Data save game rusak "
                "atau tidak lengkap."
            ) from exc

    def run(self):
        while self.running:
            self.show_dashboard()

            choice = ask_int(
                "Pilih menu [1-10]: ",
                1,
                10,
            )

            actions = {
                1: self.show_garden_details,
                2: self.plant_action,
                3: self.water_action,
                4: self.care_action,
                5: self.harvest_action,
                6: self.clean_dead_action,
                7: self.shop_action,
                8: self.end_day_action,
                9: self.save_action,
                10: self.exit_action,
            }

            try:
                actions[choice]()
            except (
                GameError,
                ValueError,
                KeyError,
            ) as exc:
                print(
                    f"\nGagal: {exc}"
                )
                pause()

    def show_dashboard(self):
        clear_screen()

        print("=" * 78)
        print(
            "SIMULATOR TAMAN BERBASIS TEKS"
        )
        print("=" * 78)

        print(
            f"Pemain: {self.player.name} | "
            f"Hari: {self.day} | "
            f"Koin: {self.player.coins} | "
            f"Energi: "
            f"{self.player.energy}/"
            f"{MAX_ENERGY}"
        )

        print(
            f"Total panen: "
            f"{self.player.total_harvested} | "
            f"Total pendapatan: "
            f"{self.player.total_earned} koin"
        )

        print("-" * 78)

        print(
            self.garden.render()
        )

        print("-" * 78)

        print(
            "1. Lihat detail taman"
        )
        print(
            "2. Tanam bibit"
        )
        print(
            "3. Siram tanaman"
        )
        print(
            "4. Rawat tanaman"
        )
        print(
            "5. Panen tanaman"
        )
        print(
            "6. Bersihkan tanaman mati"
        )
        print(
            "7. Toko bibit"
        )
        print(
            "8. Akhiri hari"
        )
        print(
            "9. Simpan permainan"
        )
        print(
            "10. Keluar"
        )

        print("=" * 78)

    def show_garden_details(self):
        clear_screen()

        print(
            "DETAIL TAMAN"
        )
        print("=" * 78)

        for line in (
            self.garden.detail_lines()
        ):
            print(line)

        pause()

    def choose_plot(
        self,
        prompt,
    ):
        total = (
            GARDEN_ROWS
            * GARDEN_COLS
        )

        return ask_int(
            prompt,
            1,
            total,
        )

    def choose_plant(
        self,
        show_owned=True,
    ):
        keys = list(
            PLANT_CATALOG.keys()
        )

        print(
            "\nJenis tanaman:"
        )

        for index, key in enumerate(
            keys,
            start=1,
        ):
            data = (
                PLANT_CATALOG[key]
            )

            owned = ""

            if show_owned:
                owned = (
                    " | bibit dimiliki: "
                    f"{self.player.seed_count(key)}"
                )

            print(
                f"{index}. "
                f"{data['name']} | "
                f"tumbuh "
                f"{data['grow_days']} hari | "
                f"harga bibit "
                f"{data['seed_price']} | "
                f"nilai panen "
                f"{data['harvest_value']}"
                f"{owned}"
            )

        choice = ask_int(
            f"Pilih tanaman "
            f"[1-{len(keys)}]: ",
            1,
            len(keys),
        )

        return keys[
            choice - 1
        ]

    def plant_action(self):
        clear_screen()

        print(
            "TANAM BIBIT"
        )
        print("=" * 78)

        print(
            self.garden.render()
        )

        self.player.require_energy()

        position = self.choose_plot(
            "\nPilih petak yang "
            "ingin ditanami: "
        )

        plot = (
            self.garden.get_plot(
                position
            )
        )

        if not plot.is_empty:
            raise GameError(
                f"Petak {position} "
                f"sudah terisi."
            )

        kind = self.choose_plant(
            show_owned=True
        )

        self.player.use_seed(
            kind
        )

        plant = (
            self.garden.plant_seed(
                position,
                kind,
            )
        )

        self.player.consume_energy()

        print(
            f"\n{plant.name} "
            f"berhasil ditanam "
            f"di petak {position}. "
            f"Energi tersisa: "
            f"{self.player.energy}."
        )

        pause()

    def water_action(self):
        clear_screen()

        print(
            "SIRAM TANAMAN"
        )
        print("=" * 78)

        print(
            self.garden.render()
        )

        self.player.require_energy()

        position = self.choose_plot(
            "\nPilih petak yang "
            "ingin disiram: "
        )

        plant = (
            self.garden.water(
                position
            )
        )

        self.player.consume_energy()

        print(
            f"\n{plant.name} "
            f"di petak {position} "
            f"berhasil disiram. "
            f"Energi tersisa: "
            f"{self.player.energy}."
        )

        pause()

    def care_action(self):
        clear_screen()

        print(
            "RAWAT TANAMAN"
        )
        print("=" * 78)

        print(
            self.garden.render()
        )

        self.player.require_energy()

        position = self.choose_plot(
            "\nPilih petak yang "
            "ingin dirawat: "
        )

        plant = (
            self.garden.care(
                position
            )
        )

        self.player.consume_energy()

        print(
            f"\n{plant.name} "
            f"di petak {position} "
            f"berhasil dirawat.\n"
            f"Kesehatan sekarang: "
            f"{plant.health}/"
            f"{plant.max_health}.\n"
            f"Energi tersisa: "
            f"{self.player.energy}."
        )

        pause()

    def harvest_action(self):
        clear_screen()

        print(
            "PANEN TANAMAN"
        )
        print("=" * 78)

        print(
            self.garden.render()
        )

        self.player.require_energy()

        position = self.choose_plot(
            "\nPilih petak yang "
            "ingin dipanen: "
        )

        plant = (
            self.garden.harvest(
                position
            )
        )

        self.player.consume_energy()

        self.player.receive_harvest(
            plant.harvest_value
        )

        print(
            f"\n{plant.name} "
            f"berhasil dipanen "
            f"dari petak {position}.\n"
            f"Anda memperoleh "
            f"{plant.harvest_value} koin."
        )

        pause()

    def clean_dead_action(self):
        clear_screen()

        print(
            "BERSIHKAN TANAMAN MATI"
        )
        print("=" * 78)

        print(
            self.garden.render()
        )

        self.player.require_energy()

        position = self.choose_plot(
            "\nPilih petak yang "
            "ingin dibersihkan: "
        )

        plant_name = (
            self.garden.remove_dead(
                position
            )
        )

        self.player.consume_energy()

        print(
            f"\nSisa tanaman "
            f"{plant_name} "
            f"di petak {position} "
            f"berhasil dibersihkan.\n"
            f"Energi tersisa: "
            f"{self.player.energy}."
        )

        pause()

    def shop_action(self):
        clear_screen()

        print(
            "TOKO BIBIT"
        )
        print("=" * 78)

        print(
            f"Koin Anda: "
            f"{self.player.coins}"
        )

        kind = self.choose_plant(
            show_owned=True
        )

        quantity = ask_int(
            "Jumlah bibit yang "
            "ingin dibeli: ",
            1,
            99,
        )

        data = (
            PLANT_CATALOG[kind]
        )

        total_cost = (
            data["seed_price"]
            * quantity
        )

        print(
            f"\nTotal harga "
            f"{quantity} bibit "
            f"{data['name']}: "
            f"{total_cost} koin."
        )

        if not ask_yes_no(
            "Lanjutkan pembelian?"
        ):
            print(
                "Pembelian dibatalkan."
            )

            pause()
            return

        self.player.buy_seed(
            kind,
            quantity,
        )

        print(
            f"Pembelian berhasil.\n"
            f"Bibit {data['name']} "
            f"sekarang: "
            f"{self.player.seed_count(kind)}.\n"
            f"Koin tersisa: "
            f"{self.player.coins}."
        )

        pause()

    def end_day_action(self):
        clear_screen()

        print(
            "AKHIRI HARI"
        )
        print("=" * 78)

        if not ask_yes_no(
            f"Akhiri hari ke-"
            f"{self.day}?"
        ):
            print(
                "Akhir hari dibatalkan."
            )

            pause()
            return

        events = (
            self.garden.advance_day(
                self.rng
            )
        )

        self.day += 1

        self.player.reset_energy()

        if self.rng.random() < 0.12:
            bonus_kind = (
                self.rng.choice(
                    list(
                        PLANT_CATALOG.keys()
                    )
                )
            )

            self.player.seeds[
                bonus_kind
            ] = (
                self.player.seed_count(
                    bonus_kind
                )
                + 1
            )

            events.append(
                "Bonus harian: "
                "Anda menemukan "
                "1 bibit "
                f"{PLANT_CATALOG[bonus_kind]['name']}."
            )

        print(
            f"\nSekarang memasuki "
            f"hari ke-{self.day}."
        )

        print(
            f"Energi dipulihkan "
            f"menjadi "
            f"{self.player.energy}/"
            f"{MAX_ENERGY}."
        )

        if events:
            print(
                "\nPeristiwa hari ini:"
            )

            for event in events:
                print(
                    f"- {event}"
                )
        else:
            print(
                "\nTidak ada perubahan "
                "pada taman hari ini."
            )

        pause()

    def save_action(self):
        self.save_manager.save(
            self.to_dict()
        )

        print(
            "\nPermainan tersimpan ke "
            f"{self.save_manager.file_path}."
        )

        pause()

    def exit_action(self):
        if ask_yes_no(
            "Simpan permainan "
            "sebelum keluar?"
        ):
            self.save_manager.save(
                self.to_dict()
            )

            print(
                "Permainan berhasil "
                "disimpan."
            )

        self.running = False

    def to_dict(self):
        return {
            "version": SAVE_VERSION,
            "day": self.day,
            "player": (
                self.player.to_dict()
            ),
            "garden": (
                self.garden.to_dict()
            ),
        }