import expressions  # Expressions

from djamago import *
# from topics import djamago  # topics
from topics import main


class Pango(Djamago):
    def __init__(self):
        super().__init__("pango")  # chatbot name


Pango.topic(main.Main)
# Pango.topic(djamago.Djamago)


p = Pango()
while True:
    print(p.respond(input("> ")).response)
