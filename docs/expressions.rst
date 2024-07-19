===============================================================================
Registering Expressions
===============================================================================

You can register expressions using `Expression.register` to create a new
expression, or `Expression.extend` to add more patterns to an existing
expression or `Expression.override` to override an existing expression.
`Expression.register`It takes two arguments:

-------------------------------------------------------------------------------
Expression definition
-------------------------------------------------------------------------------

The definition of the expression, it could just be the expression name
as `asking_no-thing@robot`. you could also subclass an existing expression
using the syntax `name(parent1, parent2, ...)`.

-------------------------------------------------------------------------------
Expression patterns
-------------------------------------------------------------------------------

a list of tuples in the for `(score, regex_pattern)`.

The score is a float or integer value between `-1` for no match, passing by `0`
for default match, to `100` for full match

The pattern is simply a string pattern to full match.
The captures of the regex will be used for matching with the arguments when
the expression is inferred.

===============================================================================
Using expressions
===============================================================================

A djamago expression consists of four parts

-------------------------------------------------------------------------------
The pattern
-------------------------------------------------------------------------------

The first and only required part of the expression. It may have two value types

1. **A registerred expression name**: A simple name reference to a list of
  mappings of score to regular epression.
2. **A quoted regular expression**: you could simply quote a regular expression
  and use it in the same way.

-------------------------------------------------------------------------------
The arguments
-------------------------------------------------------------------------------

As a simple function call, the arguments will be fullmatched on the expression
matching groups.
gives something like `how-are(you)`

-------------------------------------------------------------------------------
The match name
-------------------------------------------------------------------------------

Add a hash and a string after the pattern name regex or call arguments,
and the match will be available in the `node.vars` under the specified name.

now like:
- `greetings#greetingMessage`
- `".+"#anything`
- `hello("user")#message`

-------------------------------------------------------------------------------
The match score
-------------------------------------------------------------------------------

Fix a specific score to rescale the score match, use syntax `everyThingElse:{score}`
as in:

- `hello:60.5`
- `'hello':60.5`
- `greetings(".+"#personName:60, ".+"#personName2:40):65`

Well, you are all set to use `djamago.Expression`.
