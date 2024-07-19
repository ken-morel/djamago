from __init__ import *
import random


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
    [
        (100, r"what\s*time\s*is\s*it(?:\s*now)"),
        (100, r"que\s*es\s*la\s*hora"),
        (70, r"time please"),
    ],
)


class Chatbot(Djamago):
    def __init__(self):
        super().__init__("John Doe", topics="main")


@Chatbot.topic
class Main(Topic):
    @Callback(r"greetings")  # matches greetings
    def greet(node):
        print(node.score)
        node.response = "Hy"

    @Callback(
        r"greetings_to('.+'#collected_name)"  # matches greetings_to, to regex
    )  # and store match as colletced_name
    def greet_to(node):
        print(node.score)
        node.response = (
            "Hy! (from " + node.vars.get("collected_name", "bot") + ")"
        )

    @Callback(r"question('how are you.*')")
    def how_are_you(node, cache={}):
        if "asked" not in cache:
            node.response = (
                "I am a bot. you know I cannot feel bad. Nor fine too :cry: "
                "but I will say I feel fine, and you?"
            )
            cache["asked"] = True
            node.set_topics("howareyou")
        else:
            node.response = random.choice(
                (
                    "I do not know, you tell me, How am I?",
                    "you again and that question!",
                    "why not doing something completely different now?",
                    "Cameroon government calls, `CHANGE TOPIC`",
                )
            )


@Chatbot.topic
class HowAreYou(Topic):
    @Callback(r"'.*(?:fine|well|ok|nice).*'")
    def feel_fine(node):
        node.response = "feel fine, that is good!, Well letá change topic"
        node.set_topics("main")


bot = Chatbot()
msg = ""
while msg != "quit":
    print(bot.respond(msg := input("> ")).response)
