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

Have you ever used `chatbot AI <https://pypi.org/project/chatbotAI/>`_
It is a python module for creating chatting robots.

I used chatbotai since it was extremely difficult to use ai powerred modules
like  `chatterbot <https://pypi.org/project/chatterbot/>`_ which could not
install on my pc, or trying to generate them myself using torch or tensorflow.

Djamago provides a simple, bulky but personalized approach to that
by adding support for some parsing like tools.

Djamago deeply uses `djamago <https://pypi.org/project/djamago>`_
and so will you see in the examples

If you want to create a little chatbot, with simple and clear code... I will
discourage you, It still appears that code with `djamago` is still somehow
bulky or junk, but I'm working on that.

# How works

![flow.png](flow.png)


## Setting up Expressions

During this steps, the several expressions and dataset to be used are loaded to
djamago, happens such: `Expression.register(name: str, list[tuple[score, regex]])`

###### Expressions.py
```python
# Extract from pango
from djamago import Expression


question = lambda re: (
    fr"(?:.*(?:please|question.?)? ?{re}\??)"
    fr"|(?:may )?i ask you {re}\??"
)  # Formulate the passed RegEx as a question

Expression.register("whois", [
    (100, r"(?:who is) (.*)"),
    (30, r"(?:do you know) (.*)"),
    # Score, regex
])
Expression.register("greetings", [
    (100, r"hello ?(.*)?"),
    (100, r"good (?:morning|evening|night|after-?noon) ?(.*)?"),
    (70, r"greetings ?(.*)?"),
    (20, r"good day ?(.*)?"),
])
Expression.register("name", [
    (70, r"((?:[\w_\-]+)+ ?)"),
])
```

<details>
    <summary>Full code</summary>
    <code language="python" lang="python" >
        from djamago import Expression

        question = lambda re: (
            fr"(?:.*(?:please|question.?)? ?{re}\??)"
            fr"|(?:may )?i ask you {re}\??"
        )

        Expression.register("R", [
            (100, r"(.*)"),
        ])
        Expression.register("whois", [
            (100, r"(?:who is) (.*)"),
            (30, r"(?:do you know) (.*)"),
        ])
        Expression.register("whatis", [
            (100, r"(?:what is) (.*)"),
            (50, r"(?:tell me.? ?(?:djamago)? what is) (.*)"),
        ])
        Expression.register("greetings", [
            (100, r"hello"),
            (100, r"good (?:morning|evening|night|after-?noon)"),
            (70, r"greetings"),
            (20, r"good day"),
        ])
        Expression.register("callyou", [
            (100, question(r"how do you call yourself")),
            (100, fr"(?:tell me.? ?(?:djamago)? what is) (.*)"),
            (100, question(r"what is your name")),
            (100, question(r"how can I call you")),
        ])
        Expression.register("askingMyname", [
            (100, question(
                r"(?:how can (?:i|we) call you|what is your name|who are you|"
                r"how (?:do you|can you|are)? (?:call you|called))"
            )),
        ])
        Expression.register("username", [
            (100, question(r"(?:do you (?:know|remember))?(?: ?what is)? ?my name")),
        ])
        Expression.register("whoMadeMe", [
            (100, question(r"who (?:created|programmed|made|coded|trained) you")),
        ])
        Expression.register("name", [
            (100, r"[\w\d_\- \@]+"),
        ])

        Expression.register("aboutAUser", [
            (50,
                question(
                    r"(?:do you know(?: about)?|who is|tell me about"
                    r"|are you familiar with) ([\w\-_]+)"
                )
            )
        ])
    </code>
</details>

> [!WARNING]
> Expressions are registered globaly, so if you wan't to create an extension
  use prefixed names to prevent conflicts


## Adding topics

###### topics.py

we create a topic simply by subclassing the topic class:

```python
class Biology(djamago.Topic):
    pass
```

### Adding callbacks

To add callbacks we simply define a method we will decorate with a `djamago.Callback`
instance, it will automatically register the method

> [!TIP]
> You could change the handler for a callback simply by calling it over an other
  method

The Callback receives as argument a list of `djamago.Pattern` instances.

example

```python
class Biology(Topic):
    @Callback([
        (100, Expression("greetings(name)"))
    ])
    def greeted(node: Node):
        node.set_topics(("biology", "faq"))  # Set topics for the consecutive queries
        node.response = "Hello %s!" % node.vars.get("name", "You")

    @Callback([
        (0, RegEx(".*"))  # 0 not to override other answers
    ])
    def anything(node: Node):
        # not Setting topics will use parent topics
        node.response = random.choice([
            "Sorry, I did not understand",
            "Could you reformulate, please"
        ])
```

## Adding Faqs

You have a good database of questions and answers?, here how to add it.

`djamago.QA` is a `djamago.Topic` subclass which permit adding QAs of
FAQs into the djamago bot. The QA should be a list containing  tuple
of questions, or question scores (`tuple[str] | tuple[tuple[float, str]]`)
and a list of answers djamago will choose randomly.
you may define a `format_response`, which will process the node
before it is returned.

There are few ways to create a QA:

### Using data attribute

Here the list of QAs are already parsed and stored as a list:

```python
class Faq(QA):
    data = [
        (
            ("what is biology",),
            ("The study of live things",),
        ),
        (
            (
                (70, "what is chemistry"),
            ),
            ("The study of chemical things",),
        ),
    ]

    def format_response(node):
        node.response = f"score: {node.score:5.2f}%\n" + node.response
```

### Using json file:

```python
class Faq(djamago.QA):
    source_json = "faqs.json"

    def format_response(node):
        ...
```

> [!TIP]
> To use `nltk` python features, call `pyoload.use_nltk(True)`, it will make
  sure the required tools are installed before modifying the setting globally

### Using yaml file, (easier to read)

If you want an easy to read markup you will edit yourself, this the way forward

Make sure you have yaml installed(`pip install PyYAML`), then create a yaml file:

```yaml
%YAML 1.2
---
- - - what is biology
    - what is the intent of biology
  - |
    Biology is the study of living things
  - |
    I do not know...
- - - why sbook
    - why creating sbook
    - what is the need of sbook
    - who needs sbook
    - why do we need sbook
  - |
    It have been noticed by [UNESCO](https://unesco.org) that a high number
    of children could not have acces to quality education, due to factors
    like:

    - Instability, political or location
    - Risks or Security due to threats as Thieves, or bullies.
    - Lack of infrastructure for building schools
    - Defficient curricula leading to incomplete learning.

    Reason why we @Antimony; crated Sbook, A web platform
- - - Who created Sbook
  - |
    Sbook web platform and mobile app were two created by @Antimony;
```

Then, you are all set!!, let's join all of that into a Djamgo instance

## Running the app

### Subclassing Djamago
We will simply sublass djamago

```python
class MyChatbot(Djamago):
    def __init__(self):
        super().__init__("Jane Doe")
```

### Adding the topics

```python
MyChatbot.topic(Biology)
MyChatbot.topic(Faq)
```

### Running it...

```python
chatbot = MyChatbot()

while True:
    query = input("> ")
    node = chatbot.respond(query)
    print(node.response)
```


```
> Good morning ken-morel
Hello ken-morel!
> good after-noon ama
Hello ama!
> what is biology?
72.85533905932736
score: 72.86%
The study of live things
> what is bio
Sorry, I did not understand
> what is chemistry
Could you reformulate, please
>
```


<details>
    <summary>Full source</summary>
<code>
    from djamago import *

    use_nltk()


    question = lambda re: (
        fr"(?:.*(?:please|question.?)? ?{re}\??)"
        fr"|(?:may )?i ask you {re}\??"
    )  # Formulate the passed RegEx as a question

    Expression.register("whois", [
        (100, r"(?:who is) (.*)"),
        (30, r"(?:do you know) (.*)"),
        # Score, regex
    ])
    Expression.register("greetings", [
        (100, r"hello ?(.*)?"),
        (100, r"good (?:morning|evening|night|after-?noon) ?(.*)?"),
        (70, r"greetings ?(.*)?"),
        (20, r"good day ?(.*)?"),
    ])
    Expression.register("name", [
        (70, r"((?:[\w_\-]+)+ ?)"),
    ])


    class Biology(Topic):
        @Callback([
            (100, Expression("greetings(name)"))
        ])
        def greeted(node: Node):
            node.set_topics(("biology", "faq"))  # Set topics for the consecutive queries
            node.response = "Hello %s!" % node.vars.get("name", "You")

        @Callback([
            (0, RegEx(".*"))  # 0 not to override other answers
        ])
        def anything(node: Node):
            node.set_topics(("biology", "faq"))  # Set topics for the consecutive queries
            node.response = random.choice([
                "Sorry, I did not understand",
                "Could you reformulate, please"
            ])


    class Faq(QA):
        data = [
            (
                ("what is biology",),
                ("The study of live things",),
            ),
            (
                (
                    (70, "what is chemistry"),
                ),
                ("The study of chemical things",),
            ),
        ]

        def format_response(node):
            node.response = f"score: {node.score:5.2f}%\n" + node.response


    class MyChatbot(Djamago):
        def __init__(self):
            super().__init__("Jane Doe")


    MyChatbot.topic(Biology)
    MyChatbot.topic(Faq)

    chatbot = MyChatbot()
    while True:
        query = input("> ")
        node = chatbot.respond(query)
        print(node.response)

</code>
</details>
