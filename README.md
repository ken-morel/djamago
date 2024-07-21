[![](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![PyPI package](https://badge.fury.io/py/djamago.svg)](https://pypi.org/project/djamago)
[![Supported Python versions](https://img.shields.io/pypi/pyversions/djamago)](https://pypi.org/project/djamago)
[![Test](https://github.com/ken-morel/djamago/actions/workflows/test.yml/badge.svg)](https://github.com/ken-morel/djamago/actions/workflows/test.yml)
[![Coverage Status](https://coveralls.io/repos/github/ken-morel/djamago/badge.svg?branch=main&cache=3000)](https://coveralls.io/github/ken-morel/djamago?branch=main)
[![Documentation Status](https://readthedocs.org/projects/djamago/badge/?version=latest)](https://djamago.readthedocs.io)
[![Pypi downloads](https://img.shields.io/pypi/dd/djamago)](https://pypi.org/project/djamago)
[![Pypi downloads](https://img.shields.io/pypi/dw/djamago)](https://pypi.org/project/djamago)
[![Pypi downloads](https://img.shields.io/pypi/dm/djamago)](https://pypi.org/project/djamago)

<p align="center">
    <h1>Djamago</h1>
    <img src="https://github.com/ken-morel/djamago/blob/main/djamago.png?raw=true" alt="djamago logo" />
</p>

# Djamago

Hello, i am glad, to present to you **djamago**! :clap:

Djamago is:
- a python module :heavy_check_mark:
- a chatbot robot library :heavy_check_mark:
- my class 3's second classmate name :heavy_check_mark:

> [!NOTE]
> Sorry for the emojis, just install a new sublime plugin and really glad test it.
> I am also fun of letting AI generate titles for me. :smirk:

# Break away from the pack

What make Djamago unique from some other projects like chatbotai or chatterbot:

## Unmoor from ML-Imposed Orthodoxy

Sorry, but it is not sort of an AI which you can fine tune in 3 lines of code
to chat with your customers :cry: (I don't find the sad emoji, sorry). But that feature makes it pretty simple
to run on low performance systems or servers(like a vercel free instance), or with some fixes I will be ready
to care of, running on web browsers using brython.js(just made little tests).

## Score-Driven Regular Expression Matching for Enhanced Input Validation

Imagine two callbacks, `wantto` and `ishungry`.
`wantto("eat")` matches _I want to eat_, but `ishungry` matches that to!.
In this simple case we could simply check ishungry before wantto, but lets see how djamago does fix.

Djamago uses a score based matching, permiting you to create an expression, e.g `greetings`,
map it to a set of scores to regular expressions, and infer the names.
That promotes **DRY** style permiting your code to be less repetitive.

Example, I could register

```python
Expression.register("question", [
    (100, r"please (.+)\?"),  # perfect match
    (90, r"please (.+)"),  # missing interrogation point!, bit faulty.
    (20, r"(.+)\?"),  # just an interrogation point at the end
])

Expression.register("whatis", [
    (100, r"what is (.+)"),  # perfect match
    (70, r"do you know what is (.+)")  # step backwards
])
```

and infer them as: `question(whatis("my name"))`
It will check the patterns as given and return the match with tha maximum score on match, or `-1`.

# Enter the Demo Zone

Well, let's now explore the demo and see how it does:

```python
from djamago.demo import cli

cli()
```

```
> good morning
Hy
> what time is it
We are a Saturday and it is: 12:57
> what day are we
We are a Saturday and it is: 12:57
> how are you
I am a bot. you know I cannot feel bad. Nor fine too :cry: but I will say I feel fine, and you?
> fine
feel fine, that is good!, Well lets change topic
```


# Building a chatbot, quickstart

## fiat `expressions(in latin!)`

One basic components of djamago are expressions, what are?
In normal mode you may like to use regular expressions to match phrases
expressions permit you to map a list of mappings of scores to regular
expressions, which will then be evaluated so when used.

```python
Expression.register("I@hungry", [
    (100, r"i am hungry!?"),  # he is hungry, perfect
    (60, r"i want to eat"),  # should not override 'i want' expression, so 60
])
Expression.register("him@hungry", [
    (100, r"he is hungry!?"),  # he is hungry, perfect
    (60, r"he wants to eat"),  # should not override 'i want' expression, so 60
])
Expression.register("somebody-hungry(am-hungry, his-hungry)", [ # inherits definitions
    ...
])
Expression.alias("hungryness", "his-hungry")
Expression.override("somebody-hungry", [
    (99, r"(.+) is hungry!?"),  # not to override him@hungry
    (59, r"(.+) wants to eat"),  # same thing here
])
```

> [!NOTE]
> The capturing groups of these regex expressoins will be used later to further
> match expression arguments.

## Using expressions

Djamago has sort of special syntax for using expressions, is

```
Expression name   optional epression   optional storing
or simple regex        arguments          name alias
       |                  /              /          _ optional score
       |                 /              /          /
somebody-hungry ( "my friend" )   #statement  : 100
       |              |              /          /
      /              /              x          x
"doing (.+)"(".+"#something)
```

simple regexs are quoted, and the name aliases specified after the hash
will be available in `node.vars` attribute.

if i-love maps to `"i love (.+)"` then examples:

- `i-love('python')` gives `i love(python)`
- `i-love('.+'#name_of_what_i_love)` gives `i love (.+)` and stores capture as *name_of_what_i_love*
- `'.+'` matches anything

you can nest such function like calls and add more, many more things


##
