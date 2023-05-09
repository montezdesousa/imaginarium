import sys
import joblib
import time
from sklearn.neighbors import NearestNeighbors

from engine.Table import get_all_convolution


def train_and_pickle(X, file, n_neighbors=20, n_jobs=8, algorithm="ball_tree"):
    """Train a KNN model and pickle it to a file

    Parameters
    ----------
    X : numpy.ndarray
        The features to train the model on
    file : str
        The file to pickle the model to
    """
    knn = NearestNeighbors(n_neighbors=n_neighbors, n_jobs=n_jobs, algorithm=algorithm)
    knn.fit(X)
    joblib.dump(knn, file)


if __name__ == "__main__":
    table = sys.argv[1] if len(sys.argv) > 1 else "master_db"
    print(f"Training started for table {table}.")
    X = get_all_convolution(table)
    start = time.time()
    train_and_pickle(X, f"knn_{table}.pkl", n_neighbors=200)
    end = time.time()
    elapsed = round(end - start, 2)
    print(f"Training complete {elapsed} seconds.")
