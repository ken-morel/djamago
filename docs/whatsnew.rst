===============================================================================
What's new?
===============================================================================

-------------------------------------------------------------------------------
v0.0.2
-------------------------------------------------------------------------------

- **Added supports for named exprssions**: with the new expression syntax, now
  an expression can be named.
- **Improved expression checking errors**: Added name propositions, and error
  messages.
- **Added builtin expressions**: Now Djamago implements builtin expressions
  prefixed with a `-`.
- **Added .next to Node**: You can now easily specify precisely which method
  will follow.
- **simplified node**: now node implements all the session data including
  variables, parameters, score and candidates.
- **Added ScoreChange**: raise this in a callback to assign to it a new
  score and recheck.
