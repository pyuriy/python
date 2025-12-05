# Comprehensive Pydantic Data Validation Lab with Python

Welcome to this hands-on lab on Pydantic data validation! Pydantic is a powerful library for enforcing data types, validating inputs, and serializing models in Python applications (e.g., APIs, configs, ML pipelines). This lab builds on the cheat sheet, progressing from basics to advanced topics through guided exercises.

## Lab Objectives
- Understand Pydantic models and automatic validation.
- Implement field constraints and custom validators.
- Handle nested structures, serialization, and errors.
- Apply Pydantic in real-world scenarios like API payloads.
- Debug common issues.

**Prerequisites**: Python 3.8+, basic knowledge of type hints and classes.

**Estimated Time**: 2-3 hours.

## Setup
1. Create a new directory for the lab: `mkdir pydantic-lab && cd pydantic-lab`.
2. Create a virtual environment: `python -m venv venv` and activate it (`source venv/bin/activate` on Unix, `venv\Scripts\activate` on Windows).
3. Install Pydantic: `pip install pydantic[email]` (includes email validator).
4. Create a file `lab.py` for all exercises. Run snippets interactively in a REPL or Jupyter for faster iteration.
5. For verification: Copy-paste code into your editor and run `python lab.py`. Expected outputs are provided.

**Pro Tip**: Use `from pydantic import BaseModel, Field, ValidationError` as your import boilerplate.

---

## Section 1: Basic Models and Type Coercion
**Goal**: Create simple models and observe automatic type enforcement.

### Exercise 1.1: Simple User Model
Define a `User` model with `id` (int), `name` (str), and `age` (int, default 18). Instantiate with mixed types (e.g., `age="25"`) to see coercion.

```python
from pydantic import BaseModel

class User(BaseModel):
    id: int
    name: str
    age: int = 18

# Test instantiations
user1 = User(id=1, name="Alice", age="25")  # Coerces str to int
print(user1)  # Expected: id=1 name='Alice' age=25

user2 = User(id="2", name=42, age=30)  # Coerces str/int to types
print(user2)  # Expected: id=2 name='42' age=30
```

**Task**: Add a required `email` field without a default. Try instantiating without it—observe the `ValidationError`.

**Expected Error Snippet**:
```
pydantic_core._pydantic_core.ValidationError: 1 validation error for User
email
  Field required [type=missing, input_value={'id': 1, 'name': 'Bob'}, input_type=dict]
```

### Exercise 1.2: Config Tweaks
Add a `Config` class to the `User` model: `extra = 'forbid'` (reject extra fields) and `validate_assignment = True` (validate on reassignment).

```python
class User(BaseModel):
    # ... fields as above
    class Config:
        extra = 'forbid'
        validate_assignment = True

user = User(id=1, name="Alice", age=25, extra_field="oops")  # Should raise error
user.age = "thirty"  # Should coerce and validate
print(user.age)  # Expected: 30
```

**Task**: Experiment with `strict=True` in `Config`—does it prevent coercion? (Yes, `age="25"` would fail.)

**Verification**: Run and confirm no extra fields are accepted.

---

## Section 2: Field Constraints and Built-in Validators
**Goal**: Use `Field()` for constraints and explore type-specific validators.

### Exercise 2.1: Product Model with Constraints
Create a `Product` model: `name` (str, min_length=1), `price` (float, >0 and <=1000), `tags` (list[str], min_items=1).

```python
from pydantic import BaseModel, Field
from typing import List

class Product(BaseModel):
    name: str = Field(min_length=1)
    price: float = Field(gt=0, le=1000)
    tags: List[str] = Field(min_items=1, default_factory=list)  # Avoid mutable default

# Valid
product = Product(name="Laptop", price=999.99, tags=["electronics", "portable"])
print(product)  # Expected: name='Laptop' price=999.99 tags=['electronics', 'portable']

# Invalid: Try price=-5 or empty tags—catch the error
```

**Task**: Add `EmailStr` for a seller email. Test with invalid email like "not-an-email".

```python
from pydantic import EmailStr

# Add to Product:
seller_email: EmailStr = Field(...)
```

**Expected Error for Invalid Email**:
```
Input should be a valid email, unable to parse string as an email address [type=email_invalid, ...]
```

### Exercise 2.2: Annotated Types for Reuse
Define reusable types like `PositiveInt = Annotated[int, Field(gt=0)]` and use in a `Stock` model (`quantity: PositiveInt`).

```python
from typing import Annotated

PositiveInt = Annotated[int, Field(gt=0)]
PositiveFloat = Annotated[float, Field(gt=0)]

class Stock(BaseModel):
    symbol: str
    quantity: PositiveInt
    price: PositiveFloat

stock = Stock(symbol="AAPL", quantity="100", price=150.5)  # Coerces
print(stock)  # Expected: symbol='AAPL' quantity=100 price=150.5
```

**Task**: Create `UrlStr = Annotated[str, Field(pattern=r'^https?://')]` and test.

---

## Section 3: Custom Validators
**Goal**: Add business logic with field and model validators.

### Exercise 3.1: Field Validator for Age and Password
Extend `User` with validators: Age must be 18+ (after mode), password uppercase (before mode).

```python
from pydantic import field_validator

class User(BaseModel):
    # ... id, name, age, email as before
    password: str

    @field_validator('age', mode='after')
    @classmethod
    def validate_age(cls, v: int) -> int:
        if v < 18:
            raise ValueError('Age must be 18 or older')
        return v

    @field_validator('password', mode='before')
    @classmethod
    def uppercase_password(cls, v: str) -> str:
        return v.upper() if isinstance(v, str) else str(v).upper()

user = User(id=1, name="Bob", age=17, password="secret123")  # Age error
user_valid = User(id=2, name="Carol", age=25, password="hello")  # Password becomes 'HELLO'
print(user_valid.password)  # Expected: HELLO
```

**Task**: Add a multi-field validator for `name` and `email` (e.g., name can't be in email). Use `ValidationInfo` for context.

```python
@field_validator('name', mode='after')
@classmethod
def check_name_not_in_email(cls, v: str, info: ValidationInfo) -> str:
    if 'email' in info.data and v.lower() in info.data['email'].lower():
        raise ValueError('Name cannot be substring of email')
    return v
```

### Exercise 3.2: Model Validator for Consistency
In `User`, add a model validator (after mode) to ensure `age > 0` and log the model.

```python
from pydantic import model_validator
from typing_extensions import Self  # For type hints in Python <3.11

class User(BaseModel):
    # ... fields and field validators

    @model_validator(mode='after')
    def validate_model(self) -> Self:
        if self.age <= 0:
            raise ValueError('Age must be positive')
        print(f"Validated user: {self.name}, age {self.age}")
        return self
```

**Task**: Add a before-mode model validator to strip 'temp_' prefix from any field starting with it.

```python
@model_validator(mode='before')
@classmethod
def preprocess(cls, data):
    if isinstance(data, dict):
        return {k.lstrip('temp_'): v for k, v in data.items()}
    return data
```

**Test**: `User(temp_name="Dave")` → name="Dave".

---

## Section 4: Nested and Union Models
**Goal**: Build complex structures.

### Exercise 4.1: Nested Address in User
Define `Address` (city: str, zip: str with pattern `\d{5}`), then nest in `User.addresses: List[Address]`.

```python
from typing import List

class Address(BaseModel):
    city: str
    zip: str = Field(pattern=r'^\d{5}$')

class User(BaseModel):
    # ... basic fields
    addresses: List[Address] = Field(default_factory=list, min_items=1)

data = {
    "name": "Eve",
    "addresses": [{"city": "NYC", "zip": "10001"}, {"city": "LA", "zip": "90210"}]
}
user = User.model_validate(data)
print(user.addresses[0].city)  # Expected: NYC
```

**Task**: Make zip optional with `Optional[str]`. Test invalid zip like "ABCDE".

### Exercise 4.2: Unions and Literals
Add `status: Literal['active', 'inactive']` to User. Test invalid status.

```python
from typing import Literal

class User(BaseModel):
    # ...
    status: Literal['active', 'inactive'] = 'active'

# Invalid: status='pending' → Error: Input should be 'active' or 'inactive'
```

**Task**: Use Union for flexible `age: Union[int, str]` but validate str as age-like (e.g., "25 years").

---

## Section 5: Serialization and Error Handling
**Goal**: Output data safely and handle failures gracefully.

### Exercise 5.1: Dump and Load
Serialize User to JSON (exclude password, mask age if >100), then validate back.

```python
from pydantic import field_serializer

class User(BaseModel):
    # ... fields

    @field_serializer('password')
    def serialize_password(self, v: str) -> str:
        return '***MASKED***'

    @field_serializer('age')
    def serialize_age(self, v: int) -> str:
        return str(v) if v <= 100 else '>100'

user = User(id=1, name="Frank", age=105, password="pass")
json_str = user.model_dump_json(indent=2, exclude={'id'}, exclude_none=True)
print(json_str)
# Expected snippet: {"name": "Frank", "age": ">100", "password": "***MASKED***"}

# Load back
loaded = User.model_validate_json(json_str)
print(loaded.age)  # Expected: '>100' (as str? Wait, no—validators run on load!)
```

**Task**: Use `by_alias=True` with aliases (e.g., `full_name: str = Field(alias='name')`).

### Exercise 5.2: Robust Error Handling
Wrap instantiation in try-except, print errors prettily.

```python
try:
    bad_user = User(id="abc", age=-5)
except ValidationError as e:
    print(e.errors('short'))  # Human-readable
    print(e.json(indent=2))   # Full details
```

**Expected Output Snippet**:
```
[{'type': 'int_parsing', 'loc': ('id',), 'msg': 'Input should be a valid integer'}, {'type': 'greater_than_equal', 'loc': ('age',), 'msg': 'Input should be greater than or equal to 0'}]
```

**Task**: Create a function `safe_create_user(data: dict) -> User | None` that returns None on error, logging issues.

---

## Section 6: Advanced Challenges
**Goal**: Synthesize knowledge in mini-projects.

### Challenge 6.1: API Payload Validator (20 min)
Build a `Order` model: Nested `items: List[Item]` where `Item` has quantity (PositiveInt), product (str). Model validator: total quantity <=10. Serialize to camelCase (use `alias_generator` in Config).

```python
# Starter
class Item(BaseModel):
    quantity: PositiveInt
    product: str

class Order(BaseModel):
    items: List[Item]
    # Add validator for sum(quantities) <=10

    class Config:
        alias_generator = lambda field_name: ''.join(word.capitalize() for word in field_name.split('_'))
        populate_by_name = True  # Allow both snake and camel
```

**Test Data**:
```python
order_data = {"items": [{"quantity": 3, "product": "apple"}, {"quantity": 8, "product": "banana"}]}
# Should error on total=11
```

**Extension**: Add `HttpUrl` for delivery_url.

### Challenge 6.2: Config from Env (15 min)
Use `BaseSettings` for a `AppConfig` model: `db_url: str`, `debug: bool = False`. Load from `.env` file.

Create `.env`:
```
DB_URL=sqlite:///app.db
DEBUG=true
```

```python
from pydantic_settings import BaseSettings  # pip install pydantic-settings

class AppConfig(BaseSettings):
    db_url: str
    debug: bool = False

    class Config:
        env_file = '.env'

config = AppConfig()
print(config)  # Expected: db_url='sqlite:///app.db' debug=True
```

**Task**: Add validation: db_url must start with 'sqlite://' or 'postgres://'.

### Challenge 6.3: Recursive Category Model (15 min)
Define `Category` with `name: str`, `subcategories: List['Category'] = []`. Test a nested dict.

```python
from typing import List, Any  # Forward ref handled automatically in v2

class Category(BaseModel):
    name: str
    subcategories: List['Category'] = Field(default_factory=list)

data = {
    "name": "Electronics",
    "subcategories": [{"name": "Phones", "subcategories": [{"name": "iPhone"}]}]
}
cat = Category.model_validate(data)
print(cat.subcategories[0].subcategories[0].name)  # Expected: iPhone
```

**Extension**: Validator to prevent cycles (hint: track seen names).

---

## Wrap-Up and Best Practices
- **Debug Tip**: Use `model_dump(mode='json')` for safe serialization.
- **Performance**: For bulk validation, use `TypeAdapter(User).validate_python(data)`.
- **Common Pitfalls**: Mutable defaults (use `default_factory`), validator order (before: right-to-left).
- **Next Steps**: Integrate with FastAPI for API validation. Explore v2 migrations if from v1.

**Self-Check**: Run all code—fix any errors. Share your `lab.py` on GitHub for feedback!

For questions or extensions, ask! Sources: Pydantic docs (v2.8+ as of Dec 2025). Happy validating! 🚀
