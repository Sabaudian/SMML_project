# Import
import os

# my import
import plot_functions
import data_preparation
import constants as const
import utils.pre_processing as prepare

# Main class of the project
if __name__ == '__main__':
    """
    EXPERIMENTAL PROJECTS - NEURAL NETWORK
    Use Keras to train a neural network for the binary classification of muffins and Chihuahuas 
    based on images from this dataset.
    Images must be transformed from JPG to RGB (or Grayscale) pixel values and scaled down. 

    The student is asked to:
        - experiment with different network architectures (at least 3) and training hyperparameters,
        - use 5-fold cross validation to compute your risk estimates,
        - thoroughly discuss the obtained results, documenting the influence of the choice of
          the network architecture and the tuning of the hyperparameters on the final
          cross-validated risk estimate.

    While the training loss can be chosen freely, the reported cross-validated estimates must be 
    computed according to the zero-one loss.
    """

    # checking the dataset
    prepare.checking_dataset(dataset_path=const.DATA_PATH,
                             train_dir_path=const.TRAIN_DIR,
                             test_dir_path=const.TEST_DIR)

    # # prepare and load the datasets
    # train_ds, validation_ds, test_ds = data_preparation.load_dataset(train_data_dir=const.TRAIN_DIR,
    #                                                                  test_data_dir=const.TEST_DIR,
    #                                                                  batch_size=const.BATCH_SIZE,
    #                                                                  img_size=const.IMG_SIZE)
    # # visualize the dataset with corresponding labels
    # plot_functions.plot_data_visualization(train_ds=train_ds, show_on_screen=True, store_in_folder=True)
