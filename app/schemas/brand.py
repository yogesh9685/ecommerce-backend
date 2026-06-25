from pydantic import BaseModel, HttpUrl


class BrandCreate(BaseModel):
    name: str
    description: str | None = None
    logo_url: HttpUrl | None = None
    website_url: HttpUrl | None = None
    is_active: bool = True
