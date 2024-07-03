from dataclasses import dataclass
from typing import Any

import pytest

from default_attrgetter import default_attrgetter


@dataclass
class Address:
    street: str
    number: int
    city: str
    postcode: str


@dataclass
class House:
    rooms: int
    bathrooms: int
    address: Address | None = None


@pytest.fixture
def house_with_address() -> House:
    return House(
        rooms=3,
        bathrooms=2,
        address=Address(
            street="Main St", number=123, city="Springfield", postcode="12345"
        ),
    )


@pytest.mark.parametrize(
    "attrs, expected",
    [
        (("rooms",), 3),
        (("rooms", "bathrooms"), (3, 2)),
        (("rooms", "missing"), (3, "default")),
        (("address.street",), "Main St"),
        (("address.missing",), "default"),
        (("address.street", "address.number"), ("Main St", 123)),
        (
            ("address.street", "address.missing", "missing"),
            ("Main St", "default", "default"),
        ),
    ],
)
def test_default_attrgetter(
    attrs: tuple[str], expected: Any | tuple[Any, ...], house_with_address: House
) -> None:
    getter = default_attrgetter(*attrs, default="default")
    assert getter(house_with_address) == expected


def test_default_attrgetter_raises_attribute_error(house_with_address: House):
    getter = default_attrgetter("address.missing")
    with pytest.raises(AttributeError) as err:
        getter(house_with_address)
    assert "missing not found in Address" in str(err.value)


def test_default_attrgetter_raises_type_error(house_with_address: House):
    getter = default_attrgetter("address", "missing")
    with pytest.raises(AttributeError) as err:
        getter(house_with_address)
    assert "missing not found in House" in str(err.value)
