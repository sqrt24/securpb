avoid_prepos_letters = {"а", "о", "е", "и", "у", "я", "ы"}
prefer_prepos_letters = {"в", "ф"}


def price2human(val: int | float) -> str:
    try:
        val = "{:.2f}".format(round(float(val), 2))
        int_part, float_part = val.split(".")
        if float_part != "00":
            return f"{int(int_part):,}".replace(",", " ") + "," + float_part
        else:
            return f"{int(int_part):,}".replace(",", " ")
    except (ValueError, TypeError):
        return str(val)


def round_value(val: int | float) -> str:
    try:
        formated = "{:.2f}".format(round(float(val), 2))
        return formated.rstrip("0").rstrip(".")
    except (ValueError, TypeError):
        return str(val)


def prepos(prep: str, word: str = "") -> str:
    if len(word) == 0 or word is None:
        return prep

    match prep.lower():
        case "в":
            if word[0].lower() in prefer_prepos_letters:
                if len(word) > 1 and word[1] not in avoid_prepos_letters:
                    prep += "о"
    return f"{prep} {word}"
