from djamago import Topic, Expression, Callback, ReGex
from pyoload import *


@annotate
class Main(Topic):
    @Callback(Expression("greetings"))
    def morning(node: "Node", id: Values((0, 1, 2)), vars):
        if id == 0:
            node.response = "Hy"
            node.topics = ("main",)
        elif id == 1:
            node.response = node.query + ", How are you?"
            node.topics = ("greet",)
            return node
        elif id == 2:
            node.response = "How strange greetings!"
            node.topics = ("main",)
            return node
        return node

    @Callback(Expression('whois(name)'),)
    def whois(node, id, var):
        if var.get("name").lower() == "djamago":
            node.response = "Djamago?, it's me!"
        else:
            node.response = "I do not know %s, you tell me" % var.get('name')
        node.topics = ("main",)
        return node

    @Callback(Expression('callyou'),)
    def callyou(node, id, var):
        node.response = {
            "Ow, can call me djamago",
            "Call me djamago",
            "I am called djamago"
        }.pop()
        node.topics = ("main", "djamago")
        return node

    @Callback(
        ReGex(
            [
                (0, r".*"),
            ]
        )
    )
    def hello(node, id, match):
        node.response = "Did not understand"
        node.topics = ("main",)
        return node
