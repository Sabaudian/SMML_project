# Import
import os
import numpy as np
import pandas as pd
import tensorflow as tf
import keras_tuner as kt

from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.applications.mobilenet import MobileNet

from sklearn.model_selection import KFold

# My import
import plot_functions
import constants as const
import prepare_dataset as prepare
import utils.general_functions as general

from models_evaluation import collect_hyperparameters_tuning_data, get_hyperparameters_search_info, evaluate_model


# *********************************************************************** #
# ************* CLASSIFIER MODELS DEFINITION AND EVALUATION ************* #
# *********************************************************************** #

# MLP model
def build_mlp_model(hp):
    """
    Build a Multi-Layer Perceptron (MLP) model with tunable hyperparameters.

    Notes:
        - The function constructs a sequential model with multiple hidden layers, each consisting of dense,
          batch normalization, and dropout layers.
        - The number of units in each hidden layer is determined by the hyperparameter search space.
        - The output layer has a single unit with sigmoid activation for binary classification.
        - The learning rate for the optimizer is tuned using the provided HyperParameters object.
        - The model is compiled with the Adam optimizer, binary crossentropy loss, and accuracy metric.
        - The model's architecture is stored and displayed, including a summary printout and a plot of the network
          architecture.

    :param hp: HyperParameters,
        The hyperparameter tuning object.

    :return: tf.keras.Sequential:
        The built MLP model.
    """

    # Construct the MLP model using a sequential architecture
    model = tf.keras.Sequential(name="MultiLayer_Perceptron")

    # Add a flatten layer to convert input data into a one-dimensional array
    model.add(layers.Flatten(input_shape=const.INPUT_SHAPE, name="flatten_layer"))

    # Add four dense layer with ReLU activation and specified number of units
    model.add(layers.Dense(units=256, activation="relu", name="hidden_layer_1"))
    model.add(layers.Dense(units=128, activation="relu", name="hidden_layer_2"))
    model.add(layers.Dense(units=64, activation="relu", name="hidden_layer_3"))
    model.add(layers.Dense(units=32, activation="relu", name="hidden_layer_4"))

    # Define the number of units for the current hidden layer
    units = hp.Int("units", min_value=32, max_value=512, step=32)
    # Add a dense layer with ReLU activation and specified number of units
    model.add(layers.Dense(units=units, activation="relu", name="hidden_layer_5"))

    # Define the value of the dropout rate for the current hidden layer
    dropout_rate = hp.Float("dropout_rate", min_value=0.2, max_value=0.5, step=0.1)
    # Add dropout for regularization to prevent overfitting
    model.add(layers.Dropout(rate=dropout_rate, name="dropout_layer"))

    # Output layer with sigmoid activation for binary classification
    model.add(layers.Dense(units=1, activation="sigmoid", name="output_layer"))

    # Tune the learning rate for the optimizer
    hp_learning_rate = hp.Choice("learning_rate", values=[1e-2, 1e-3, 1e-4])

    model.compile(
        optimizer=tf.keras.optimizers.legacy.Adam(learning_rate=hp_learning_rate),
        loss="binary_crossentropy",
        metrics=["accuracy"]
    )

    # Store and Display the model's architecture
    general.makedir(os.path.join("plot", "MLP"))  # Create the directory
    plot_path = os.path.join("plot", "MLP", "MLP_model_summary_plot.jpg")  # Path to store the plot
    model.summary()  # Print a summary of the network
    # Plot the architecture of the model
    tf.keras.utils.plot_model(model=model, to_file=plot_path, dpi=96)

    return model


# CNN model
def build_cnn_model(hp):
    """
    Build a Convolutional Neural Network (CNN) model with tunable hyperparameters.

    Notes:
        - The model is constructed using a sequential architecture with multiple convolutional layers followed
          by batch normalization, max pooling, and dropout.
        - The number of filters and kernel size for each convolutional layer is predefined.
        - The number of units in the dense layer, dropout rate, and learning rate are tuned using the
          provided HyperParameters object.
        - The output layer consists of a single unit with sigmoid activation, suitable for binary classification tasks.
        - The model is compiled with the Adam optimizer, binary crossentropy loss, and accuracy metric.
        - The model's architecture is stored and displayed, including a summary printout and a plot of the network
          architecture.

    :param hp: HyperParameters,
        The hyperparameter tuning object.

    :return: tf.keras.Sequential:
        The built CNN model.
    """

    # Create a Sequential model
    model = tf.keras.Sequential(name="Convolutional_Neural_Network")

    # First Convolutional layer with 32 filters and a kernel size of (3, 3)
    model.add(layers.Conv2D(filters=32, kernel_size=(3, 3), activation="relu",
                            input_shape=const.INPUT_SHAPE, name="convolution_1"))
    # Batch Normalization for stabilization and acceleration
    model.add(layers.BatchNormalization(name="batch_normalization_1"))
    # MaxPooling layer to reduce spatial dimensions
    model.add(layers.MaxPooling2D(pool_size=(2, 2), name="max_pooling_1"))
    # Add dropout for regularization to prevent overfitting
    model.add(layers.Dropout(rate=0.25, name="dropout_1"))

    # Second Convolutional layer with 32 filters and a kernel size of (3, 3)
    model.add(layers.Conv2D(filters=32, kernel_size=(3, 3), activation="relu", name="convolution_2"))
    model.add(layers.BatchNormalization(name="batch_normalization_2"))
    model.add(layers.MaxPooling2D(pool_size=(2, 2), name="max_pooling_2"))
    model.add(layers.Dropout(rate=0.25, name="dropout_2"))

    # Third Convolutional layer with 32 filters and a kernel size of (3, 3)
    model.add(layers.Conv2D(filters=64, kernel_size=(3, 3), activation="relu", name="convolution_3"))
    model.add(layers.BatchNormalization(name="batch_normalization_3"))
    model.add(layers.MaxPooling2D(pool_size=(2, 2), name="max_pooling_3"))
    model.add(layers.Dropout(rate=0.25, name="dropout_3"))

    # Fourth Convolutional layer with 32 filters and a kernel size of (3, 3)
    model.add(layers.Conv2D(filters=64, kernel_size=(3, 3), activation="relu", name="convolution_4"))
    model.add(layers.BatchNormalization(name="batch_normalization_4"))
    model.add(layers.MaxPooling2D(pool_size=(2, 2), name="max_pooling_4"))
    model.add(layers.Dropout(rate=0.25, name="dropout_4"))

    # Fifth Convolutional layer with 128 filters and a kernel size of (3, 3)
    model.add(layers.Conv2D(filters=128, kernel_size=(3, 3), activation="relu", name="convolution_5"))
    model.add(layers.BatchNormalization(name="batch_normalization_5"))
    model.add(layers.MaxPooling2D(pool_size=(2, 2), name="max_pooling_5"))
    model.add(layers.Dropout(rate=0.25, name="dropout_5"))

    # Sixth Convolutional layer with 128 filters and a kernel size of (3, 3)
    model.add(layers.Conv2D(filters=128, kernel_size=(3, 3), activation="relu", name="convolution_6"))
    model.add(layers.BatchNormalization(name="batch_normalization_6"))
    model.add(layers.MaxPooling2D(pool_size=(2, 2), name="max_pooling_6"))
    model.add(layers.Dropout(rate=0.25, name="dropout_6"))

    # GlobalMaxPooling2D layer for feature extraction and dimensionality reduction
    model.add(layers.GlobalMaxPool2D(name="global_max_pooling"))

    # Flatten layer to transition from convolutional layers to dense layer
    model.add(layers.Flatten(name="flatten"))

    # Define the number of units for the current dense layer
    hp_units = hp.Int("units", min_value=32, max_value=512, step=32)
    # Add a dense layer with ReLU activation and specified number of units
    model.add(layers.Dense(units=hp_units, activation="relu", name="dense_layer_1"))

    # Define the value of the dropout rate
    hp_dropout_rate = hp.Float("dropout_rate", min_value=0.2, max_value=0.5, step=0.1)
    # Add dropout for regularization to prevent overfitting
    model.add(layers.Dropout(rate=hp_dropout_rate, name="dropout_layer"))

    # Output layer with sigmoid activation for binary classification
    model.add(layers.Dense(units=1, activation="sigmoid", name="output_layer"))

    # Tune the learning rate for the optimizer
    hp_learning_rate = hp.Choice("learning_rate", values=[1e-2, 1e-3, 1e-4])

    # Compile the model
    model.compile(
        optimizer=tf.keras.optimizers.legacy.Adam(learning_rate=hp_learning_rate),
        loss="binary_crossentropy",
        metrics=["accuracy"]
    )

    # Store and Display the model's architecture
    general.makedir(os.path.join("plot", "CNN"))  # Create the directory
    plot_path = os.path.join("plot", "CNN", "CNN_model_summary_plot.jpg")  # Path to store the plot
    model.summary()  # Print a summary of the network
    # Plot the architecture of the model
    tf.keras.utils.plot_model(model=model, to_file=plot_path, dpi=96)

    return model


# MobileNet Model
def build_mobilenet_model(hp):
    """
    Build a MobileNet model with tunable hyperparameters.

     Notes:
        - The constructed model includes a flatten layer, a dense layer with tunable number of units,
          batch normalization, dropout, and an output layer with sigmoid activation for binary classification.
        - Hyperparameters for the dense layer units, dropout rate, and learning rate are tuned using the
          provided HyperParameters object.
        - The model is compiled with the Adam optimizer, binary crossentropy loss, and accuracy metric.
        - The model's architecture is stored and displayed, including a summary printout and a plot of the network
          architecture.

    :param hp: HyperParameters,
        The hyperparameter tuning object.

    :return: tf.keras.Sequential:
        The built MobileNet model.
    """

    # Load the MobileNet base model without top layers (include_top=False)
    base_model = MobileNet(weights="imagenet", include_top=False, input_shape=const.INPUT_SHAPE)

    # Freeze the weights of the MobileNet base model
    base_model.trainable = False

    # Create a Sequential model with the MobileNet base model
    model = tf.keras.Sequential(layers=[
        base_model,
        layers.Flatten(name="flatten"),
        layers.Dense(units=hp.Int("units", min_value=32, max_value=512, step=32),
                     activation="relu", name="dense_layer"),
        layers.BatchNormalization(name="batch_normalization"),
        layers.Dropout(hp.Float("dropout_rate", min_value=0.2, max_value=0.5, step=0.1), name="dropout_layer"),
        layers.Dense(units=1, activation="sigmoid", name="output_layer")
    ], name="MobileNet")

    # Tune the learning rate for the optimizer
    hp_learning_rate = hp.Choice("learning_rate", values=[1e-2, 1e-3, 1e-4])

    model.compile(
        optimizer=tf.keras.optimizers.legacy.Adam(learning_rate=hp_learning_rate),
        loss="binary_crossentropy",
        metrics=["accuracy"]
    )

    # Store and Display the model's architecture
    general.makedir(os.path.join("plot", "MobileNet"))  # Create the directory
    plot_path = os.path.join("plot", "MobileNet", "MobileNet_model_summary_plot.jpg")  # Path to store the plot
    model.summary()  # Print a summary of the network
    # Plot the architecture of the model
    tf.keras.utils.plot_model(model=model, to_file=plot_path, dpi=96)

    return model


# ************************************************************* #
# ****************** HYPERPARAMETER TUNING   ****************** #
# ************************************************************* #


# Perform hyperparameter Tuning
def tuning_hyperparameters(model, model_name, x_train, y_train, x_val, y_val, best_model_directory, model_weights_path,
                           show_plot=True, save_plot=True):
    """
    Tuning the hyperparameters of the input model using Keras Tuner (kerastuner).
    The function performs hyperparameter tuning using Keras Tuner's Hyperband algorithm.
    It saves the best model, its hyperparameters, and training history in the "models" directory.

    Notes:
        - This function performs hyperparameter tuning using Keras Tuner Hyperband.
        - It prints information about the model being tuned and creates a directory for the best model.
        - The best model's weights are saved to a file.
        - History of training is plotted and saved.

    :param model: tf.keras.Model, The model to be tuned.
    :param model_name: str, The name of the model.
    :param x_train: numpy.ndarray, The input training data.
    :param y_train: numpy.ndarray, The target training data.
    :param x_val: numpy.ndarray, The input validation data.
    :param y_val: numpy.ndarray, The target validation data.
    :param best_model_directory: str, Path to the best model folder.
    :param model_weights_path: str, Path to the saved weights of the model.
    :param show_plot: bool, Flag indicating whether to display evaluation plots.
        Default is True.
    :param save_plot: bool, Flag indicating whether to save evaluation plots.
        Default is True.


    :returns: None
    """

    # Print about the model in input
    print("\n> " + model_name + " Tuning Hyperparameters:")

    # Create a directory for the best model
    general.makedir(best_model_directory)

    # Tuning model
    tuner = kt.Hyperband(
        hypermodel=model,
        objective="val_accuracy",
        max_epochs=5,
        factor=2,
        overwrite=False,
        directory="models",
        project_name=model_name
    )

    # Prints a summary of the hyperparameters in the search space
    tuner.search_space_summary()

    # Monitor "val_loss" and stop early if not improving
    early_stopping = tf.keras.callbacks.EarlyStopping(monitor="val_loss", patience=3, verbose=1,
                                                      restore_best_weights=True)

    # Performs a search for best hyperparameter configurations.
    tuner.search(
        x_train, y_train,
        epochs=10,
        validation_data=(x_val, y_val),
        callbacks=[early_stopping]
    )

    # Collect hyperparameter during the tuning process
    collect_hyperparameters_tuning_data(model_name=model_name, tuner=tuner)

    # Retrieve the best hyperparameters
    best_hyperparameters = tuner.get_best_hyperparameters()[0]

    # Information about the optimal hyperparameter found during the tuning process
    get_hyperparameters_search_info(model_name=model_name, best_hyperparameters=best_hyperparameters)

    print("\n> Build the model with the optimal hyperparameters and train it on the data for 10 epochs")
    # Build the model with the optimal hyperparameters
    optimal_hp_model = tuner.hypermodel.build(best_hyperparameters)

    # Train the model for 10 epochs
    history = optimal_hp_model.fit(
        x=x_train, y=y_train,
        epochs=10,
        validation_data=(x_val, y_val),
        callbacks=[early_stopping]
    )

    # Serialize model structure to JSON
    model_json = optimal_hp_model.to_json()
    with open(os.path.join(best_model_directory, "best_model.json"), "w") as json_file:
        json_file.write(model_json)

    # Save the best model's weights to the created directory
    optimal_hp_model.save_weights(filepath=model_weights_path)

    # Check if weights have been saved
    if os.path.exists(path=model_weights_path):
        print("\n> The best weights for " + f"{model_name} model were saved successfully!\n")

    # Plot history after tuning
    plot_functions.plot_history(history=history, model_name=model_name,
                                show_on_screen=show_plot, store_in_folder=save_plot)


# *************************************************************** #
# ****************** K-FOLD CROSS-VALIDATION   ****************** #
# *************************************************************** #

def zero_one_loss(y_true, y_pred):
    """
    Compute the zero-one loss metric.
    Returns 1 when y_true != y_pred, 0 otherwise.

    Notes:
        - This function computes the zero-one loss metric, which is commonly used for binary classification tasks.
        - The function converts predicted values and true labels to integers.
        - The zero-one loss value is computed as 1 when there is a misclassification (y_true != y_pred),
          and 0 otherwise.

    :param y_true: tensor, True labels.
    :param y_pred: tensor, Predicted labels.

    :returns: zero_one_loss_value (tensor): Computed zero-one loss.
    """

    # Convert predicted values to integers
    y_pred = tf.cast(y_pred + 0.5, tf.int16)
    # Convert true labels to integers
    y_true = tf.cast(y_true, tf.int16)

    # Compute the absolute difference between true and predicted labels
    diff = tf.math.abs(y_true - y_pred)

    # Check if the absolute difference is not equal to 0
    # Cast the boolean values to int16 to get 1 for mis-classification, 0 for correct classification
    zero_one_loss_value = tf.cast(tf.math.not_equal(x=diff, y=0), tf.int16)

    return zero_one_loss_value


# KFold cross validation function
def kfold_cross_validation(model_name, x_train, y_train, x_val, y_val, k_folds):
    """
    Perform K-fold cross-validation on a Keras model using the zero-one loss metrics.

    Notes:
        - The function initializes directories for model storage
          and handles loading existing models to speed up the process.
        - It utilizes K-Fold Cross-Validation to assess model performance across multiple folds of the data.
        - Training metrics such as loss, accuracy, and zero-one loss are computed and saved for each fold.
        - The average performance metrics across all folds are calculated and saved to a CSV file.
        - Training history plots for each fold are generated and optionally stored.
        - The trained model is saved for future use.

    :param model_name: str, the name of the model.
    :param x_train: numpy.ndarray, Training data features.
    :param y_train: numpy.ndarray, Training data labels.
    :param x_val: numpy.ndarray, Validation data features.
    :param y_val: numpy.ndarray, Validation data labels.
    :param k_folds: int, The number of folds for K-Fold Cross-Validation.

    :return: model (tf.keras.Model): The trained model.
    """
    # Print about the model in input
    print("\n> " + model_name + " KFold Cross-Validation:")

    # Define the path for storing the models
    dir_path = os.path.join("models", "KFold")
    # Create folder
    general.makedir(dir_path)
    # Path to the models' file
    file_path = os.path.join(dir_path, model_name + "_kfold_model.keras")

    # Check if model.keras already exist to speed up the process (move on to evaluation)
    if os.path.exists(path=file_path):

        # Load model from the right folder
        model = tf.keras.models.load_model(filepath=file_path, custom_objects={"zero_one_loss": zero_one_loss})
        print("- Model Loaded Successfully!")
    else:  # if model.keras does not exist -> load model from json then execute k-fold cross-validation

        # Path to the model directory
        best_model_directory = os.path.join("models", model_name, "best_model")

        # Load json and define model
        json_file = open(os.path.join(best_model_directory, "best_model.json"), "r")
        load_model_from_json = json_file.read()
        json_file.close()

        # This is the structure of the best model obtained after tuning
        model = tf.keras.models.model_from_json(json_string=load_model_from_json)

        # Load weight into the model, i.e., the best hyperparameters
        model.load_weights(filepath=os.path.join(best_model_directory, "best_model.weights.h5"))
        print("-- Best weights for " + model_name + " model have been Loaded Successfully!")

        # KFold Cross-Validation function
        kfold = KFold(n_splits=k_folds, shuffle=True)

        # Combine training and validation data for K-fold cross-validation
        X = np.concatenate((x_train, x_val), axis=0)
        Y = np.concatenate((y_train, y_val), axis=0)

        # Initialize lists to save data
        fold_data = []
        fold_history = []

        for fold, (train_idx, val_idx) in enumerate(kfold.split(X)):
            print("\n> Fold {}/{}".format(fold + 1, k_folds))

            X_train, X_val = X[train_idx], X[val_idx]
            Y_train, Y_val = Y[train_idx], Y[val_idx]

            # Create and compile a new instance of the model
            model.compile(
                optimizer=tf.keras.optimizers.legacy.Adam(),
                loss="binary_crossentropy",
                metrics=["accuracy", zero_one_loss]
            )

            # Train the model on the training set for this fold
            history = model.fit(
                X_train, Y_train,
                batch_size=const.BATCH_SIZE,
                epochs=10,
                validation_data=(X_val, Y_val),
                verbose=1
            )

            # Collect training history data for generate a plot later
            fold_history.append(history)

            # Brief evaluation per epoch on validation set
            val_loss, val_accuracy, val_zero_one_loss = model.evaluate(X_val, Y_val, verbose=0)

            # Collect data per fold
            fold_data.append({
                "Fold": fold + 1,
                "Loss": val_loss,
                "Accuracy (%)": val_accuracy * 100,
                "0-1 Loss": val_zero_one_loss
            })

        # Create a pandas DataFrame from the collected data
        fold_df = pd.DataFrame(data=fold_data)

        # Calculate average values
        avg_values = {
            "Fold": "Average",
            "Loss": np.mean(fold_df["Loss"]),
            "Accuracy (%)": np.mean(fold_df["Accuracy (%)"]),
            "0-1 Loss": np.mean(fold_df["0-1 Loss"])
        }

        # Concatenate the average values to the DataFrame
        fold_df = pd.concat(objs=[fold_df, pd.DataFrame([avg_values])], ignore_index=True)

        # Save fold data to csv file
        fold_data_csv_file_path = os.path.join(const.DATA_PATH, f"{model_name}_fold_data.csv")
        fold_df.to_csv(fold_data_csv_file_path, index=False, float_format="%.3f")

        # Plot fold history
        plot_functions.plot_fold_history(fold_history=fold_history, model_name=model_name,
                                         show_on_screen=False, store_in_folder=True)

        # Save the model to the path
        model.save(file_path)

    return model


# ******************************************************** #
# ****************** PROCESS WORKFLOW   ****************** #
# ******************************************************** #


# Organize the various procedures
def classification_procedure_workflow(models, x_train, y_train, x_val, y_val, x_test, y_test, kfold,
                                      show_plot, save_plot):
    """
    Execute the classification procedure workflow.

    :param models: A dictionary containing classification models.
    :param x_train: numpy.ndarray, Training data features.
    :param y_train: numpy.ndarray, Training data labels.
    :param x_val: numpy.ndarray, Validation data features.
    :param y_val: numpy.ndarray, Validation data labels.
    :param x_test: numpy.ndarray, Test data features.
    :param y_test: numpy.ndarray, Test data labels.
    :param kfold: int, The number of folds for K-Fold Cross-Validation.
        Default is 5.
    :param show_plot: bool, Flag indicating whether to display evaluation plots.
        Default is True.
    :param save_plot: bool, Flag indicating whether to save evaluation plots.
        Default is True.

    :returns: None
    """

    # List to collect models data
    all_models_data = []

    # Scroll through the dictionary
    for key, value in models.items():
        # MLP, CNN and MobileNet (String ID)
        model_name = key
        # Models
        model_type = value

        # Best models' folder path
        tuned_model_folder = os.path.join("models", model_name, "best_model")
        # Best models' weights file path
        weight_path = os.path.join(tuned_model_folder, "best_model.weights.h5")

        # Do Tuning if not already done it
        if not os.path.exists(weight_path):
            # Tuning Hyperparameters and Save the Best
            tuning_hyperparameters(model=model_type, model_name=model_name,
                                   x_train=x_train, y_train=y_train, x_val=x_val, y_val=y_val,
                                   best_model_directory=tuned_model_folder, model_weights_path=weight_path,
                                   show_plot=show_plot, save_plot=save_plot)

        # Apply Kfold Cross-validation
        kfold_result = kfold_cross_validation(model_name=model_name,
                                              x_train=x_train, y_train=y_train, x_val=x_val, y_val=y_val, k_folds=kfold)

        # Evaluate the results on the Test set
        data = evaluate_model(model=kfold_result, model_name=model_name, x_test=x_test, y_test=y_test,
                              show_plot=show_plot, save_plot=save_plot)
        all_models_data.append(data)

    # Create a pandas DataFrame
    df = pd.DataFrame(all_models_data)

    # Save the data
    general.makedir(dirpath=const.DATA_PATH)
    file_path = os.path.join(const.DATA_PATH, "Models_Performances_on_Test_Set.csv")
    df.to_csv(file_path, index=False, float_format="%.3f")


# To be called in the main
def classification_and_evaluation(train_path, test_path, show_plot=True, save_plot=True):
    """
    Perform classification and evaluation of models.

    This function orchestrates the entire process of classification and evaluation, including data loading,
    visualization, data preprocessing, model training, hyperparameter tuning, K-Fold Cross-Validation, and evaluation
    on the test set. It loads datasets, prints information about the classes, visualizes the dataset, scales the data,
    performs data augmentation, converts datasets into arrays, obtains classification models, applies hyperparameter
    tuning, K-Fold Cross-Validation, and evaluates the models. Finally, it saves the evaluation results to a CSV file.

    :param train_path: str, Path to the training dataset.
    :param test_path: str, Path to the test dataset.
    :param show_plot: bool, Flag indicating whether to display evaluation plots.
        Default is True.
    :param save_plot: bool, Flag indicating whether to save evaluation plots.
        Default is True.

    :returns: None
    """

    # Load keras datasets
    train_dataset, val_dataset, test_dataset = prepare.load_dataset(train_data_dir=train_path,
                                                                    test_data_dir=test_path)

    # Printing information about the datasets
    print("\n> Class Names:"
          "\n\t- Class 0 = {}"
          "\n\t- Class 1 = {}".format(train_dataset.class_names[0], train_dataset.class_names[1]))

    # Visualize the dataset showing some images with corresponding labels
    plot_functions.plot_view_dataset(train_ds=train_dataset, show_on_screen=show_plot, store_in_folder=save_plot)

    # Scaling data
    train_ds = prepare.data_normalization(tf_dataset=train_dataset, augment=True)
    val_ds = prepare.data_normalization(tf_dataset=val_dataset, augment=False)
    test_ds = prepare.data_normalization(tf_dataset=test_dataset, augment=False)

    # Visualize the data_augmentation process effect
    plot_functions.plot_data_augmentation(train_ds=train_dataset, data_augmentation=prepare.perform_data_augmentation(),
                                          show_on_screen=show_plot, store_in_folder=save_plot)

    # dataset into array
    X_train, y_train = prepare.image_to_array(train_ds)
    X_val, y_val = prepare.image_to_array(val_ds)
    X_test, y_test = prepare.image_to_array(test_ds)

    # Get the classification models
    classification_models = general.get_classifier()

    # Tuning, K-Fold Cross-Validation and then evaluate the models
    classification_procedure_workflow(models=classification_models, x_train=X_train, y_train=y_train, x_val=X_val,
                                      y_val=y_val, x_test=X_test, y_test=y_test, kfold=const.KFOLD,
                                      show_plot=show_plot, save_plot=save_plot)
