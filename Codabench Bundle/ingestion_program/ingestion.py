# ------------------------------------------
# Imports
# ------------------------------------------
import os
import json
import numpy as np
import pandas as pd
from datetime import datetime as dt


class Ingestion:
    """
    Class for handling the ingestion process.

    Args:
        None

    Attributes:
        * start_time (datetime): The start time of the ingestion process.
        * end_time (datetime): The end time of the ingestion process.
        * model (object): The model object.
        * train_data (dict): The train data dict.
        * test_data (dict): The test data dict.
        * predictions (array): The model predictions.
        * test_grain_ids (list): List of grain IDs for test samples.
        * ingestion_result (dict): The ingestion result dict.
    """

    def __init__(self):
        """
        Initialize the Ingestion class.

        """
        self.start_time = None
        self.end_time = None
        self.model = None
        self.train_data = None
        self.test_data = None
        self.predictions = None
        self.test_grain_ids = None
        self.ingestion_result = None

    def start_timer(self):
        """
        Start the timer for the ingestion process.
        """
        self.start_time = dt.now()

    def stop_timer(self):
        """
        Stop the timer for the ingestion process.
        """
        self.end_time = dt.now()

    def get_duration(self):
        """
        Get the duration of the ingestion process.

        Returns:
            timedelta: The duration of the ingestion process.
        """
        if self.start_time is None:
            print("[-] Timer was never started. Returning None")
            return None

        if self.end_time is None:
            print("[-] Timer was never stopped. Returning None")
            return None

        return self.end_time - self.start_time

    def save_duration(self, output_dir=None):
        """
        Save the duration of the ingestion process to a file.

        Args:
            output_dir (str): The output directory to save the duration file.
        """
        duration = self.get_duration()
        duration_in_mins = int(duration.total_seconds() / 60)
        duration_file = os.path.join(output_dir, "ingestion_duration.json")
        if duration is not None:
            with open(duration_file, "w") as f:
                f.write(json.dumps({"ingestion_duration": duration_in_mins}, indent=4))

    def _load_npz_files(self, input_dir, filenames, load_labels=True):
        """
        Load .npz files and extract images and optionally labels.

        Args:
            input_dir (str): Directory containing .npz files.
            filenames (list): List of .npz filenames to load.
            load_labels (bool): Whether to load labels from files.

        Returns:
            tuple: (X, y, grain_ids) - images, labels (or None), grain IDs
        """
        X_list = []
        y_list = []
        grain_ids = []

        for filename in filenames:
            filepath = os.path.join(input_dir, filename)
            if os.path.exists(filepath):
                try:
                    data = np.load(filepath)
                    X_list.append(data['x'])
                    if load_labels and 'y' in data:
                        y_list.append(data['y'])
                    # Extract grain ID from filename
                    grain_id = filename.split('_')[0].replace('grain', '')
                    grain_ids.append(grain_id)
                except Exception as e:
                    print(f"[-] Error loading {filename}: {e}")

        X = np.array(X_list)
        y = np.array(y_list) if y_list else None

        return X, y, grain_ids

    def load_train_and_test_data(self, input_dir):
        """
        Load the training and testing data from input_dir.

        Training data: Files listed in input_data.csv (with labels)
        Test data: .npz files NOT in input_data.csv (without labels)
                   OR if all files are in CSV, use a subset for testing

        Args:
            input_dir (str): The input data directory.
        """
        print("[*] Loading data from input directory")

        # Load the CSV with training metadata
        csv_path = os.path.join(input_dir, "input_data.csv")
        if not os.path.exists(csv_path):
            raise FileNotFoundError(f"input_data.csv not found in {input_dir}")

        df = pd.read_csv(csv_path)
        print(f"[*] Found {len(df)} entries in input_data.csv")

        # Get all .npz files in directory
        all_npz_files = [f for f in os.listdir(input_dir) if f.endswith('.npz')]
        print(f"[*] Found {len(all_npz_files)} .npz files in input directory")

        # Files in CSV are training data (with labels)
        train_files = set(df['filename'].tolist())

        # Files NOT in CSV are test data (without labels)
        test_files = [f for f in all_npz_files if f not in train_files]

        print(f"[*] Training files: {len(train_files)}")
        print(f"[*] Test files: {len(test_files)}")

        # Load training data
        print("[*] Loading training data...")
        train_filenames = df['filename'].tolist()
        train_labels = df['varietyNumber'].values

        X_train, _, train_grain_ids = self._load_npz_files(
            input_dir, train_filenames, load_labels=False
        )
        y_train = train_labels[:len(X_train)]  # Match loaded samples

        self.train_data = {
            'X': X_train,
            'y': y_train,
            'grain_ids': train_grain_ids
        }
        print(f"[*] Loaded {len(X_train)} training samples")
        print(f"[*] Training data shape: {X_train.shape}")
        print(f"[*] Labels distribution: {np.unique(y_train, return_counts=True)}")

        # Load test data
        if len(test_files) > 0:
            print("[*] Loading test data (unlabeled files)...")
            X_test, _, test_grain_ids = self._load_npz_files(
                input_dir, test_files, load_labels=False
            )
        else:
            # If no separate test files, use training data for testing
            # (This is just for pipeline testing - in real competition, test files should be separate)
            print("[!] No separate test files found. Using training data for testing.")
            X_test = X_train
            test_grain_ids = train_grain_ids

        self.test_data = {
            'X': X_test,
            'grain_ids': test_grain_ids
        }
        self.test_grain_ids = test_grain_ids
        print(f"[*] Loaded {len(X_test)} test samples")
        print(f"[*] Test data shape: {X_test.shape}")

    def init_submission(self, Model):
        """
        Initialize the submitted model.

        Args:
            Model (object): The model class.
        """
        print("[*] Initializing Submitted Model")
        self.model = Model()

    def fit_submission(self):
        """
        Fit the submitted model.
        """
        print("[*] Fitting Submitted Model")
        self.model.fit(self.train_data)

    def predict_submission(self):
        """
        Make predictions using the submitted model.
        """
        print("[*] Calling predict method of submitted model")
        self.predictions = self.model.predict(self.test_data)
        print(f"[*] Generated {len(self.predictions)} predictions")

    def compute_result(self):
        """
        Compute the ingestion result.
        Creates a dictionary mapping grain IDs to predicted variety numbers.
        """
        print("[*] Computing Ingestion Result")

        # Create result dictionary with grain_id -> predicted_variety
        result = {}
        for grain_id, pred in zip(self.test_grain_ids, self.predictions):
            result[str(grain_id)] = int(pred)

        self.ingestion_result = {
            'predictions': result,
            'num_predictions': len(result)
        }
        print(f"[*] Result contains {len(result)} predictions")

    def save_result(self, output_dir=None):
        """
        Save the ingestion result to files.

        Args:
            output_dir (str): The output directory to save the result files.
        """
        # Create output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)

        result_file = os.path.join(output_dir, "result.json")
        with open(result_file, "w") as f:
            f.write(json.dumps(self.ingestion_result, indent=4))
        print(f"[*] Results saved to {result_file}")