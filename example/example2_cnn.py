import keras
from keras.datasets import mnist
from keras.models import Sequential
from keras.layers import Dense, Dropout, Flatten
from keras.layers import Conv2D, MaxPooling2D
from keras import backend
import itchatsh


@itchatsh.register("lr")
def set_lr(lr="1e-3"):
    global model
    model.lr.set_value(float(lr))
    return "set learning rate to {lr}".format(lr=float(lr))


@itchatsh.register("stop")
def stop():
    global keep_run
    keep_run = False
    return "stop running"


if __name__ == '__main__':
    itchatsh.start(hotReload=True)

    batch_size = 128
    num_classes = 10
    learning_rate = 1e-3
    keep_run = True
    # input image dimensions
    img_rows, img_cols = 28, 28

    # the data, shuffled and split between train and test sets
    (x_train, y_train), (x_test, y_test) = mnist.load_data()

    if backend.image_data_format() == 'channels_first':
        x_train = x_train.reshape(x_train.shape[0], 1, img_rows, img_cols)
        x_test = x_test.reshape(x_test.shape[0], 1, img_rows, img_cols)
        input_shape = (1, img_rows, img_cols)
    else:
        x_train = x_train.reshape(x_train.shape[0], img_rows, img_cols, 1)
        x_test = x_test.reshape(x_test.shape[0], img_rows, img_cols, 1)
        input_shape = (img_rows, img_cols, 1)

    x_train = x_train.astype('float32')
    x_test = x_test.astype('float32')
    x_train /= 255
    x_test /= 255
    print('x_train shape:', x_train.shape)
    print(x_train.shape[0], 'train samples')
    print(x_test.shape[0], 'test samples')

    # convert class vectors to binary class matrices
    y_train = keras.utils.to_categorical(y_train, num_classes)
    y_test = keras.utils.to_categorical(y_test, num_classes)

    model = Sequential()
    model.add(Conv2D(32, kernel_size=(3, 3),
                     activation='relu',
                     input_shape=input_shape))
    model.add(Conv2D(64, (3, 3), activation='relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Dropout(0.25))
    model.add(Flatten())
    model.add(Dense(128, activation='relu'))
    model.add(Dropout(0.5))
    model.add(Dense(num_classes, activation='softmax'))

    model.compile(loss=keras.losses.categorical_crossentropy,
                  optimizer=keras.optimizers.Adam(),
                  metrics=['accuracy'])
    while keep_run:
        model.fit(x_train, y_train,
                  batch_size=batch_size,
                  verbose=1,
                  epochs=1,
                  validation_data=(x_test, y_test))
    score = model.evaluate(x_test, y_test, verbose=0)
    itchatsh.send('Test loss: {loss}'.format(loss=score[0]))
    itchatsh.send('Test accuracy: {accuracy}'.format(accuracy=score[1]))
