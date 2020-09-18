# Competitive Programming Snippet Generator for VSCode

A tool to easily create VSCode snippets for competitive programming. This tool allows you to define any number of VSCode snippets and their dependencies on one another. For example, if snippet A depends on the implementation of snippet B, then both snippets will be inserted when you use snippet A.

## How to generate snippets

1. Edit `generate.py`'s `OUTPUT_DIR` variable to direct to your VSCode's snippet directory.
2. Run `python generate.py` to create the snippets.
3. Use the snippets in your editor! The snippets included in this repo are only usable in .CPP files, and can be seen by typing `cpp_` while editing a .CPP file in VSCode.

## How to create your own snippets

1. Create a new file in the `./templates` folder. Insert your desired snippet into that file exactly how you the snippet to appear when you use it in VSCode. An example for a modular inverse implementation can be seen below:

```cpp
int inverse(int a) {
  int x, y;
  int gcd = extended_euclid(a, MOD, x, y);
  // if gcd != 1 then no solution (might not be relevant)
  // if you need x to always be positive, x = (x % MOD + MOD) % MOD
  return x;
}
```

2. Create a new `.schema.xml` file in the `./schemas` folder. This file is what provides all the metadata needed to configure the VSCode snippet. This includes the name of the template file, the prefix of the snippet, display name, description, and any dependencies. An example of for the modular inverse schema file can be seen below:

```xml
<?xml version="1.0"?>
<schema>
  <template name="inv_modulo" prefix="cpp" display-name="Inverse Modulo">
    Returns the modular inverse of a given value using the extended euclidean algorithm.
  </template>
  <dependencies>
    <dependency template-name="ext_euclid" />
  </dependencies>
</schema>
```

## TO-DO

- [] Use an environment variable or input parameter for the VSCode snippet directory rather than editing the python script.
- [] Include more snippets.
