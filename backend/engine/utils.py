import os
from typing import List, Tuple
from PIL import Image
from urllib.request import urlopen
import numpy as np
import pandas as pd
import validators
import csv


def read_img(name: str) -> Image:
    """Read image from file

    Parameters
    ----------
    name : str
        Path to image

    Returns
    -------
    PIL.Image
        Image from file
    """
    if validators.url(name):
        img = read_img_url(name)
    elif os.path.exists(name):
        img = Image.open(name)
    else:
        print(f"File {name} not found")
        return None

    if img.mode != "RGB":
        img = img.convert("RGB")
    return img


def read_img_url(url: str) -> Image:
    """Read image from url

    Parameters
    ----------
    url : str
        URL of image

    Returns
    -------
    PIL.Image
        Image from url
    """
    with urlopen(url) as response:
        img = Image.open(response)

    if img.mode != "RGB":
        img = img.convert("RGB")
    return img


def resize_img_to_array(img, width: int, height: int) -> Image:
    """Resize image to array

    Parameters
    ----------
    img : PIL.Image
        Image to resize
    width : int
        Width of image
    height : int
        Height of image

    Returns
    -------
    PIL.Image
        Resized image
    """
    return img.resize((width, height), Image.LANCZOS)


def dump_features(result: List, file: str) -> None:
    """Dump features to file

    Parameters
    ----------
    url : str
        Url of image
    features : np.ndarray
        Features to dump
    """
    mode = "a" if os.path.exists(file) else "w"
    with open(file, mode, newline="") as f:
        writer = csv.writer(f)
        writer.writerows(result)


def read_csv(file: str) -> Tuple[np.array, pd.Series]:
    """Read csv file

    Parameters
    ----------
    file : str
        Path to csv file

    Returns
    -------
    np.array
        Image features
    pd.Series
        Image labels
    """
    X = pd.read_csv(file, header=None)
    Y = X[0]
    X_conv_2d = X[[col for col in X.columns if col > 0]].values.astype(float)

    return X_conv_2d, Y
