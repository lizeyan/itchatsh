# ItChatSh

Suppose that there is a deep neural network running on a server, you may want to know the training progress in time and adjust parameters based on the output. ItChatSh makes it convenient to communicate between running python programs and your cellphone(by WeChat). ItChatSh is based on [ItChat](https://github.com/littlecodersh/ItChat).
 
 
## Install

## Usage

``` python
import itchatsh
import os
import time

@itchatsh.register("ls")
def ls(path="."):
    return "\n".join(os.listdir(path))

if __name__ == '__main__':
    itchatsh.start(hotReload=True, block_thread=True)
```