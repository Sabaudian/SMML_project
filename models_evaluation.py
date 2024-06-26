# Import
import os
import pandas as pd

from IPython import display
from sklearn.metrics import classification_report

# My import
import plot_functions
import constants as const
import utils.general_functions as general


# ******************************************** #
# ************* MODEL EVALUATION ************* #
# ******************************************** #


# Print info about the hyperparameter search
def get_hyperparameters_search_info(model_name, best_hyperparameters):
    """
    Print information about the optimal hyperparameter found during the tuning process,
    and store them into a .csv file

    :param model_name: The name of the model.
    :param best_hyperparameters: The best hyperparameters.
    """

    # Print info.
    print("\n> The hyperparameter search is complete!"
          "\n- The optimal number of units in the densely-connected layer is: {}"
          .format(best_hyperparameters.get("units")) +  # Dense layer units
          "\n- The optimal dropout rate is: {}"
          .format(best_hyperparameters.get("dropout_rate")) +  # Dropout-rate
          "\n- The optimal learning rate for the optimizer is: {}"
          .format(best_hyperparameters.get("learning_rate")))  # Learning rate

    # Define a dataframe
    model_best_hp_dict = {
        "Model": model_name,
        "Units": best_hyperparameters["units"],
        "Dropout Rate": best_hyperparameters["dropout_rate"],
        "Learning Rate": best_hyperparameters["learning_rate"]
    }

    # Turn it into a dataframe
    df = pd.DataFrame(data=[model_best_hp_dict])

    # Save data to csv file
    file_path = os.path.join(const.DATA_PATH, f"{model_name}_best_hyperparameters.csv")
    df.to_csv(file_path, index=False, float_format="%.4f")


# Collect data about the search
def collect_hyperparameters_tuning_data(model_name, tuner):
    """
    Collects hyperparameter tuning data for different models and saves it as a CSV file.

    :param model_name: (string) The name of the model being tuned.
        Supported options: 'MLP', 'CNN', 'MobileNet'.
    :param tuner: The hyperparameter tuner object.

    :return: None
    """
    # if not already present, create a folder to store data
    general.makedir(dirpath=const.DATA_PATH)

    # models: MLP, CNN, MobileNet
    keras_model_trials = []
    keras_model_units = []
    keras_model_dropout_rate = []
    keras_model_learning_rates = []
    keras_model_score = []

    for num_trial in tuner.oracle.trials.values():
        keras_model_trials.append(int(num_trial.trial_id) + 1)
        keras_model_units.append(num_trial.hyperparameters["units"])
        keras_model_dropout_rate.append(num_trial.hyperparameters["dropout_rate"])
        keras_model_learning_rates.append(num_trial.hyperparameters["learning_rate"])
        keras_model_score.append(num_trial.score)

    # Define a dataframe
    df = pd.DataFrame(list(zip(keras_model_trials, keras_model_units, keras_model_dropout_rate,
                               keras_model_learning_rates, keras_model_score)),
                      columns=["Trial", "Units", "Dropout Rate", "Learning Rate", "Validation Accuracy"])

    # Sort the dataframe by trial values
    df.sort_values(by=["Trial"], ascending=True, inplace=True)

    # Save data to csv file
    file_path = os.path.join(const.DATA_PATH, f"{model_name}_hyperparameter_tuning_data.csv")
    df.to_csv(file_path, index=False, float_format="%.4f")


# Test Loss and Accuracy metrics
def test_accuracy_loss_model(model, model_name, x_test, y_test):
    """
    Compute a simple evaluation of the model,
    printing the loss and accuracy metrics for the test set.

    :param model: Model in input.
    :param model_name: Name of the model.
    :param x_test: Input values of the test dataset.
    :param y_test: Target values of the test dataset.

    :return data_list: evaluation metrics dictionary
    """

    # Collect evaluation metrics
    test_score = model.evaluate(x=x_test, y=y_test, verbose=0)

    # Loss and Accuracy for the test set
    test_loss = test_score[0]
    test_accuracy = test_score[1]

    # Print evaluation info. about the model
    print("- Test Loss: {:.4f}".format(test_loss))
    print("- Test Accuracy: {:.4f} %".format(test_accuracy * 100))

    # Collect data
    data_list = {
        "Model": model_name,
        "Loss": test_loss,
        "Accuracy (%)": test_accuracy * 100
    }

    # Return dictionary
    return data_list


def compute_evaluation_metrics(model, model_name, x_test, y_test):
    """
    Get the classification report about the model in input.

    :param model: Model in input.
    :param model_name: Name of the model.
    :param x_test: Input values of the test dataset.
    :param y_test: Target values of the test dataset.

    :return: The Classification Report Dataframe of the model
    """

    # Predict
    predict = model.predict(x=x_test, verbose=0)
    # Convert the predictions to binary classes (0 or 1)
    y_pred = (predict > 0.5).astype("int32")

    # Compute report
    clf_report = classification_report(y_true=y_test, y_pred=y_pred, target_names=const.CLASS_LIST, digits=2,
                                       output_dict=True)

    # Update so in df is shown in the same way as standard print
    clf_report.update({"accuracy": {"precision": None, "recall": None, "f1-score": clf_report["accuracy"],
                                    "support": clf_report.get("macro avg")["support"]}})
    df = pd.DataFrame(data=clf_report).transpose()

    # Print report
    print("\n> Classification Report:")
    display.display(df)

    # Save the report
    general.makedir(dirpath=const.DATA_PATH)
    file_path = os.path.join(const.DATA_PATH, f"{model_name}_classification_report.csv")
    df.to_csv(file_path, index=True, index_label="index", float_format="%.3f")

    return df


# Model evaluation with extrapolation of data and information plot
def evaluate_model(model, model_name, x_test, y_test, show_plot=True, save_plot=True):
    """
    Evaluate the Performance of the model on the test set.

    :param model: The model in input.
    :param model_name: Name of the model.
    :param x_test: Input values of the test dataset.
    :param y_test: Target values of the test dataset.
    :param show_plot: If True, displays the plot on the screen.
        Default is True.
    :param save_plot: If True, save the plot.
        Default is True.

    :return data: evaluation metrics dictionary per model
    """

    # Evaluate the model
    print("\n> " + model_name + " Model Evaluation:")

    # Compute a simple evaluation report on the model performances
    data = test_accuracy_loss_model(model=model, model_name=model_name, x_test=x_test, y_test=y_test)

    # Compute the classification_report of the model
    compute_evaluation_metrics(model=model, model_name=model_name, x_test=x_test, y_test=y_test)

    # Plot Confusion Matrix
    plot_functions.plot_confusion_matrix(model=model, model_name=model_name, x_test=x_test, y_test=y_test,
                                         show_on_screen=show_plot, store_in_folder=save_plot)

    # Plot a representation of the prediction
    plot_functions.plot_model_predictions_evaluation(model=model, model_name=model_name, class_list=const.CLASS_LIST,
                                                     x_test=x_test, y_test=y_test, show_on_screen=show_plot,
                                                     store_in_folder=save_plot)

    # Plot a visual representation of the classification model, predicting classes
    plot_functions.plot_visual_prediction(model=model, model_name=model_name, x_test=x_test, y_test=y_test,
                                          show_on_screen=show_plot, store_in_folder=save_plot)

    # Prints a separation line for cleaner output
    print("__________________________________________________________________________________________")

    # Return dictionary
    return data
