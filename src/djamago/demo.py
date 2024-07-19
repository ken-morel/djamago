from __init__ import *


Expression.register(
    "greetings(-greetings)",  # Subclass the predefined -greetings
    [],
)

Expression.register(
    "greetings_to(-greetings-to)",  # Subclass the predefined -greetings-to
    [],
)

Expression.register(
    "wanting_current-time",
    [],
)


class Main(Topic):
    @Callback(Expression("greetings"))
    def greet(node):
        print(node.score)
        node.response = "Hy"

    @Callback(Expression("greetings_to('name'#collected_name)"))
    def greet_to(node):
        print(node.score)
        node.response = (
            "Hy.(from " + node.vars.get("collected_name", "bot") + ")"
        )


class Chatbot(Djamago):
    def __init__(self):
        super().__init__("John Doe")


Chatbot.topic(Main)


bot = Chatbot()
msg = ""
while msg != "quit":
    print(bot.respond(msg := input("> ")).response)
