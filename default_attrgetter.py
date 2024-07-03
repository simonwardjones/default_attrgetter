from typing import Any, Callable, overload


class Sentinel:
    pass


NO_DEFAULT = Sentinel()


def get_nested_attr(obj: Any, attr: str, default: Any) -> Any:
    if not isinstance(attr, str):  # type: ignore
        raise TypeError("attr must be a string")
    for name in attr.split("."):
        if hasattr(obj, name):
            obj = getattr(obj, name)
        elif default is not NO_DEFAULT:
            return default
        else:
            raise AttributeError(f"{name} not found in {obj}")
    return obj


@overload
def default_attrgetter(
    __attr: str, *, default: Any = NO_DEFAULT
) -> Callable[[Any], Any]: ...


@overload
def default_attrgetter(
    *attrs: str, default: Any = NO_DEFAULT
) -> Callable[[Any], tuple[Any, ...]]: ...


def default_attrgetter(
    *attrs: str, default: Any = NO_DEFAULT
) -> Callable[[Any], Any | tuple[Any, ...]]:
    """Get the attrs from an object, if an attribute is missing return the default value
    if the attr is a string split it by '.' and get the nested attribute.

    If multiple attributes are provided, return a tuple with the values

    If no default is provided and an attribute is missing, an attribute error is raised
    """

    def getter(obj: Any) -> Any | tuple[Any, ...]:
        if len(attrs) == 1:
            return get_nested_attr(obj, attrs[0], default)
        return tuple(get_nested_attr(obj, attr, default) for attr in attrs)

    return getter
