import pydantic

from errors import ApiException


class CreateUserSchema(pydantic.BaseModel):
    email: str
    password: str


class CreateAdvertisementSchema(pydantic.BaseModel):
    title: str
    description: str
    user_id: int


def validate(data: dict, schema_class):
    try:
        return schema_class(**data).dict()
    except pydantic.ValidationError as err:
        raise ApiException(400, err.errors())
