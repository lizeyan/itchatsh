import itchatsh
import os
import time


@itchatsh.register("ls")
def ls(path="."):
    return "\n".join(os.listdir(path))


if __name__ == '__main__':
    itchatsh.start(hotReload=True)
    while True:
        time.sleep(1)

