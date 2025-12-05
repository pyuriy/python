# Python Collections Cheat Sheet

Concise reference for Python 3.x built-in collections and iterables: List, Dictionary, Set, Tuple, Range, Enumerate, Iterator, Generator. Extended with Deque, Counter, DefaultDict, NamedTuple.

## List
```python
lst = []                          # Empty list.
lst = list(iterable)              # From iterable (e.g., list("abc") → ['a','b','c']).
lst = [x**2 for x in range(5)]    # List comprehension → [0,1,4,9,16].
item = lst[index]                 # Access (0-based; -1 for last). Raises IndexError.
lst[index] = value                # Assign (mutable).
slice = lst[start:end:step]       # Slice (end exclusive; step ±1 default). E.g., lst[::-1] reverses.
length = len(lst)                 # Number of elements.
lst.append(item)                  # Add item to end.
lst.extend(iterable)              # Add all from iterable to end (or lst += iterable).
lst.insert(index, item)           # Insert item at index (shifts right).
lst.remove(item)                  # Remove first occurrence (raises ValueError if missing).
item = lst.pop(index=-1)          # Remove/return item at index (default end).
index = lst.index(item)           # Index of first occurrence (raises ValueError if missing).
count = lst.count(item)           # Number of occurrences.
lst.sort(key=None, reverse=False) # Sort in-place (key for custom sort).
lst.reverse()                     # Reverse in-place.
sorted_lst = sorted(lst)          # New sorted list.
reversed_it = reversed(lst)       # Iterator over reversed list.
max_val = max(lst)                # Largest element (or min(lst)).
sum_val = sum(lst)                # Sum of elements (or math.prod for product).
flattened = [item for sub in lst for item in sub]  # Flatten nested list.
```

## Dictionary
```python
d = {}                            # Empty dict.
d = dict(key1=val1, key2=val2)    # From keyword args.
d = {k: v for k, v in pairs}      # Dict comprehension (pairs iterable of (k,v)).
d = dict.fromkeys(keys, default)  # Keys with default value.
value = d[key]                    # Access (raises KeyError if missing).
value = d.get(key, default=None)  # Access with default.
d[key] = value                    # Set/overwrite value (mutable).
d.update(other_dict)              # Update from another dict/iterable of pairs.
value = d.pop(key, default=None)  # Remove/return value (default if missing).
del d[key]                        # Delete key (raises KeyError).
keys = d.keys()                   # View of keys (dynamic).
values = d.values()               # View of values (dynamic).
items = d.items()                 # View of (key,value) tuples (dynamic).
d.clear()                         # Remove all items.
```

## Set
```python
s = set()                         # Empty set ({} is empty dict).
s = {1, 2, 3}                     # From literals (unique, unordered).
s = set(iterable)                 # From iterable (deduplicates).
s = {x**2 for x in range(5)}      # Set comprehension → {0,1,4,9,16}.
item in s                         # Membership test (O(1) avg).
s.add(item)                       # Add item (ignores duplicates).
s.remove(item)                    # Remove item (raises KeyError if missing).
s.discard(item)                   # Remove item (no error if missing).
item = s.pop()                    # Remove/return arbitrary item.
union = s1 | s2                   # Union (or s1.union(s2)).
intersect = s1 & s2               # Intersection (or s1.intersection(s2)).
diff = s1 - s2                    # Difference (in s1 not s2; or s1.difference(s2)).
sym_diff = s1 ^ s2                # Symmetric difference (or s1.symmetric_difference(s2)).
s1.issubset(s2)                   # True if s1 ⊆ s2.
s1.issuperset(s2)                 # True if s1 ⊇ s2.
s.clear()                         # Remove all items.
```

## Tuple
```python
t = ()                            # Empty tuple.
t = (1,)                          # Single-element (comma required).
t = (1, 2, 3)                     # From literals.
t = tuple(iterable)               # From iterable.
item = t[index]                   # Access (immutable; 0-based).
slice = t[start:end:step]         # Slice.
length = len(t)                   # Number of elements.
count = t.count(item)             # Number of occurrences.
index = t.index(item)             # Index of first occurrence (raises ValueError).
a, b, c = t                       # Unpack (if lengths match).
```

## Range
```python
r = range(stop)                   # 0 to stop-1.
r = range(start, stop, step=1)    # Arithmetic sequence (step can be negative).
item = r[index]                   # Access (efficient).
length = len(r)                   # (stop - start + step - 1) // step (adjusted for sign).
list_r = list(r)                  # Convert to list.
for i in r: ...                   # Iterate lazily (memory-efficient).
```

## Enumerate
```python
enum = enumerate(iterable, start=0)  # Iterator of (index, item) tuples.
for index, item in enumerate(lst):   # Loop with indices.
    print(f"{index}: {item}")
# Output: 0: a, 1: b, etc.
```

## Iterator
```python
it = iter(iterable)               # Get iterator from iterable.
item = next(it)                   # Get next item (raises StopIteration at end).
item = next(it, default)          # With default instead of exception.
for item in it: ...               # Consume iterator.
# Custom: class MyIter: def __iter__(self): return self; def __next__(self): ...
```

## Generator
```python
def gen_func():                   # Generator function.
    yield 1
    yield 2
g = gen_func()
item = next(g)                    # 1, then 2, then StopIteration.
for item in g: ...                # Iterate (lazy, memory-efficient).
# Expression: gen_expr = (x**2 for x in range(5))  # (0,1,4,9,16) lazily.
list_g = list(g)                  # Consume to list [1,2].
g.close()                         # Close generator (raises GeneratorExit).
# yield from: def subgen(): yield 3; def gen(): yield 1; yield from subgen(); yield 2
```

## Deque (from collections)
```python
from collections import deque
dq = deque()                      # Empty double-ended queue.
dq = deque(iterable)              # From iterable.
dq.append(item)                   # Add to right.
dq.appendleft(item)               # Add to left.
item = dq.pop()                   # Remove/return from right.
item = dq.popleft()               # Remove/return from left.
dq.rotate(n=1)                    # Rotate right by n (negative left).
dq.clear()                        # Remove all.
```

## Counter (from collections)
```python
from collections import Counter
c = Counter("abracadabra")        # Counts elements → {'a':5, 'b':2, ...}.
c = Counter({key: count})         # From dict.
most_common = c.most_common(3)    # Top 3: [('a',5),('r',2),('b',2)].
c['x'] += 1                       # Increment (default 0).
total = sum(c.values())           # Total count.
```

## DefaultDict (from collections)
```python
from collections import defaultdict
dd = defaultdict(list)            # Default factory: list() for missing keys.
dd['key'].append(1)               # Auto-creates [] if missing.
dd = defaultdict(lambda: 0)       # Default 0.
value = dd['missing']             # 0 (no KeyError).
```

## NamedTuple (from collections)
```python
from collections import namedtuple
Point = namedtuple('Point', ['x', 'y'])  # Or Point = namedtuple('Point', 'x y').
p = Point(1, 2)                   # Create instance.
x = p.x                           # Access by name (or p[0]).
p._asdict()                       # To dict {'x':1, 'y':2}.
p._replace(y=3)                   # New instance with y=3.
```

## Key Differences
| Type          | Mutable | Ordered | Duplicates | Indexed | Hashable | Use Case                  |
|---------------|---------|---------|------------|---------|----------|---------------------------|
| List          | Yes    | Yes    | Yes       | Yes    | No      | Dynamic arrays            |
| Dict          | Yes    | Yes*   | Keys: No  | No     | Keys: Yes| Key-value storage         |
| Set           | Yes    | No     | No        | No     | Yes     | Unique elements, sets ops |
| Tuple         | No     | Yes    | Yes       | Yes    | Yes     | Immutable records         |
| Range         | No     | Yes    | No        | Yes    | Yes     | Numeric sequences         |
| Deque         | Yes    | Yes    | Yes       | Yes    | No      | Efficient append/pop ends |
| Counter       | Yes    | No     | N/A       | No     | No      | Element counting          |
| DefaultDict   | Yes    | Yes*   | Keys: No  | No     | Keys: Yes| Dict with defaults        |
| NamedTuple    | No     | Yes    | Yes       | Yes    | Yes     | Structured immutable data |

*Insertion order since Python 3.7.

For more, run `help(collection)` in Python REPL or see docs.python.org.

## 1. Collections

### List
```python
<list> = [<el_1>, <el_2>, ...]  # Creates a list object. Also list(<collection>).
<el>   = <list>[index]          # First index is 0. Last -1. Allows assignments.
<list> = <list>[<slice>]        # Also <list>[from_inclusive : to_exclusive : ±step].
<list>.append(<el>)             # Appends element to the end. Also <list> += [<el>].
<list>.extend(<collection>)     # Appends elements to the end. Also <list> += <coll>.
<list>.sort()                   # Sorts the elements in ascending order.
<list>.reverse()                # Reverses the order of list's elements.
<list> = sorted(<collection>)   # Returns a new list with sorted elements.
<iter> = reversed(<list>)       # Returns reversed iterator of elements.
<el>  = max(<collection>)       # Returns largest element. Also min(<el_1>, ...).
<num> = sum(<collection>)       # Returns sum of elements. Also math.prod(<coll>).
elementwise_sum  = [sum(pair) for pair in zip(list_a, list_b)]
sorted_by_second = sorted(<collection>, key=lambda el: el[1])
sorted_by_both   = sorted(<collection>, key=lambda el: (el[1], el[0]))
flatter_list     = list(itertools.chain.from_iterable(<list>))
<int> = len(<list>)             # Returns number of items. Also works on dict, set and string.
<int> = <list>.count(<el>)      # Returns number of occurrences. Also `if <el> in <coll>: ...`.
<int> = <list>.index(<el>)      # Returns index of the first occurrence or raises ValueError.
<el>  = <list>.pop()            # Removes and returns item from the end or at index if passed.
<list>.insert(<int>, <el>)      # Inserts item at passed index and moves the rest to the right.
<list>.remove(<el>)             # Removes first occurrence of the item or raises ValueError.
<list>.clear()                  # Removes all list's items. Also works on dictionary and set.
```

### Dictionary
```python
<dict> = {key_1: val_1, key_2: val_2, ...}      # Use `<dict>[key]` to get or set the value.
<view> = <dict>.keys()                          # Collection of keys that reflects changes.
<view> = <dict>.values()                        # Collection of values that reflects changes.
<view> = <dict>.items()                         # Coll. of key-value tuples that reflects chgs.
value  = <dict>.get(key, default=None)          # Returns default argument if key is missing.
value  = <dict>.setdefault(key, default=None)   # Returns and writes default if key is missing.
<dict> = collections.defaultdict(<type>)        # Returns a dict with default value `<type>()`.
<dict> = collections.defaultdict(lambda: 1)     # Returns a dict with default value 1.
```

*(Note: Due to length, further sections like Set, Tuple, etc., follow a similar concise code-snippet style. For the complete exhaustive list, refer to the source.)*
