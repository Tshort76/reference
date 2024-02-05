## Key ideas
- Compiled with strong static typing
- Imperative with functional aspects (? functional aspects)
- No garbage collection or run time
- Generics 'resolved' at compile time to type optimized code
- References are immutable by default
  - specific types (e.g. Atoms) exist for mutable collections
  - There can only ever be 1 mutable OR arbitrarily many immutable references to any given value at any given time

- Algebraic Data types, good generics, and pattern matching ... helps deal with the annoying aspects of types that make them get in the way

### Generics
When Rust compiles *generic* (<T>) code, it performs a process called *monomorphization*. We write generic code that works for some arbitrary type T, and Rust generates specific uses of the code by filling in the concrete types at compile time. For example, it will generate (optimized) code for Vec<i32> and separate code for Vec<&str>.  Unfortunately, this means that there cannot be pre-built libraries that can be linked; libraries must be compiled at the same time as your source code!

Rust’s package manager and build tool, Cargo, makes it
easy to use libraries published by others on Rust’s public
package repository, the crates.io website.
# Tooling
Rust’s package manager and build tool, Cargo, makes it easy to use libraries published by others on Rust’s public package repository, the crates.io website.

# Sources
Programming Rust, Second Edition by Jim Blandy, Jason Orendorff, and Leonora F.S. Tindall (O’Reilly)
