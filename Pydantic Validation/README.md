# Pydantic Validation Cheat Sheet

Pydantic is a Python library for data validation, parsing, and serialization using type annotations. It enforces types at runtime, handles coercion, and provides clear error messages. Ideal for APIs, configs, and data pipelines.

## Installation
```bash
pip install pydantic
```
*Requires Python 3.8+.*

## Basic Models
Inherit from `BaseModel` to define schemas. Pydantic validates on instantiation.

```python
from pydantic import BaseModel

class User(BaseModel):
    id: int
    name: str
    age: int = 18  # Default value

# Valid instantiation (coerces types)
user = User(id=1, name="Alice", age="25")  # age becomes int
print(user)  # id=1 name='Alice' age=25

# Invalid: Raises ValidationError
# User(id="abc", name="Alice", age=25)
```

- **Key Behavior**: Automatic type coercion (e.g., str → int). Use `strict=True` in `Config` to disable.
- **Config Class** (optional):
  ```python
  class Config:
      validate_assignment = True  # Validate on field assignment
      extra = 'forbid'  # Reject extra fields
  ```

## Built-in Types & Constraints
Pydantic supports standard types + extras like `EmailStr`, `HttpUrl`.

| Type | Example | Constraint Examples |
|------|---------|---------------------|
| `int` | `x: int` | `Field(gt=0, le=100)` (greater than 0, ≤100) |
| `str` | `x: str` | `Field(min_length=3, max_length=50)` |
| `float` | `x: float` | `Field(multiple_of=0.5)` |
| `bool` | `x: bool` | `Field()` (coerces 'true' → True) |
| `EmailStr` | `email: EmailStr` | Validates email format |
| `HttpUrl` | `url: HttpUrl` | Validates URL |
| `list[int]` | `tags: list[str]` | `Field(min_items=1)` |
| `dict[str, int]` | `meta: dict[str, Any]` | `Field(max_items=10)` |

```python
from pydantic import BaseModel, Field, EmailStr

class Product(BaseModel):
    name: str = Field(..., min_length=1)  # Required field
    price: float = Field(gt=0, le=1000)
    email: EmailStr
```

- **...** in `Field(...)` makes field required (no default).

## Field Options (via `Field()`)
Customize fields with `pydantic.Field()`.

| Option | Purpose | Example |
|--------|---------|---------|
| `gt/lt/ge/le` | Numeric bounds | `Field(gt=0)` |
| `min_length/max_length` | String/list length | `Field(min_length=5)` |
| `multiple_of` | Multiples | `Field(multiple_of=5)` |
| `alias` | Input key alias | `Field(alias='full_name')` |
| `default` | Default value | `Field(default='unknown')` |
| `default_factory` | Callable default | `Field(default_factory=datetime.utcnow)` |
| `strict=True` | No coercion | `Field(strict=True)` |
| `frozen=True` | Immutable field | Prevents post-init changes |
| `exclude=True` | Skip in serialization | Omitted in `model_dump()` |
| `json_schema_extra` | Custom schema | `{'example': 'value'}` |

```python
from pydantic import Field
from typing import Annotated

# Annotated pattern for reuse
PositiveInt = Annotated[int, Field(gt=0)]
class Model(BaseModel):
    count: PositiveInt
```

## Validators
Custom logic with `@field_validator` or `@model_validator`. Modes: `'before'`, `'after'`, `'plain'`, `'wrap'`.

### Field Validators
Validate single/multiple fields.

| Mode | When | Behavior |
|------|------|----------|
| `before` | Pre-parsing | Raw input; return coercible value |
| `after` | Post-parsing | Typed value; validate/mutate |
| `plain` | Replaces parsing | No further validation |
| `wrap` | Around parsing | Handler for delegation; error handling |

```python
from pydantic import BaseModel, field_validator

class User(BaseModel):
    age: int
    password: str

    @field_validator('age', mode='after')
    @classmethod
    def check_age(cls, v: int) -> int:
        if v < 18:
            raise ValueError('Must be 18+')
        return v

    @field_validator('password', mode='before')
    @classmethod
    def hash_password(cls, v: str) -> str:
        return v.upper()  # Mutate input

    # Multiple fields
    @field_validator('age', 'password', mode='after')
    @classmethod
    def log_field(cls, v):
        print(f"Validated: {v}")
        return v
```

- **Raise Errors**: `ValueError`, `TypeError`, or `PydanticCustomError`.
- **Info Access**: Add `ValidationInfo` param for context (e.g., `info.data`).

### Model Validators
Validate entire model.

```python
from pydantic import model_validator
from typing_extensions import Self

class User(BaseModel):
    username: str
    password: str
    confirm_password: str

    @model_validator(mode='after')
    def passwords_match(self) -> Self:
        if self.password != self.confirm_password:
            raise ValueError('Passwords must match')
        return self

    @model_validator(mode='before')
    @classmethod
    def preprocess(cls, data):
        if isinstance(data, dict) and 'sensitive' in data:
            del data['sensitive']  # Remove forbidden keys
        return data
```

- **Wrap Mode**: Use `handler` to delegate (e.g., logging errors).

## Nested & Recursive Models
Handle complex structures.

```python
from typing import List
from pydantic import BaseModel

class Address(BaseModel):
    city: str
    zip: str = Field(pattern=r'\d{5}')

class User(BaseModel):
    name: str
    addresses: List[Address] = Field(min_items=1)  # List validation

# Recursive (e.g., tree)
class TreeNode(BaseModel):
    value: int
    children: List['TreeNode'] = []  # Forward ref

user = User(name="Alice", addresses=[{"city": "NYC", "zip": "10001"}])
```

- **Union Types**: `status: Literal['active', 'inactive']` or `Union[str, int]`.

## Serialization & Parsing
Convert models to dict/JSON.

```python
# To dict
data = user.model_dump(by_alias=True, exclude={'password'})  # {'name': 'Alice', ...}

# To JSON
json_str = user.model_dump_json(indent=2, exclude_none=True)

# From dict/JSON
new_user = User.model_validate(data)  # Or User.model_validate_json(json_str)

# Custom serializers
@field_serializer('password')
def serialize_pw(self, v: str) -> str:
    return '***'  # Mask in output
```

- **Modes**: `mode='python'` (dict), `mode='json'` (JSON-compatible).
- **Include/Exclude**: `include={'fields'}`, `exclude_unset=True` (omit defaults).

## Error Handling
`ValidationError` provides details.

```python
from pydantic import ValidationError

try:
    User(id="invalid")
except ValidationError as e:
    print(e.errors())  # [{'type': 'int_parsing', 'loc': ('id',), 'msg': 'Input should be a valid integer'}]
    print(e.json(indent=2))  # Formatted JSON
```

- **Custom Errors**: Use `PydanticCustomError` for schema-friendly messages.

## Advanced Tips
- **Settings**: Use `BaseSettings` for env vars (e.g., `class Config: env_file='.env'`).
- **Dataclasses**: `@dataclass` with Pydantic via `pydantic.dataclasses.dataclass`.
- **Performance**: Use `TypeAdapter` for non-model validation (faster).
- **Best Practices**:
  - Validate defaults: `validate_default=True` in `Field`.
  - Use `alias_generator` for snake_case → camelCase.
  - Avoid mutable defaults (use `default_factory`).
  - For large models, validate subsets with `model_validate(partial_data, from_attributes=True)`.
- **Common Pitfalls**: Order of validators (before: right-to-left; after: left-to-right). Inheritance overrides model validators.

## Sources
Compiled from official Pydantic docs (v2+), Medium cheat sheets, and dev resources (as of Dec 2025). For latest, see [docs.pydantic.dev](https://docs.pydantic.dev/latest/).
