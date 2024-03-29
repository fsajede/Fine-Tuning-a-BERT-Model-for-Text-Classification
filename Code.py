# -*- coding: utf-8 -*-

# Instalation

pip install tensorflow

pip install transformers

pip install datasets

# Obtain a BERT model

from transformers import TFAutoModel
bert_model = TFAutoModel. from_pretrained("distilbert-base-uncased")

# Using BERT Tokenizer

from transformers import AutoTokenizer
tokenizer = AutoTokenizer.from_pretrained("distilbert-base-uncased")

# Example:Tokenize using BERTa

tokens = tokenizer.tokenize("The dog is playing.")
tokens

tokens = tokenizer.tokenize("The dog is playing doggygame.")
tokens

# Getting token id

token_ids = tokenizer.convert_tokens_to_ids(tokens)
token_ids

# add [CLS] and [SEP] tokens

tokens = ["[CLS]"] + tokens + ["[SEP]"]
tokens

token_ids = tokenizer.convert_tokens_to_ids(tokens)
token_ids

# direct way to getting token id

t =tokenizer("The dog is playing doggygame.")
t

t['input_ids']

# tokenizing multiple sentence
t = tokenizer(["The dog is playing doggygame.", "The cat is sleeping."])
t

t['input_ids']

# customize tokenization

t = tokenizer(["The dog is playing doggygame.", "The cat is sleeping."],max_length=9,truncation=True)
t

t['input_ids']

# Using pad

t = tokenizer(["The dog is playing doggygame.", "The cat is sleeping."],max_length=9,truncation=True,padding=True)
t

tokenizer.decode(t["input_ids"][0])

tokenizer.decode(t["input_ids"][1])

# Get tokens as np.array

t = tokenizer(["The dog is playing doggygame.", "The cat is sleeping."],max_length=9,truncation=True,padding=True,return_tensors="tf")
t

t['input_ids']

t['attention_mask']

# Getting BERT’s output

output = bert_model(t["input_ids"],attention_mask=t["attention_mask"])
output

output[0].shape

# embeddings of the tokens of the first sequence
output[0][0]

# embedding of the [CLS] token of the first sequence
output[0][0][0]

# embedding of the [CLS] token of the second sequence
output[0][1][0]

# array of embeddings of all [CLS] tokens
output[0][:,0].shape

output[0][:,0]

# obtain a text classification dataset
from datasets import load_dataset
tr_dataset = load_dataset("amazon_polarity", split="train")

tr_dataset

# Get unique label names
label_names = set(example["label"] for example in tr_dataset)

# Print label names
print(label_names)

# first example
tr_dataset[0]

# text of first example
tr_dataset[0] ['content']

# label of first example
tr_dataset[0] ['label']

# using part of dataset
tr_dataset = tr_dataset.shuffle(seed=0)

tokenized_train = tokenizer(tr_dataset["content"][:1000] , max_length=512, truncation=True, padding='max_length', return_tensors="tf")

tokenized_train

from tensorflow.keras.utils import to_categorical

train_y = to_categorical(tr_dataset["label"][:1000])

# Fine-tuning BERT model

import tensorflow as tf
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Input, Dense

bert_model = TFAutoModel.from_pretrained("distilbert-base-uncased")
bert_model.trainable = False

# Set the shapes for input

token_ids = Input(shape=(512,), dtype=tf.int32, name="token_ids")
attention_masks = Input(shape=(512,), dtype=tf.int32, name="attention_masks")

# Set the rest of the model
bert_output = bert_model(token_ids,attention_mask=attention_masks)
dense_layer = Dense(64,activation="relu")(bert_output[0][:,0])
output = Dense(2,activation="softmax")(dense_layer)
model = Model(inputs=[token_ids,attention_masks],outputs=output)

#Seeing the layers of the model

model.summary()

# Compiling the model

model.compile(optimizer="adam", loss="binary_crossentropy", metrics=["accuracy"])

# Training the model

model.fit([tokenized_train["input_ids"],tokenized_train["attention_mask"]], train_y, batch_size=25, epochs=5)

# Evaluating the model

# obtaining and processing test data
tr_dataset_test = load_dataset("amazon_polarity", split="test")
tr_dataset_test = tr_dataset_test.shuffle(seed=0)

tokenized_test= tokenizer(tr_dataset_test["content"][:1000] , max_length=512, truncation=True, padding='max_length', return_tensors="tf")
test_y = to_categorical(tr_dataset_test["label"][:1000])

# evaluationg the model
score = model.evaluate([tokenized_test["input_ids"],tokenized_test["attention_mask"]], test_y, verbose=0)
print('Accuracy on test data:', score[1])

import numpy as np

# Predicting on the test data
predictions = model.predict([tokenized_test["input_ids"], tokenized_test["attention_mask"]])

# Convert predicted probabilities to class labels
predicted_labels = np.argmax(predictions, axis=1)

# Convert one-hot encoded true labels to class labels
true_labels = np.argmax(test_y, axis=1)

# Extracting content and labels from the test dataset
test_content = tr_dataset_test["content"][:1000]
test_labels = tr_dataset_test["label"][:1000]

# Find indices where the model predicted correctly and incorrectly
correct_indices = np.where(predicted_labels == true_labels)[0]
incorrect_indices = np.where(predicted_labels != true_labels)[0]

# Select at least 10 examples the model predicts correctly
correct_samples = [(test_content[i], predicted_labels[i], true_labels[i]) for i in correct_indices[:10]]

# Select at least 10 examples the model predicts incorrectly
incorrect_samples = [(test_content[i], predicted_labels[i], true_labels[i]) for i in incorrect_indices[:10]]

# Print observations
print("Observations on correctly predicted examples:")
for example in correct_samples:
    print(f"Predicted: {example[1]}, True Label: {example[2]}, Content: {example[0]}")

print("\nObservations on incorrectly predicted examples:")
for example in incorrect_samples:
    print(f"Predicted: {example[1]}, True Label: {example[2]}, Content: {example[0]}")

# Predicting on the test data
predictions = model.predict([tokenized_test["input_ids"], tokenized_test["attention_mask"]])

# Convert predicted probabilities to class labels
import numpy as np

predicted_labels = np.argmax(predictions, axis=1)

# Convert one-hot encoded true labels to class labels
true_labels = np.argmax(test_y, axis=1)

# Extracting content and labels from the test dataset
test_content = tr_dataset_test["content"][:1000]
test_labels = tr_dataset_test["label"][:1000]

# Find indices where the model predicted correctly and incorrectly
correct_indices = np.where(predicted_labels == true_labels)[0]
incorrect_indices = np.where(predicted_labels != true_labels)[0]

# Select at least 10 examples the model predicts correctly
correct_samples = [(test_content[i], predicted_labels[i], true_labels[i]) for i in correct_indices[:10]]

# Select at least 10 examples the model predicts incorrectly
incorrect_samples = [(test_content[i], predicted_labels[i], true_labels[i]) for i in incorrect_indices[:10]]

# Print observations
print("Observations on correctly predicted examples:")
for example in correct_samples:
    print(f"Predicted: {example[1]}, True Label: {example[2]}, Content: {example[0]}")

print("\nObservations on incorrectly predicted examples:")
for example in incorrect_samples:
    print(f"Predicted: {example[1]}, True Label: {example[2]}, Content: {example[0]}")

# cosine similarity function
import numpy as np
from math import sqrt
def cosine_similarity(a, b) :
	return np.dot(a,b)/(sqrt(np.dot(a,a))*sqrt(np.dot(b,b)) )

# Define pairs of sentences
sentence_pairs = [
    ["The boy is chasing a ball.", "The girl is napping in the sunlight."],
    ["A car is racing down the track.", "A plane is soaring in the sky."],
    ["The chef is preparing a delicious meal.", "The painter is creating a colorful masterpiece."],
    ["A scientist is conducting experiments in the lab.", "An engineer is designing new technologies."],
    ["A musician is playing a melodic tune.", "A dancer is gracefully moving to the rhythm."],
]

# Calculate and display cosine similarity for each pair
for i, pair in enumerate(sentence_pairs):
    # Tokenize the sentence pair
    t_pair = tokenizer(pair,max_length=30,truncation=True,padding=True,return_tensors="tf")

    # Obtain BERT's contextual embeddings
    output_pair = bert_model(t_pair["input_ids"], attention_mask=t_pair["attention_mask"])

    # Display the contextual embeddings of the first token ([CLS]) for each pair
    print(f"Pair {i + 1}:\nSentence 1: {pair[0]}\nSentence 2: {pair[1]}")

    # Display the contextual embeddings
    emb_1 = output_pair[0][0][2].numpy()  # Change index to the desired embedding
    emb_2 = output_pair[0][1][2].numpy()  # Change index to the desired embedding
    print("Contextual Embedding (Sentence 1):", emb_1)
    print("Contextual Embedding (Sentence 2):", emb_2)

    # Calculate cosine similarity between embeddings
    similarity_score = cosine_similarity(emb_1, emb_2)
    print(f"Cosine Similarity Score: {similarity_score:.4f}\n")

#additional examples

t_pair = tokenizer(['The  car wash is near my apartment.','A plane is soaring in the sky.'],max_length=30,truncation=True,padding=True,return_tensors="tf")

output = bert_model(t_pair["input_ids"], attention_mask=t_pair["attention_mask"])

cosine_similarity(output[0][0][2],output[0][1][2])

t_pair = tokenizer(['He  applied for ','The blue car is beautiful.'],max_length=30,truncation=True,padding=True,return_tensors="tf")

# saving dataset

import pandas as pd

# Load the entire dataset
tr_dataset = load_dataset("amazon_polarity", split="train")

# Convert to a Pandas DataFrame
df = pd.DataFrame(tr_dataset)

# Save the DataFrame to a CSV file
df.to_csv('full_dataset.csv', index=False)
