"""Response pieces shared by more than one feature.

A note on naming: fields are snake_case where the contract is snake_case, and
camelCase where it is camelCase (the pagination envelope, the transcript list).
That is what the front end reads, so the models say exactly that rather than
converting.
"""

from pydantic import BaseModel, ConfigDict


class ApiModel(BaseModel):
    """Base for every response model.

    ``populate_by_name`` lets a model be built from ORM attribute names while
    still serialising under the contract's field names where the two differ.
    """

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)


class PageMeta(ApiModel):
    """The pagination envelope every list endpoint returns."""

    page: int
    pageSize: int
    total: int
    totalPages: int


class SimpleResponse(ApiModel):
    """The plain success reply, for endpoints with nothing else to say."""

    ok: bool = True
    message: str | None = None
