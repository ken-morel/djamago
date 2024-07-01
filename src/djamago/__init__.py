"""
djamago is a python library which will help you create simple chatbots
the simple way. It uses regular expressions to match queries and
provide a response with the best match
"""

import re

from pyoload import *
from typing import Callable

# from .contrib.spellcheck.correction import correction as text_correction


@annotate
class Pattern:
    def __init__(*_, **__):
        raise NotImplementedError()


@annotate
class Evaluator(Pattern):
    def __init__(self, func):
        self.__func__ = func

    def check(
        self, node: 'Node'
    ) -> tuple[int | float, int, dict[str | re.Pattern, str]]:
        val, var = self.__func__(node)
        return (val, 0, var)


@annotate
class RegEx(Pattern):
    """
    Provides the base for regex pattern matching
    """

    @multimethod
    def __init__(self: Pattern, regex: list[tuple[float | int, str]]):
        """
        Initializes a new Regular expression as Pattern
        :param regex: a list of tuples (score, regular expression)
        which will be used to match
        """
        scores, res = zip(*regexs)
        res = map(re.compile, res)
        self.regexs = tuple(zip(res, scores))

    @multimethod
    def __init__(self: Pattern, regex: str, score: int | float = 100.0):
        """
        Initializes a new Regular expression as Pattern
        :param regex: the regex
        which will be used to match
        """
        pattern = re.compile(regex)
        self.regexs = [(score, pattern)]

    def check(self: "RegEx", node: 'Node') -> tuple[int | float, int, re.Match]:
        """
        Compares all the RegEx's stored on initialization to the string
        and if matching, returns the score and match object associated

        :param txt: The string to test
        :returns: A tuple (score, match Object)
        """
        ms = []
        for id, (score, regex) in enumerate(self.regexs):
            if m := regex.search(node.query):
                ms.append((score, id, m))
        ms.sort(key=lambda m: m[0], reverse=True)
        return ms[0]


@annotate
class Expression(Pattern):
    """
    Expression class to create a new expression, in the form

    """
    ENTRIES: dict[str, list[tuple]] = {}

    @classmethod
    @annotate
    def register(
        cls,
        name: str,
        vals: list[tuple[float | int, str]],
    ) -> None:
        """
        Registers a new expression
        :param name: The name under which to register the expression
        :param vals: a list of tuples in the form (score, regex)
        """
        cls.ENTRIES[name] = [(score, re.compile(txt)) for score, txt in vals]

    @staticmethod
    def parse(
        string: str,
    ) -> tuple[str | re.Pattern, int | float, tuple | re.Pattern]:
        """
        Expression.parses the passed Expression into tuples of (call, args)
        :param string: The string to Expression.parse

        :returns: The Expression.parsed expression tuple
        """
        global indent
        name = ""
        has_args = True
        i = 0
        while i < len(string):
            c = string[i]
            if c.isalnum() or c == ":":
                name += c
                i += 1
            else:
                break
        else:
            has_args = False
        if ":" in name:
            name, score = name.rsplit(":", 1)
            score = int(score)
        else:
            score = 100
        if not has_args:
            return (name, score, ())
        i, string = 0, string[i + 1:]
        args = []
        while i < len(string):
            c = string[i]
            if c == ")":
                break
            elif c == '"':  # A string argument
                sargs = []
                nin = 0
                i += 1
                regex = ""
                while i < len(string):  # collecting string
                    if string[i] == "(":
                        nin += 1
                    elif string[i] == ")":
                        nin -= 1
                    if nin == 0 and string[i] == '"':  # end of string
                        if len(string) > i + 1 and string[i + 1] == ":":
                            # then it is followed by score
                            i += 2  # skip score
                            sscore = ""
                            while i < len(string) and string[i].isnumeric():
                                # next score digit
                                sscore += string[i]
                                i += 1
                            sscore = int(sscore)
                        else:
                            sscore = 100  # no score in expr
                            i += 1
                        if string[i] == "(":
                            scall = ""  # store whole call here
                            snin = 0
                            while i < len(string):
                                if snin == 0 and string[i] == ")":
                                    i += 1
                                    break
                                if string[i] == '(':
                                    snin += 1
                                elif string[i] == ')':
                                    snin -= 1
                                scall += string[i]
                                i += 1
                            sargs = Expression.parse("a" + scall)[2]
                            while i < len(string) and string[i] in ", ":
                                i += 1
                        break
                    else:
                        regex += string[i]
                        i += 1
                args.append((re.compile(regex), sscore, tuple(sargs)))
            elif c.isalpha():  # other call
                call = ""  # store whole call here
                nin = 0
                while i < len(string):
                    if nin == 0 and string[i] == ")":
                        i += 1
                        break
                    if string[i] == '(':
                        nin += 1
                    elif string[i] == ')':
                        nin -= 1
                    call += string[i]
                    i += 1
                args.append(Expression.parse(call))
                while i < len(string) and string[i] in ", ":
                    i += 1
        i -= 1
        return (name, score, tuple(args))

    @classmethod
    @annotate
    def _check(
        cls, name: str | re.Pattern, nscore, params: tuple[tuple | re.Pattern], string: str
    ) -> tuple[int | float, int, dict[str | re.Pattern, str]]:
        tests = []
        if isinstance(name, str):
            try:
                regexs = cls.ENTRIES[name]
            except KeyError:
                raise ValueError(f"Expression {name!r} does not exist")
        elif isinstance(name, re.Pattern):
            regexs = [(100, name)]
        for id, (score, regex) in enumerate(regexs):
            vars = {}
            mat = regex.search(string)
            if not mat:
                continue
            args = mat.groups()
            args = args[:len(params)]
            if len(params) != len(args):
                continue
            match_score = 0
            for param, arg in zip(params, args):
                if isinstance(param, tuple):
                    paramname, paramscore, paramargs = param
                    vars[str(paramname)] = arg
                    pscore, _, pvars = Expression._check(
                        paramname,
                        paramscore,
                        paramargs,
                        arg,
                    )
                    for k, v in pvars.items():
                        vars[paramname + "." + k] = v
                    if pscore == -1:
                        continue
                    else:
                        match_score += pscore / 100 * score
                elif isinstance(param, re.Pattern):
                    if param.search(arg):
                        match_score += 100
                    else:
                        return -1, -1, {}
                else:
                    raise Exception()
            if len(params) == 0:
                match_score = 100
            tests.append((match_score / 100 * nscore, id, vars))

        if len(tests) == 0:
            return (-1, -1, {})
        else:
            tests.sort(key=lambda k: k[0], reverse=True)
            return tests[0]

    def __init__(self, expr: str):
        self.expr = Expression.parse(expr)

    def check(self, node: 'Node') -> _check.__annotations__.get("return"):
        return Expression._check(*self.expr, node.query)


class Callback:
    __func__: Callable
    pattern: Pattern

    @overload
    def __init__(
        self, patterns: "list[tuple[int | float, Pattern]]"
    ):
        self.patterns = patterns

    @overload
    def __init__(
        self, pattern: Pattern
    ):
        self.patterns = [(100, pattern)]

    @annotate
    def __call__(self, func: Callable) -> "Callback":
        self.__func__ = func
        if hasattr(func, "overload"):
            self.overload = func.overload
        return self

    def __set_name__(self, obj: Type, name: str) -> None:
        obj.register(self)
        self.topic = obj

    def __get__(self, obj: "Topic") -> "Callback":
        return self

    @annotate
    def respond(
        self, node: "Node", id: int = 0, vals=None, cpid: int = 0
    ) -> None:
        if not hasattr(self, "__func__"):
            raise RuntimeError("Callable not decorated")
        if vals is None:
            self.__func__(node, *self.patterns[cpid][1].check(node.query)[-2:])
        else:
            self.__func__(node, id, vals)

    @annotate
    def check(
        self, node: "Node"
    ) -> "list[tuple]":
        matches = []
        for cpid, (pscore, pattern) in enumerate(self.patterns):
            ml, id, vals = pattern.check(node)
            if ml >= 0:
                matches.append(
                    (cpid, ml / 100 * pscore, self, id, vals)
                )
        return matches


class Topic:
    _callbacks: list[Callback]
    name: str = None

    @classmethod
    def register(cls, callback: Callback):
        if not hasattr(cls, "_callbacks"):
            cls._callbacks = []
        cls._callbacks.append(callback)

    @classmethod
    def matches(
        cls, node: 'Node'
    ) -> tuple[int, float | int, Callback, int, dict[str, str]]:
        matches = []
        for callback in cls._callbacks:
            matches.extend(callback.check(node))
        return matches


@annotate
class Node:
    topics: tuple[tuple[int | float, str] | str] = ()
    parent: "Node | type(None)"
    response: str | type(None)
    query: str

    def __init__(
        self,
        query: str,
        raw_query: str,
        topics: tuple[str] = ("main",),
        parent: "Node | type(None)" = None,
        response: str = None,
    ):
        self.topics = topics
        self.parent = parent
        self.response = response
        self.query = query
        self.raw_query = raw_query

    def __str__(self):
        return f"<djamado.Node({self.query!r}) -> {self.response!r}>"


@annotate
class Djamago:
    topics: dict[str, Topic]
    nodes: list[Node]
    name: str

    def __init_subclass__(cls):
        cls.topics = {}

    def __init__(self, name: str = ""):
        self.name = name
        self.nodes = [
            Node(
                parent=None,
                query="",
                raw_query="",
                response="",
                topics=("main",),
            )
        ]

    @unannotable
    @overload
    def respond(self, query: str) -> Node:
        node = Node(
            parent=self.nodes[-1],
            raw_query=query,
            query=query.lower(),
        )
        self.respond_node(node)
        self.nodes.append(node)
        return node

    @unannotable
    @respond.overload
    def respond_node(self, node: Node) -> None:
        matches = []
        for topic in node.parent.topics:
            if isinstance(topic, tuple):
                score, topic = topic
            else:
                score = 100
            matches.extend([
                (s / 100 * score, c, cpid, i, v)
                for cpid, s, c, i, v in self.topics.get(topic).matches(node)
            ])
        matches.sort(key=lambda m: m[0], reverse=True)
        if len(matches) == 0:
            raise ValueError("Node did not find any match")
        cpid, id, var = matches[0][2:5]
        matches[0][1].respond(node, id, var, cpid)

    @classmethod
    def topic(cls, topic: type):
        name = topic.name or topic.__name__.lower()
        cls.topics[name] = topic


__version__ = "0.0.1"
