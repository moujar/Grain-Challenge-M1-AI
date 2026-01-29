# ------------------------------------------
# Imports
# ------------------------------------------
import os
import json
import pandas as pd
from datetime import datetime as dt


class Scoring:
    """
    This class is used to compute the scores for the competition.

    Attributes:
        * start_time (datetime): The start time of the scoring process.
        * end_time (datetime): The end time of the scoring process.
        * reference_data (dict): The reference data (ground truth labels).
        * ingestion_result (dict): The ingestion result (predictions).
        * ingestion_duration (float): The ingestion duration.
        * scores_dict (dict): The scores dictionary.
    """

    def __init__(self, name=""):
        # Initialize class variables
        self.start_time = None
        self.end_time = None
        self.reference_data = None
        self.ingestion_result = None
        self.ingestion_duration = None
        self.scores_dict = {}

    def start_timer(self):
        self.start_time = dt.now()

    def stop_timer(self):
        self.end_time = dt.now()

    def get_duration(self):
        if self.start_time is None:
            print("[-] Timer was never started. Returning None")
            return None

        if self.end_time is None:
            print("[-] Timer was never stopped. Returning None")
            return None

        return self.end_time - self.start_time

    def load_reference_data(self, reference_dir):
        """
        Load the reference data (ground truth labels) from reference_data.csv.

        Args:
            reference_dir (str): The reference data directory name.
        """
        print("[*] Reading reference data")

        reference_data_file = os.path.join(reference_dir, "reference_data.csv")

        if not os.path.exists(reference_data_file):
            raise FileNotFoundError(f"reference_data.csv not found in {reference_dir}")

        # Load CSV with ground truth labels
        df = pd.read_csv(reference_data_file)

        # Create dictionary mapping grainID -> varietyNumber (ground truth)
        self.reference_data = {}
        for _, row in df.iterrows():
            grain_id = str(row['grainID'])
            variety = int(row['varietyNumber'])
            self.reference_data[grain_id] = variety

        print(f"[*] Loaded {len(self.reference_data)} ground truth labels")

    def load_ingestion_result(self, predictions_dir):
        """
        Load the ingestion result (predictions) from result.json.

        Args:
            predictions_dir (str): The predictions directory name.
        """
        print("[*] Reading ingestion result")

        ingestion_result_file = os.path.join(predictions_dir, "result.json")

        if not os.path.exists(ingestion_result_file):
            raise FileNotFoundError(f"result.json not found in {predictions_dir}")

        with open(ingestion_result_file, "r") as f:
            result = json.load(f)

        # Extract predictions dictionary
        self.ingestion_result = result.get('predictions', {})
        print(f"[*] Loaded {len(self.ingestion_result)} predictions")

        # Load ingestion duration if available
        duration_file = os.path.join(predictions_dir, "ingestion_duration.json")
        if os.path.exists(duration_file):
            with open(duration_file, "r") as f:
                duration_data = json.load(f)
                self.ingestion_duration = duration_data.get('ingestion_duration', None)
                print(f"[*] Ingestion duration: {self.ingestion_duration} minutes")

    def compute_scores(self):
        """
        Compute the accuracy score for the competition.

        Accuracy = (number of correct predictions) / (total predictions)
        """
        print("[*] Computing scores")

        if not self.ingestion_result:
            print("[-] No predictions found")
            self.scores_dict = {"score": 0.0}
            return

        if not self.reference_data:
            print("[-] No reference data found")
            self.scores_dict = {"score": 0.0}
            return

        # Count correct predictions
        correct = 0
        total = 0
        missing_ground_truth = 0

        for grain_id, predicted_variety in self.ingestion_result.items():
            if grain_id in self.reference_data:
                true_variety = self.reference_data[grain_id]
                if int(predicted_variety) == int(true_variety):
                    correct += 1
                total += 1
            else:
                missing_ground_truth += 1

        # Compute accuracy
        if total > 0:
            accuracy = correct / total
        else:
            accuracy = 0.0

        print(f"[*] Correct predictions: {correct}/{total}")
        print(f"[*] Accuracy: {accuracy:.4f} ({accuracy * 100:.2f}%)")

        if missing_ground_truth > 0:
            print(f"[!] Warning: {missing_ground_truth} predictions had no ground truth")

        # Store scores - 'score' key matches competition.yaml leaderboard column
        self.scores_dict = {
            "score": round(accuracy, 6),
            "correct": correct,
            "total": total,
            "accuracy_percent": round(accuracy * 100, 2)
        }

    def write_scores(self, output_dir):
        """
        Write scores to scores.json file.

        Args:
            output_dir (str): The output directory to save the scores file.
        """
        print("[*] Writing scores")

        # Create output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)

        score_file = os.path.join(output_dir, "scores.json")
        with open(score_file, "w") as f_score:
            f_score.write(json.dumps(self.scores_dict, indent=4))

        print(f"[*] Scores saved to {score_file}")
