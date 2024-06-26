# Statistical Methods for Machine Learning: experimental project

[![Pycharm Badge](https://img.shields.io/badge/PyCharm-000000.svg?&style=for-the-badge&logo=PyCharm&logoColor=white)](https://www.jetbrains.com/pycharm/)
[![Pyton Badge](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/downloads/release/python-3105/)
[![Tensorflow Badge](https://img.shields.io/badge/TensorFlow-FF6F00?style=for-the-badge&logo=tensorflow&logoColor=white)](https://www.tensorflow.org)
[![Keras Badge](https://img.shields.io/badge/Keras-FF0000?style=for-the-badge&logo=keras&logoColor=white)](https://keras.io)

Use Keras to train a neural network for the binary classification of muffins and Chihuahuas.

## General Information

- **Python** version is: **3.10.5** (_click on the badge_)
- **requirements.txt** contains all the necessary python packages (_use the command below to install all the pachages_)
```
pip install -r requirements.txt
```
- The file called "SMML_Project_Report" is the document describing the project

## Structure of the project
the architecture of this project is fundamentally organized into four blocks. The initial two blocks are dedicated to preprocessing and data preparation tasks, whereas the latter two blocks are focused on model construction: classification and evaluation.

<picture>
  <img src="https://github.com/Sabaudian/SMML_project/assets/32509505/4b168037-0c91-4363-bcd5-cc720ae99e86">
</picture>

#### A. Preprocessing
In the preprocessing phase, the emphasis is on refining the dataset. The process involves systematically addressing corrupted files, detecting and managing duplicates through image hashing, and conducting a thorough dataset check.

#### B. Data Preparation
In the data preparation phase, the primary focus is on loading and enhancing the dataset. This involves using Keras and TensorFlow to load training, validation, and test datasets, applying data augmentation techniques such as flip, rotation, and zoom, and normalizing pixel values. The goal is to ensure the dataset is well-prepared and suitable for subsequent steps.

#### C. Classification
In the classification phase, a robust image classification pipeline is established using Keras and TensorFlow. The implementation introduces configurable models, including Multilayer Perceptron, Convolutional Neural Network and MobileNet. The workflow seamlessly integrates hyperparameter tuning and K-fold cross-validation for comprehensive model optimization.

#### D. Evaluation
In the evaluation phase, the model’s performance is tested through the presentation of insightful metrics, such as loss and accuracy. The module further generates classification reports, produces confusion matrices, and offers intuitive plots to analyze predictions.

## Performace Summary:

|   | MLP | CNN | MOBILENET | 
| --- | --- | --- | --- |
| Accuracy (%)  | 71.537 | 94.510 | 99.493 |
| Loss  | 0.573 | 0.222 | 0.019 |

The models exhibit varying degrees of performance, with MobileNet emerging as the
standout performer, achieving near-perfect accuracy and classification proficiency.
The CNN model also demonstrates notable results. The MLP model performs worse
than its counterparts, exhibiting suboptimal performance characterized by higher loss
resulting in a notable rate of misclassification.
