import shlex
import itchat


__command_dispatch__ = {}

__instance__ = None


def register(command):
    def wrapper(func):
        global __command_dispatch__
        __command_dispatch__[command] = func
        return func
    return wrapper


@itchat.msg_register(itchat.content.TEXT)
def __dispatch__(msg: dict):
    _msg = shlex.split(msg["Content"])
    command = _msg[0]
    if command not in __command_dispatch__:
        return "unrecognized command \"{cmd}\".".format(cmd=command)
    args, kwargs = parse_options(_msg[1:])
    func = __command_dispatch__[command]
    return func(*args, **kwargs)


def parse_options(opts: list):
    args = []
    kwargs = {}
    current_key_word = None
    for opt in opts:
        if opt.startswith("--"):
            current_key_word = opt.lstrip("-")
            continue
        if current_key_word is None:
            args.append(opt)
            continue
        if current_key_word not in kwargs:
            kwargs[current_key_word] = opt
            continue
        if not isinstance(kwargs[current_key_word], list):
            kwargs[current_key_word] = [kwargs[current_key_word]]
        kwargs[current_key_word].append(opt)
    return args, kwargs


def start(login_func=itchat.login):
    login_func()
    itchat.run(blockThread=False)
    global __instance__
    __instance__ = itchat.new_instance()

