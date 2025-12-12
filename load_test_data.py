from pathlib import Path
from json import load
from services import catalog_service
from catalog_app.schemas import GoodSchemaIncoming

BASE_DIR = Path(__file__).resolve().parent


def load_test_data() -> None:
    with open(BASE_DIR / "test_data.json", mode="r", encoding="utf-8") as file:
        goods_list = [
            GoodSchemaIncoming(
                id=item.get("id"),
                name=item.get("name"),
                art=item.get("art"),
                okei=item.get("okei"),
                price=item.get("price"),
                description=item.get("description")[2048]
                if len(item.get("description")) > 2048
                else item.get("description"),
                balance=item.get("balance"),
                is_active=item.get("is_active"),
            )
            for item in load(file)
        ]
        catalog_service.create_or_update_goods(goods_list)
