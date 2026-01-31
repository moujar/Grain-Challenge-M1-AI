# Model file which contains a model class in scikit-learn style
# Model class must have these 3 methods
# - __init__: initializes the model
# - fit: trains the model
# - predict: uses the model to perform predictions
#
# Created by: Abderrahmane Moujar and  Oloruntobi Paul Olutola
# Created on: 30 Jan, 2026

# ----------------------------------------
# Imports
# ----------------------------------------
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA


# ----------------------------------------
# Model Class
# ----------------------------------------
class Model:

    def __init__(self):
        """
        This is a constructor for initializing classifier

        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        print("[*] - Initializing Classifier")

        # Optimized RandomForest classifier
        self.clf = RandomForestClassifier(
            n_estimators=200,        # More trees for better accuracy
            max_depth=30,            # Deeper trees
            min_samples_split=5,     # Prevent overfitting
            min_samples_leaf=2,      # Prevent overfitting
            max_features='sqrt',     # Use sqrt of features per split
            n_jobs=-1,               # Use all CPU cores
            random_state=42,
            class_weight='balanced'  # Handle class imbalance
        )

        # Scaler for normalizing features
        self.scaler = StandardScaler()

        # PCA for dimensionality reduction (faster training, less overfitting)
        self.pca = PCA(n_components=100, random_state=42)
        self.use_pca = True

        # Number of histogram bins per channel
        self.n_bins = 32

    def _extract_color_histogram(self, img):
        """
        Extract color histogram features from an image.

        Parameters
        ----------
        img: numpy array of shape (H, W, C)

        Returns
        -------
        hist: 1D numpy array of histogram features
        """
        histograms = []
        for c in range(img.shape[2]):
            channel = img[:, :, c].flatten()
            # Normalize to 0-1 range
            if channel.max() > 1:
                channel = channel / 255.0
            hist, _ = np.histogram(channel, bins=self.n_bins, range=(0, 1))
            hist = hist / (hist.sum() + 1e-8)  # Normalize histogram
            histograms.append(hist)
        return np.concatenate(histograms)

    def _extract_statistics(self, img):
        """
        Extract statistical features from an image.

        Parameters
        ----------
        img: numpy array of shape (H, W, C)

        Returns
        -------
        stats: 1D numpy array of statistical features
        """
        stats = []
        for c in range(img.shape[2]):
            channel = img[:, :, c]
            stats.extend([
                np.mean(channel),
                np.std(channel),
                np.min(channel),
                np.max(channel),
                np.median(channel),
                np.percentile(channel, 25),
                np.percentile(channel, 75),
            ])
        return np.array(stats)

    def _extract_features(self, X):
        """
        Extract features from images using multiple methods.

        Parameters
        ----------
        X: numpy array of shape (n_samples, H, W, C)

        Returns
        -------
        features: numpy array of shape (n_samples, n_features)
        """
        if isinstance(X, list):
            X = np.array(X)

        n_samples = X.shape[0]
        features_list = []

        for i in range(n_samples):
            img = X[i]

            # 1. Color histograms (n_bins * 3 channels = 96 features)
            hist_features = self._extract_color_histogram(img)

            # 2. Statistical features (7 stats * 3 channels = 21 features)
            stat_features = self._extract_statistics(img)

            # 3. Downsampled image (reduce resolution for faster processing)
            # Resize to smaller size using simple averaging
            h, w = img.shape[:2]
            new_h, new_w = 16, 16  # Downsample to 16x16
            block_h, block_w = h // new_h, w // new_w

            if block_h > 0 and block_w > 0:
                downsampled = img[:block_h * new_h, :block_w * new_w].reshape(
                    new_h, block_h, new_w, block_w, -1
                ).mean(axis=(1, 3))
            else:
                downsampled = img[:new_h, :new_w]

            flat_features = downsampled.flatten()

            # Combine all features
            combined = np.concatenate([hist_features, stat_features, flat_features])
            features_list.append(combined)

        return np.array(features_list)

    def fit(self, train_data):
        """
        This function trains the model provided training data

        Parameters
        ----------
        train_data: dict
            contains train data and labels
            - 'X': numpy array of images (n_samples, height, width, channels)
            - 'y': numpy array of labels (n_samples,)

        Returns
        -------
        None
        """
        print("[*] - Training Classifier on the train set")

        # Extract features and labels
        X = train_data['X']
        y = train_data['y']

        # Extract features from images
        print("[*] - Extracting features...")
        X_features = self._extract_features(X)
        print(f"[*] - Extracted {X_features.shape[1]} features per sample")

        # Scale features
        X_scaled = self.scaler.fit_transform(X_features)

        # Apply PCA for dimensionality reduction
        if self.use_pca and X_scaled.shape[1] > self.pca.n_components:
            print(f"[*] - Applying PCA: {X_scaled.shape[1]} -> {self.pca.n_components} dimensions")
            X_scaled = self.pca.fit_transform(X_scaled)

        # Train the classifier
        print(f"[*] - Training on {X_scaled.shape[0]} samples with {X_scaled.shape[1]} features")
        self.clf.fit(X_scaled, y)
        print("[*] - Training complete")

    def predict(self, test_data):
        """
        This function predicts labels on test data.

        Parameters
        ----------
        test_data: dict
            contains test data
            - 'X': numpy array of images (n_samples, height, width, channels)

        Returns
        -------
        y: 1D numpy array
            predicted labels
        """
        print("[*] - Predicting test set using trained Classifier")

        # Extract features
        X = test_data['X']

        # Extract features from images
        X_features = self._extract_features(X)

        # Scale features
        X_scaled = self.scaler.transform(X_features)

        # Apply PCA
        if self.use_pca and hasattr(self.pca, 'components_'):
            X_scaled = self.pca.transform(X_scaled)

        # Predict
        y = self.clf.predict(X_scaled)

        print(f"[*] - Predicted {len(y)} samples")
        return y
