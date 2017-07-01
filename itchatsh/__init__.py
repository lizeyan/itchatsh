import shlex
import itchat


__command_dispatch__ = {}
__instance__ = None
__open_shell__ = False
__version__ = 0.1


def set_open(val=True):
    global __open_shell__
    __open_shell__ = val


def register(command):
    def wrapper(func):
        global __command_dispatch__
        __command_dispatch__[command] = func
        return func
    return wrapper


@itchat.msg_register(itchat.content.TEXT)
def __dispatch__(msg: dict):
    if not __open_shell__ and msg["ToUserName"] != "filehelper":
        return ""
    _msg = shlex.split(msg["Content"])
    command = _msg[0]
    if command not in __command_dispatch__:
        return "unrecognized command \"{cmd}\".".format(cmd=command)
    args, kwargs = parse_options(_msg[1:])
    func = __command_dispatch__[command]
    itchat.send(func(*args, **kwargs), msg["ToUserName"])


def send(msg, to="filehelper"):
    itchat.send(msg, to)


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


def start(login_func=itchat.auto_login, block_thread=False, *args, **kwargs):
    """
    :param login_func: this func will be executed to login
    :param block_thread: block current thread or create a new daemon thread
    :param args: will be passed to login_func
    :param kwargs: will be passed to login_func
    :return:
    """
    login_func(*args, **kwargs)
    itchat.run(blockThread=block_thread)
    global __instance__
    __instance__ = itchat.new_instance()

