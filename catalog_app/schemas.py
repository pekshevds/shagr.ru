from pydantic import BaseModel, Field


class CategorySchemaOutgoing(BaseModel):
    id: str = Field()
    name: str = Field(max_length=150)
    slug: str = Field(max_length=300, default="")
    parent_slug: str = Field(max_length=300, default="")
    childs: list["CategorySchemaOutgoing"] | None = Field(default=None)


class CategoryListSchemaOutgoing(BaseModel):
    categories: list[CategorySchemaOutgoing] = Field()
    count: int = Field(default=0)


class GoodSchemaIncoming(BaseModel):
    id: str = Field()
    name: str = Field(max_length=150)
    art: str = Field(max_length=50, default="")
    code: str = Field(max_length=11, default="")
    okei: str = Field(max_length=50, default="")
    price: float = Field(default=0)
    description: str = Field(max_length=2048, default="")
    balance: float = Field(default=0)
    is_active: bool = Field(default=False)


class GoodSchemaOutgoing(BaseModel):
    id: str = Field()
    name: str = Field(max_length=150)
    short_name: str = Field(max_length=50, default="")
    art: str = Field(max_length=50, default="")
    slug: str = Field(max_length=300, default="")
    code: str = Field(max_length=11, default="")
    okei: str = Field(max_length=50, default="")
    price: float = Field(default=0)
    description: str = Field(max_length=2048, default="")
    balance: float = Field(default=0)
    is_active: bool = Field(default=False)
    seo_title: str = Field(default="")
    seo_description: str = Field(default="")
    seo_keywords: str = Field(default="")


class GoodListSchemaOutgoing(BaseModel):
    goods: list[GoodSchemaOutgoing] = Field()
    count: int = Field(default=0)
