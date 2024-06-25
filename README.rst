.. image:: djamago.png
  :target: https://github.com/ken-morel/djamago

.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
  :target: https://github.com/psf/black


==================================================
Djamago
==================================================

Have you ever used `chatbot AI <https://pypi.org/project/chatbotAI/>`_
It is a python module for creating chatting robots.

I used chatbotai since it was extremely difficult to use ai powerred modules
like  `chatterbot <https://pypi.org/project/chatterbot/>`_ which could not
install on my pc, or trying to generate them myself using torch or tensorflow.

Djamago provides a simple, bulky but personalized approach to that
by adding support for some parsing like tools.

Djamago deeply uses `pyoload <https://pypi.org/project/pyoload>`_
and so will you see in the examples

--------------------------------------------------
How works
--------------------------------------------------
![](flow.png)

.. code-block:: python
  from djamago import *


  class Pango(Djamago):
      def __init__(self):
          super().__init__("pango")


  @Pango.topic
  class Main(Topic):
      @overload
      def morning(node: "Node", id: Values((0,)), match: re.Match):
          node.response = "Hy"
          node.topics = ("main", )
          return node

      @overload
      def morning(node: "Node", id: Values((1,)), match: re.Match):
          node.response = match.string + ", How are you?"
          node.topics = ("greet", )
          return node

      @overload
      def morning(node: "Node", id: Values((2,)), match: re.Match):
          node.response = "How strange greetings!"
          node.topics = ("main", )
          return node

      morning = Callback(ReGex([
          (100, r"hello"),
          (100, r"good (morning|evening|night|after-?noon)"),
          (20, r"good day"),
      ]))(morning)

      @Callback(ReGex([
          (0, r".*"),
      ]))
      def hello(node, id, match):
          node.response = "Did not understand"
          node.topics = ("main", )
          return node


  @Pango.topic
  class Greet(Topic):
      @Callback(ReGex([
          (0, r".*"),
      ]))
      def dum(node, id, match):
          node.response = "Did you know?..."
          node.topics = ("main", )
          return node


  p = Pango()
  while True:
      print(p.respond(input("> ")).response)
