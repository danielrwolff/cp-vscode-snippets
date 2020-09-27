# Competitive Programming Snippet Generator for VSCode

A tool to easily create VSCode snippets for competitive programming. This tool allows you to define any number of VSCode snippets and their dependencies on one another. For example, if snippet A depends on the implementation of snippet B, then both snippets will be inserted when you use snippet A.

## How to generate snippets

1. Edit `generate.py`'s `OUTPUT_DIR` variable to direct to your VSCode's snippet directory.
2. Run `python generate.py` to create the snippets. Python 3.X is required.
3. Use the snippets in your editor! The snippets included in this repo are only usable in .CPP files, and can be seen by typing `cpp_` while editing a .CPP file in VSCode.

## How to create your own snippets

1. Create a new file in the `./templates` folder, with no file extension. The name of this file will correspond to the suffix of the snippet shortcut. Insert your desired snippet into that file exactly how you want the snippet to appear when you use it in VSCode. An example for a modular inverse implementation can be seen below:

```cpp
int inverse(int a) {
  int x, y;
  int gcd = extended_euclid(a, MOD, x, y);
  // if gcd != 1 then no solution (might not be relevant)
  // if you need x to always be positive, x = (x % MOD + MOD) % MOD
  return x;
}
```

2. Add an entry to the `config.yaml` file located in the root directory of the repo. Order of entries don't matter!

| Field        | Description                                                                                                                                                          |
| ------------ | -------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Name         | The name of the template file.                                                                                                                                       |
| Prefix       | The prefix to add to the snippet (will prepend the Name field, separated by an underscore. )                                                                         |
| Display      | The display name for the snippet.                                                                                                                                    |
| Description  | The description of the snippet.                                                                                                                                      |
| Dependencies | A list of template names that this snippet depends on (uses). The templates listed here will be included in this snippet, prepended to this snippets implementation. |

An example of a `config.yaml` file for the inverse modulo example above:

```yaml
- Name: ext_euclid
  Prefix: cpp
  Display: Extended Euclidean Algorithm
  Description: Calculates the GCD of A and B while also determining the coefficients for each.

- Name: inv_modulo
  Prefix: cpp
  Display: Inverse Modulo
  Description: Returns the modular inverse of a given value using the extended euclidean algorithm.
  Dependencies: [ext_euclid]
```

## TO-DO

- [x] Use an environment variable or input parameter for the VSCode snippet directory rather than editing the python script.
- [ ] Include more snippets.
