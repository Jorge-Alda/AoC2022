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

### Day 08

Debugging Rust with the extension [CodeLLDB](https://marketplace.visualstudio.com/items?itemName=vadimcn.vscode-lldb).

### Day 09

* Implementing `From` to convert to a custom enum/struct

```rust
use std::convert::From;

struct MyStruct {
  //...
}

impl MyStruct {
  fn From<i32>(x: i32) -> Self {
    //...
  }
}
```

* Appending the content of a vector into other vector:

```rust
let mut v1 = vec![1, 2, 3];
let mut v2 = vec![4, 5, 6];

v1.append(&mut v2);
assert_eq![v1, vec![1, 2, 3, 4, 5, 6]];
assert_eq![v2, []];
```

Note that the copied vector needs to be passed as `&mut`, as it will be emptied by `append`.

### Day 13

* Using `serde_json` to parse a list of values and store it in a `Value`.

* `impl`-ementing the `PartialOrd` and `Ord` traits to compare and sort `struct`s or `enum`s.
  * Traits cannot be implemented in objects defined in a different file.
