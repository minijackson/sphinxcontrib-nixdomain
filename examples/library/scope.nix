{
  /**
    This function is inside a scope!

    The documentation can refer to other function in the same scope,
    it will be resolved, local first, e.g. {func}`myOtherFunc`.

    It can also refer to functions from the parent scope,
    e.g. {func}`myFunc`.
  */
  myScopedFunc = null;

  /**
    This function is also inside a scope!
  */
  myOtherFunc = null;
}
