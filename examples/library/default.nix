{
  /**
    Compute the addition of `a` and `b`.

    :type: `a :: int -> b :: int -> int`
    :param int a: the first number to add
    :param int b: the second number to add
    :returns: `a` and `b` added together

    :::{rubric} Example usage:
    :::

    ``` nix
    lib.myFunc 2 2
    # => 4
    ```
  */
  myFunc = a: b: a + b;

  /**
    Same as {func}`myFunc`,
    but with `a` and `b` given as an attribute set.

    :type: `{ a :: int; b :: int; } -> int`
    :param int a: the first number to add
    :param int b: the second number to add
    :returns: `a` and `b` added together
  */
  myOtherFunc = { a, b }: a + b;

  scope = import ./scope.nix;
}
