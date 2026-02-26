from const_app.models import Const, Vat


def fetch_last_values() -> Const | None:
    return Const.objects.all().order_by("-start").first()


def fetch_last_vat() -> Vat | None:
    const = fetch_last_values()
    if const:
        return const.vat
    return None
