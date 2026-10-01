import os


def clear_screen():
    os.system(
        "cls"
        if os.name == "nt"
        else "clear"
    )


def pause():
    input(
        "\nTekan Enter untuk melanjutkan..."
    )


def ask_text(prompt):
    while True:
        value = input(prompt).strip()

        if value:
            return value

        print(
            "Input tidak boleh kosong."
        )


def ask_int(
    prompt,
    minimum=None,
    maximum=None,
):
    while True:
        raw = input(prompt).strip()

        try:
            value = int(raw)
        except ValueError:
            print(
                "Masukkan angka yang valid."
            )
            continue

        if (
            minimum is not None
            and value < minimum
        ):
            print(
                f"Nilai minimal adalah "
                f"{minimum}."
            )
            continue

        if (
            maximum is not None
            and value > maximum
        ):
            print(
                f"Nilai maksimal adalah "
                f"{maximum}."
            )
            continue

        return value


def ask_yes_no(prompt):
    while True:
        answer = input(
            f"{prompt} [y/n]: "
        ).strip().lower()

        if answer in {
            "y",
            "ya",
        }:
            return True

        if answer in {
            "n",
            "tidak",
        }:
            return False

        print(
            "Masukkan y atau n."
        )