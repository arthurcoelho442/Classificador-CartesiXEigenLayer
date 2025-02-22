import tensorflow as tf

arquivo = './backup/classificador'

model = tf.keras.models.load_model(arquivo+'.h5')

converter = tf.lite.TFLiteConverter.from_keras_model(model)
tflite_model = converter.convert()

with open(arquivo+".tflite", "wb") as f:
    f.write(tflite_model)