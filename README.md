# default_attrgetter

This is a simple module that provides a python implementation similar to the `operator.attrgetter` function, but with a default value. As this is a python implementation it will probably be slower.

### example usage:
```python
from default_attrgetter import default_attrgetter

class A:
    one = 1
    two = 2

class B
    one = 1
    a = A()

b = B()

getter = default_attrgetter('one', 'a.two', 'missing', 'a.missing', default=0)
result = getter(b)
print(result) # (1, 2, 0, 0)
```
