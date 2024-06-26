from djamago import Expression

question = lambda re: (
    fr"{re}|"
    fr"(?:(?:please|question.?)? ?{re}\??)|"
    fr"(?:may )?i ask (?:you )?{re}\??"
)


Expression.register("whois", [
    (100, r"(?:who is) (.*)"),
    (30, r"(?:do you know) (.*)"),
])
Expression.register("name", [
    (50, r"[\w\- ]+(?: [\w\- ]+)*")
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
    (100, question(r"how can i call you")),
])
