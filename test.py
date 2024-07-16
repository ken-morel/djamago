import re


text = "hello('world'#world:50, name:25, other(name)#other)#15"


class Expression:
    class ParsingError(ValueError):
        def __init__(self, begin, end, msg):
            self.params = (begin, end, msg)
            super().__init__(msg.format(begin, end))

        def moved(self, num: int):
            return self.__class__(
                self.params[0] + num, self.params[1] + num, self.params[2]
            )

    STRING_QUOTES = "'\""
    NAME_CHARS = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_-"
    ENTRIES = {"hello": "hello world"}

    @staticmethod
    def parse(text: str):
        score = 100
        pos = 0
        args = []
        name = ""

        intersection = set(Expression.STRING_QUOTES) & set(Expression.NAME_CHARS)
        if len(intersection) != 0:
            raise RuntimeError(
                f"found common characters {intersection} between djamago.Expression.STRING_QUOTES and djamago.Expression.NAME_CHARS"
            )

        text = text.strip()

        if text[pos] in Expression.STRING_QUOTES:  # Is a string liretal
            begin = pos + 1  # Index after quote
            end = (
                text[begin:].find(text[pos]) + begin
            )  # find quote after first, then add back index
            while text[end - 1] == "\\":
                text = text[end - 1 : end]
                begin2 = end + 1
                end = text[begin2:].find(text[pos]) + begin2

            if end - begin == -1:
                raise Expression.ParsingError(
                    begin,
                    end,
                    "Expression regex string literal began at {0} but never closed",
                )
            elif end - begin == 0:
                raise Expression.ParsingError(
                    begin, end, "empty expression string at {1}"
                )
            else:
                regex = re.compile(text[begin:end])
                pos = end + 1
        elif text[pos] in Expression.NAME_CHARS:
            end = begin = pos
            while len(text) > end and text[end] in Expression.NAME_CHARS:
                end += 1
            regex = Expression.ENTRIES.get(text[begin:end])
            if regex is None:
                raise Expression.ParsingError(
                    begin,
                    end,
                    "expression '"
                    + text[begin:end]
                    + "' never registerred at {0} to {1}",
                )
            pos = end
        if len(text) > pos and text[pos] == "(":  # arguments
            pos += 1
            still_args = True
            while len(text) > pos and still_args:  # a loop for each arg
                stack: list[int] = []  # the expression stack
                begin = pos
                if text[pos] == " ":
                    pos += 1
                    continue
                elif text[pos] == ")":
                    pos += 1
                    break
                for pos in range(begin, len(text)):
                    if text[pos] in "," and len(stack) == 0:  # a closing character
                        pos += 1
                        break
                    elif text[pos] in ")" and len(stack) == 0:
                        still_args = False
                        pos += 1
                        break
                    elif text[pos] == " " and len(stack) == 0:
                        continue
                    elif text[pos] == "(":
                        stack.append(pos)
                    elif text[pos] == ")":
                        stack.pop()
                if len(stack) > 0:
                    raise Expression.ParsingError(
                        stack[-1],
                        pos,
                        "brace opened at {0} never closed",
                    )
                try:
                    end = pos
                    parsed = Expression.parse(text[begin:end])
                except Expression.ParsingError as e:
                    raise e.moved(begin) from e
                else:
                    args.append(parsed)
        if len(text) > pos and text[pos] == "#":
            begin = pos = pos + 1
            while len(text) > pos and text[pos] in Expression.NAME_CHARS:
                pos += 1
            end = pos
            name = text[begin:end]
        if len(text) > pos and text[pos] == ":":
            begin = pos = pos + 1
            while len(text) > pos and text[pos].isnumeric():
                pos += 1
            end = pos
            score = int(text[begin:end])
        return (regex, args, name, score)
