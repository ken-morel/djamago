from djamago import *


def test_parse():
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
    queries = iter(("hello", "what is chemistry", "wsqdklqsd", "what is bio", "good morning ama"))
    for q in queries:
        node = chatbot.respond(q)


if __name__ == '__main__':
    test_parse()
