# Advent of Code 2022

This year I will try to solve each [puzzle](https://adventofcode.com/2022) in both Python and Rust.

* [Python](Python/README.md)
* [Rust](Rust/README.md)

## Learning Rust

### Day 01

* Read file (shorter way):

```rust
text = include_str!("input");
```

* Convert `str` to numeric types:

  * Annotating the variable:

  ```rust
    let x: u32 = "4".parse().unwrap(); 
  ```

  * Using "turbofish":

  ```rust
    let x = "4".parse::<u32>().unwrap();
  ```

* Operations with iterators, including `sorted`, `rev`, `cartesian_product`, etc

```toml
[dependencies]
itertools = "0.10.5"
```

```rust
use itertools.Itertools;
```

### Day 07

Filtering values from a HashMap needs two de-references: `values()` (or `keys()`, `items()`) return references so not to consume the map, and `filter()` also doesn't consume its arguments:

```rust
use std::collections::HashMap;

let mut map: HashMap<String, u32> = HashMap::new();

//...

let total = map.values().filter(|x| **x > 0).sum();
```
