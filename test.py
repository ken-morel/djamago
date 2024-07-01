import re


def parse(
    string: str,
) -> tuple:
    """
    Expression.parses the passed Expression into tuples of
    (call, score, args)
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
        if c == ",":
            i += 1
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
                            if string[i] == "(":
                                snin += 1
                            elif string[i] == ")":
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
                if string[i] == "(":
                    nin += 1
                elif string[i] == ")":
                    nin -= 1
                call += string[i]
                i += 1
            args.append(parse(call))
            while i < len(string) and string[i] in ", ":
                i += 1
    i -= 1
    return (name, score, tuple(args))

print(parse('amas:3(name,"am","am":3,"kd",ama("dkd"))'))
