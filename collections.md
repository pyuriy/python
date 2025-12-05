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
