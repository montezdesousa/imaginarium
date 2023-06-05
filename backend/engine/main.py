import gzip
import os
import pickle
import sys
from typing import List, Tuple
import matplotlib.pyplot as plt

# INTERNAL IMPORTS
from .constants import IMAGE_WIDTH, IMAGE_HEIGHT
from .extract_features import create_model, get_img_features
from .utils import read_img, resize_img_to_array
from .Table import get_urls_from_ids


def plot_neighbors(
    url: str,
    table: str,
    distance: List[float],
    idx: List[int],
    top: int = 8,
    per_row: int = 4,
):
    """Plot the neighbors

    Parameters
    ----------
    url : str
        The url of the image
    table : str
        The table to query
    neighbors : tuple
        The neighbors to plot
    top : int, optional
        The number of neighbors to plot, by default 8
    per_row : int, optional
        The number of images per row, by default 4
    """
    urls, _, _ = get_urls_from_ids(idx, table)
    _, axes = plt.subplots(top // per_row + 1, per_row, figsize=(8, 10))
    axes[0][0].imshow(read_img(url))

    for i in range(per_row):
        axes[0][i].axis("off")

    k = 0
    for j in range(top // per_row):
        for i in range(per_row):
            image = read_img(urls[k])
            image = resize_img_to_array(image, 200, 200)
            axes[j + 1][i].imshow(image)
            axes[j + 1][i].axis("off")
            axes[j + 1][i].annotate(
                round(distance[k], 2),
                (0, 0),
                (0, -3),
                xycoords="axes fraction",
                textcoords="offset points",
                va="top",
            )
            k += 1

    mng = plt.get_current_fig_manager()
    mng.resize(*mng.window.maxsize())
    plt.show()


def get_neighbors(url: str, knn_file: str) -> Tuple[List[float], List[int]]:
    """Get the neighbors of an image

    Parameters
    ----------
    url : str
        The url of the image
    knn_file : str
        The url containing the knn model
    reference_files : pd.Series
        The reference files
    top : int, optional
        The number of neighbors to plot, by default 8
    """
    current_dir = os.path.abspath(os.path.dirname(__file__))
    with gzip.open(os.path.join(current_dir, knn_file), 'rb') as f:
        knn = pickle.load(f)

    model = create_model(input_shape=[IMAGE_WIDTH, IMAGE_HEIGHT, 3])
    X_conv_2d = get_img_features(url, model)
    if len(X_conv_2d) > 0:
        X_conv_2d = X_conv_2d.reshape(1, -1)
        neighbors = knn.kneighbors(X_conv_2d, return_distance=True)
        distance = [float(i) for i in neighbors[0][0]]
        idx = [int(i) for i in neighbors[1][0]]
        return distance, idx
    return [], []


def get_result_urls(query: str, table: str) -> List[Tuple[str, str, str]]:
    """Get the urls of the result

    Parameters
    ----------
    query : str
        The url of the image
    table : str
        The table to query

    Returns
    -------
    List[Tuple[str, str, str]]
        The urls of the result
    """
    _, idx = get_neighbors(query, f"knn_{table}.pkl")
    if idx:
        print(idx)
        return get_urls_from_ids(idx, table)



if __name__ == "__main__":
    img_file = "https://cdn3.jornaldenegocios.pt/images/2019-01/img_440x274$2019_01_07_12_49_10_346064.jpg"

    if len(sys.argv) > 1:
        img_file = sys.argv[1]

    table = "master_db"

    distance, idx = get_neighbors(img_file, f"backend\knn_{table}.pkl")
    plot_neighbors(
        url=img_file,
        table=table,
        distance=distance,
        idx=idx,
        top=20,
        per_row=4,
    )
