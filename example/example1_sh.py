import itchatsh
import os


@itchatsh.register("ls")
def ls(path="."):
    return "\n".join(os.listdir(path))


if __name__ == '__main__':
    itchatsh.start(hotReload=True, block_thread=True)

