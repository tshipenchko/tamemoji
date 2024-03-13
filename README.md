# Tamemoji: Handwritten Emoji Recognition
# [video report](https://youtu.be/REMOVED)
# [application available online](https://tamemoji.zxc.sx/)

Tamemoji is a project aimed at recognizing and classifying handwritten emojis. This project is developed using Python, FastAPI, TensorFlow, Keras, and React.js. The main goal is to provide a new user interface for typing emojis, especially on mobile devices with touch screens.

## Project Overview

The project involves the development of a web application for handwritten emoji classification. The application allows users to draw emojis, send the drawings of emojis, and predict the drawn emoji using a machine learning model. The source code of the project is available on [GitHub](https://github.com/tshipenchko/tamemoji/).

## Data Collection

Data collection is facilitated through an online game where participants draw emojis. We have collected about 2500 images in 12 classes (emojis). The full dataset is available at Google Drive.

## Machine Learning Models

The project predominantly employs Convolutional Neural Network (CNN) architectures for the task of recognizing hand-drawn emojis. CNNs are specifically chosen for their adeptness in processing image data, particularly in capturing intricate spatial features that are crucial for distinguishing between different classes of emojis.

## Results

The model with a resolution of 128x128 pixels demonstrated the most favorable performance with a final test accuracy of 63.26%. The raw data along with the code can be accessed in our [GitHub repository](https://github.com/tshipenchko/tamemoji/blob/master/jupyter/resize_test.ipynb). The final trained model is uploaded to the [releases](https://github.com/tshipenchko/tamemoji/releases/tag/1.0.0) on GitHub repository.

## Future Work

- Expansion of the dataset to include a wider variety of emojis and handwriting styles.
- Creating a browser extension for typing emojis using hard drawn emoji search with our model.

For more detailed information, please refer to the full project report.
