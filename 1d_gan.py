# -*- coding: utf-8 -*-
"""1D GAN.ipynb
Original file is located at
    https://colab.research.google.com/drive/1vtV7H_bw4Mz5UNCipm2O-OcEZcfc9ixP

Implemented by Muhammad Hanan Asghar
"""

# Commented out IPython magic to ensure Python compatibility.
import matplotlib.pyplot as plt
import numpy as np
# %matplotlib inline

def generate_samples(n=100):
  X1 = np.random.rand(n) - 0.5
  X2 = X1 * X1
  X1 = X1.reshape(n, 1)
  X2 = X2.reshape(n, 1)
  return np.hstack((X1, X2))

data = generate_samples()
plt.scatter(data[:, 0], data[:, 1])
plt.show()

"""#Discriminator"""

from keras.models import Sequential
from keras.layers import Dense
from keras.utils.vis_utils import plot_model

def define_discriminator(n_inputs=2):
  model = Sequential()
  model.add(Dense(25, activation="relu", kernel_initializer="he_uniform",
                  input_dim=n_inputs))
  model.add(Dense(1, activation="sigmoid"))
  model.compile(loss="binary_crossentropy", optimizer="adam", metrics=["accuracy"])
  return model

model = define_discriminator()

model.summary()

def generate_real_samples(n): #[-0.5, 0.5], # = 1
  X1 = np.random.rand(n) - 0.5 #inputs
  X2 = X1 * X1 #outpus
  X1 = X1.reshape(n, 1)
  X2 = X2.reshape(n, 1)
  X = np.hstack((X1, X2))
  y = np.ones((n, 1))
  return X, y

def generate_fake_samples(n): #[-1, 1], # = 0
  X1 = -1 + np.random.rand(n) * 2 # inputs
  X2 = -1 + np.random.rand(n) * 2 # outpus
  X1 = X1.reshape(n, 1)
  X2 = X2.reshape(n, 1)
  X = np.hstack((X1, X2))
  y = np.zeros((n, 1))
  return X, y

def train_discriminator(model, n_epochs=1000, n_batch=128):
  half_batch = int(n_batch / 2)
  for i in range(n_epochs):
    # generate real examples
    X_real, y_real = generate_real_samples(half_batch)
    # train model on real values
    model.train_on_batch(X_real, y_real)
    # generate fake examples
    X_fake, y_fake = generate_fake_samples(half_batch)
    # train model on fake values
    model.train_on_batch(X_fake, y_fake)

    _, acc_real = model.evaluate(X_real, y_real, verbose=0)
    _, acc_fake = model.evaluate(X_fake, y_fake, verbose=0)
    print(i, acc_real, acc_fake)

model = define_discriminator()
train_discriminator(model)

"""#Generator"""

def define_generator(latent_dim, n_outputs=2):
  model = Sequential()
  model.add(Dense(15, activation="relu", kernel_initializer="he_uniform",
                  input_dim=latent_dim))
  model.add(Dense(n_outputs, activation="linear"))
  return model

model = define_generator(5)
model.summary()

def generate_latent_points(latent_dim, n):
  x_input = np.random.randn(latent_dim * n)
  x_input = x_input.reshape(n, latent_dim)
  return x_input

def generate_fake_samples_g(generator, latent_dim, n):
  x_input = generate_latent_points(latent_dim, n)
  x = generator.predict(x_input)
  plt.scatter(x[:, 0], x[:, 1])
  plt.show()

latent_dim = 5
model = define_generator(5)
generate_fake_samples_g(model, 5, 100)

