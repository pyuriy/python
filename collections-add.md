# Python Collections Cheat Sheet - addition

This cheat sheet covers key Python collections and iterable concepts: **List**, **Dictionary**, **Set**, **Tuple**, **Range**, **Enumerate**, **Iterator**, and **Generator**. It includes creation, common operations, methods/functions, and examples. Focus is on Python 3.x essentials.

## List
Mutable, ordered sequence. Allows duplicates. Indexed (0-based).

### Creation
| Syntax | Example | Notes |
|--------|---------|-------|
| `[]` or `list()` | `lst = []`<br>`lst = list("abc")` | Empty or from iterable. |
| Comprehension | `lst = [x**2 for x in range(5)]` | `[0, 1, 4, 9, 16]` |

### Access & Slicing
- Index: `lst[0]` (first), `lst[-1]` (last).
- Slice: `lst[1:3]` (indices 1 to 2), `lst[::-1]` (reverse).
- Length: `len(lst)`.

### Common Methods
| Method | Description | Example |
|--------|-------------|---------|
| `append(x)` | Add `x` to end. | `lst.append(4)` → `[1,2,3,4]` |
| `extend(iterable)` | Add all from iterable to end. | `lst.extend([4,5])` → `[1,2,3,4,5]` |
| `insert(i, x)` | Insert `x` at index `i`. | `lst.insert(1, 0)` → `[1,0,2,3]` |
| `remove(x)` | Remove first occurrence of `x`. | `lst.remove(2)` → `[1,3]` |
| `pop(i=-1)` | Remove/return item at `i`. | `val = lst.pop(0)` → `val=1`, lst=`[2,3]` |
| `index(x)` | Return index of first `x`. | `lst.index(3)` → `2` |
| `count(x)` | Count occurrences of `x`. | `lst.count(2)` → `1` |
| `sort(key=None, reverse=False)` | Sort in place. | `lst.sort()` → sorted list |
| `reverse()` | Reverse in place. | `lst.reverse()` → `[3,2,1]` |
| `clear()` | Remove all items. | `lst.clear()` → `[]` |

### Example
```python
lst = [1, 2, 3]
lst += [4]  # [1,2,3,4]
print(lst[1:])  # [2,3,4]
```

## Dictionary
Mutable, unordered (pre-3.7; insertion-ordered since 3.7), key-value pairs. Keys unique, hashable.

### Creation
| Syntax | Example | Notes |
|--------|---------|-------|
| `{}` or `dict()` | `d = {}`<br>`d = dict(a=1, b=2)` | Empty or from kwargs. |
| From iterables | `d = dict([('a',1), ('b',2)])` | Pairs of (key, value). |
| Comprehension | `d = {x: x**2 for x in range(3)}` | `{0:0, 1:1, 2:4}` |

### Access
- Key: `d['a']` (raises KeyError if missing).
- Safe: `d.get('a', 0)` (default 0 if missing).
- Keys/Values/Items: `list(d.keys())`, `list(d.values())`, `list(d.items())`.

### Common Methods
| Method | Description | Example |
|--------|-------------|---------|
| `d[k] = v` | Set `v` for key `k`. | `d['c'] = 3` → `{'a':1, 'b':2, 'c':3}` |
| `update(other)` | Update from another dict/iterable. | `d.update({'b':4})` → `{'a':1, 'b':4}` |
| `pop(k, default=None)` | Remove/return `k`'s value. | `val = d.pop('a')` → `val=1` |
| `del d[k]` | Delete key `k`. | `del d['b']` |
| `clear()` | Remove all items. | `d.clear()` → `{}` |
| `fromkeys(keys, value=None)` | Create dict with keys set to value. | `dict.fromkeys(['a','b'], 0)` → `{'a':0, 'b':0}` |

### Example
```python
d = {'a': 1, 'b': 2}
print(d.get('c', 0))  # 0
for k, v in d.items():
    print(k, v)  # a 1\nb 2
```

## Set
Mutable, unordered, unique elements. Elements hashable.

### Creation
| Syntax | Example | Notes |
|--------|---------|-------|
| `set()` | `s = set()` | Empty. |
| `{}` (not for empty) | `s = {1, 2, 3}` | From literals. |
| From iterable | `s = set([1,2,2])` | `{1,2}` (dedupes). |
| Comprehension | `s = {x**2 for x in [1,2,2]}` | `{1,4}` |

### Common Operations/Methods
| Operation | Description | Example |
|-----------|-------------|---------|
| `|` or `union(other)` | Union (all unique). | `{1,2} | {2,3}` → `{1,2,3}` |
| `&` or `intersection(other)` | Intersection (common). | `{1,2} & {2,3}` → `{2}` |
| `-` or `difference(other)` | Difference (in first, not second). | `{1,2} - {2,3}` → `{1}` |
| `^` or `symmetric_difference(other)` | XOR (in one but not both). | `{1,2} ^ {2,3}` → `{1,3}` |
| `add(x)` | Add `x`. | `s.add(4)` → `{1,2,4}` |
| `remove(x)` | Remove `x` (KeyError if missing). | `s.remove(1)` |
| `discard(x)` | Remove `x` (no error if missing). | `s.discard(5)` |
| `pop()` | Remove/return arbitrary item. | `val = s.pop()` |
| `clear()` | Remove all. | `s.clear()` → `set()` |

### Example
```python
s1 = {1, 2}
s2 = {2, 3}
print(s1 | s2)  # {1,2,3}
s1.add(4)  # {1,2,4}
```

## Tuple
Immutable, ordered sequence. Allows duplicates. Indexed.

### Creation
| Syntax | Example | Notes |
|--------|---------|-------|
| `()` or `tuple()` | `t = ()`<br>`t = tuple([1,2])` | Empty or from iterable. |
| Literal | `t = (1,)` (single)<br>`t = (1,2,3)` | Comma for single. |
| Comprehension (unpack) | N/A (immutable, no direct comp). | Use list comp then `tuple()`. |

### Access & Slicing
- Same as List: `t[0]`, `t[1:3]`, `len(t)`.
- Unpacking: `a, b = t` (if len=2).

### Common Methods
- Limited: `count(x)`, `index(x)`.
- No mutation methods (immutable).

### Example
```python
t = (1, 2, 2)
print(t.count(2))  # 2
a, b = t[:2]  # a=1, b=2
```

## Range
Immutable sequence of numbers. Efficient for loops (lazy).

### Creation
| Syntax | Example | Notes |
|--------|---------|-------|
| `range(stop)` | `r = range(5)` | 0 to 4. |
| `range(start, stop[, step])` | `r = range(1, 6, 2)` | 1,3,5 (step=2). |
| Negative step | `r = range(5, 0, -1)` | 5,4,3,2,1. |

### Access
- Index: `r[0]`, `r[-1]`.
- Length: `len(r)`.
- Iterate: `for i in r: ...`
- Convert: `list(r)` → `[0,1,2,3,4]`.

### Example
```python
r = range(3)
print(list(r))  # [0,1,2]
print(r[1])  # 1
```

## Enumerate
Built-in function: Returns iterator of (index, value) pairs for iterable.

### Syntax
`enumerate(iterable, start=0)`

### Example
```python
fruits = ['apple', 'banana']
for i, fruit in enumerate(fruits, start=1):
    print(i, fruit)  # 1 apple\n2 banana
```

- Use: Looping with indices without manual counter.

## Iterator
Object implementing `__iter__()` (returns self) and `__next__()` (returns next item, raises StopIteration at end).

### Creation
- Most collections: `iter(lst)`.
- Custom: Define class with `__iter__` and `__next__`.

### Usage
```python
it = iter([1,2,3])
print(next(it))  # 1
print(next(it))  # 2
# next(it) → 3, then StopIteration
```

- Protocol: Enables `for` loops, list comps.
- One-time use: Exhausts on iteration.

## Generator
Lazy iterator via functions with `yield`. Memory-efficient for large sequences.

### Creation
- Function with `yield`: `def gen(): yield 1; yield 2`
- Expression: `(x**2 for x in range(5))`
- Sendable: `yield from` for sub-generators.

### Common Operations
- `next(gen)`: Yield next value.
- Iterate: `for val in gen(): ...`
- Close: `gen.close()`.

### Example
```python
def squares(n):
    for i in range(n):
        yield i**2

g = squares(3)
print(next(g))  # 0
print(list(g))  # [1, 4]

# Expression
evens = (x for x in range(10) if x % 2 == 0)
print(list(evens))  # [0,2,4,6,8]
```

### Key Differences Summary
| Type | Mutable? | Ordered? | Duplicates? | Indexed? | Use Case |
|------|----------|----------|-------------|----------|----------|
| List | Yes | Yes | Yes | Yes | Ordered collections. |
| Dict | Yes | Yes (3.7+) | Keys: No | No | Key-value mapping. |
| Set | Yes | No | No | No | Unique, fast membership. |
| Tuple | No | Yes | Yes | Yes | Immutable records. |
| Range | No | Yes | No (unique nums) | Yes | Efficient numeric sequences. |

For more, see Python docs (e.g., `help(list)` in REPL). Test snippets in interactive shell!
