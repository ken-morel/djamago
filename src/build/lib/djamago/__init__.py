import re

from pyoload import *
from typing import Callable
# from .contrib.spellcheck.correction import correction as text_correction


@annotate
class Pattern:
    pass


@annotate
class ReGex(Pattern):
    def __init__(self, regexs: list[tuple[str | float | int]]):
        scores, res = zip(*regexs)
        res = map(re.compile, res)
        self.regexs = tuple(zip(res, scores))

    def check(self, txt) -> tuple[int | re.Match]:
        ms = []
        for id, (regex, score) in enumerate(self.regexs):
            if m := regex.search(txt):
                ms.append((score, id, m))
        ms.sort(key=lambda m: m[0], reverse=True)
        return ms[0]


@annotate
class Expression(Pattern):
    ENTRIES: dict[str, list[tuple]] = {}

    @classmethod
    def register(cls, name: str, vals: list[tuple[float | int | str]]):
        cls.ENTRIES[name] = [(score, re.compile(txt)) for score, txt in vals]

    @classmethod
    def parse(cls, string):
        if string[0] == ':':
            return re.compile(string[1:-1])
        name = ""
        args = []
        scope = 0
        nin = 0
        for c in string:
            if c == " ":
                continue
            if scope == 0:
                if c.isalpha():
                    name += c
                else:
                    scope = 1
            if scope == 1:
                if nin == 0:
                    if c == "(":
                        nin = 1
                        args.append("")
                        continue
                if nin == 1 and c == ",":
                    args.append("")
                    continue
                if nin == 1 and c == '"':
                    scope = 2
                    args[-1] = ':'
                    continue
                if nin >= 1:
                    if c == "(":
                        nin += 1
                    elif c == ")":
                        nin -= 1
                    args[-1] += c
            elif scope == 2:
                if c == '"':
                    scope = 1
                else:
                    args[-1] += c
        return (name, tuple(map(Expression.parse, args)))

    @classmethod
    def _check(cls, name, params, string):
        # print("requesting expr", name, "params", params, "in", repr(string))
        tests: list[tuple[float | int, dict]] = []
        for id, (score, regex) in enumerate(cls.ENTRIES[name]):
            # print("item:", id, "score:", score, "regex:", regex)
            vars = {}
            mat = regex.search(string)
            if not mat:
                # print("  no match")
                continue
            args = mat.groups()
            # print("match", args, params)
            args = args[:len(params)]
            # print("strip", args)
            if len(params) != len(args):
                # print("     LENGTH DISMATCH")
                continue
            for param, arg in zip(params, args):
                if isinstance(param, tuple):
                    paramname, paramargs = param
                    vars[paramname] = arg
                    # print("    ", (paramname, paramargs), arg)
                    _, pscore, pvars = Expression._check(paramname, paramargs, arg)
                    for k, v in pvars.items():
                        vars[paramname + "." + k] = v
                    if pscore == -1:
                        continue
                    else:
                        score += pscore
                elif isinstance(param, re.Pattern):
                    if param.search(arg):
                        score += 100
                    else:
                        return -1, -1, {}
                else:
                    raise Exception()
            tests.append((score, id, vars))

        if len(tests) == 0:
            return (-1, -1, {})
        else:
            tests.sort(key=lambda k: k[0], reverse=True)
            return tests[0]

    def __init__(self, expr: str):
        self.expr = Expression.parse(expr)

    def check(self, val):
        return Expression._check(*self.expr, val)


@annotate
class Callback:
    __func__: Callable
    pattern: Pattern

    def __init__(self, pattern: "Pattern"):
        self.pattern = pattern

    def __call__(self, func: Callable):
        self.__func__ = func
        if hasattr(func, "overload"):
            self.overload = func.overload
        return self

    def __set_name__(self, obj: type, name: str):
        obj.register(self)
        self.topic = obj

    def __get__(self, obj):
        return self

    def respond(self, node: "Node", id: int = 0, vals=None):
        if not hasattr(self, "__func__"):
            raise RuntimeError("Callable not decorated")
        if vals is None:
            self.__func__(node, *self.pattern.check(node.query)[-2:])
        else:
            self.__func__(node, id, vals)


class Topic:
    _callbacks: list[Callback]
    name: str = None

    @classmethod
    def register(cls, callback: Callback):
        if not hasattr(cls, "_callbacks"):
            cls._callbacks = []
        cls._callbacks.append(callback)

    @classmethod
    def matches(cls, node):
        matches = []
        for callback in cls._callbacks:
            ml, id, vals = callback.pattern.check(node.raw_query)
            if ml >= 0:
                matches.append((ml, callback, id, vals))
        return matches


@annotate
class Node:
    topics: tuple[Topic | str] = ()
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
            query=(query),
        )
        self.respond_node(node)
        self.nodes.append(node)
        return node

    @unannotable
    @respond.overload
    def respond_node(self, node: Node) -> None:
        matches = []
        for topic in node.parent.topics:
            matches.extend(self.topics.get(topic).matches(node))
        matches.sort(key=lambda m: m[0], reverse=True)
        id, var = matches[0][2:4]
        matches[0][1].respond(node, id, var)

    @classmethod
    def topic(cls, topic: type):
        name = topic.name or topic.__name__.lower()
        cls.topics[name] = topic


__version__ = "0.0.1"
