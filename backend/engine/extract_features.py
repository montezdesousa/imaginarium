"""Process image and convert to convolution"""
import time
from typing import List, Tuple
import numpy as np
from tqdm import tqdm

from keras.applications import ResNet50
from keras.applications.resnet import preprocess_input

# INTERNAL IMPORTS
from engine.constants import IMAGE_WIDTH, IMAGE_HEIGHT
from engine.build_dataset import get_asset_list
from engine.db import Session
from engine.utils import read_img, resize_img_to_array


def create_model(input_shape: List[int]) -> ResNet50:
    """Create model for image processing

    Parameters
    ----------
    input_shape : List[int]
        Shape of input image

    Returns
    -------
    ResNet50
        Model for image processing
    """
    model = ResNet50(
        input_shape=input_shape, include_top=False, weights="imagenet", pooling="avg"
    )

    for layer in model.layers:
        layer.trainable = False

    return model


def get_img_features(url: str, model: ResNet50) -> List[float]:
    """Get image features

    Parameters
    ----------
    url : str
        Url of image

    Returns
    -------
    np.ndarray
        Image features
    """
    try:
        img = read_img(url)
    except Exception as e:
        print(f"Error reading image {url}: {e}")
        return []
    
    if img:
        img_array = resize_img_to_array(img, IMAGE_WIDTH, IMAGE_HEIGHT)
        X = preprocess_input(np.expand_dims(img_array, axis=0).astype(float))
        X_conv = model.predict(X)
        return X_conv[0].flatten()
    return []


def convert_and_write_to_db(
    table: str,
    assets: List[Tuple[str, str, str]],
    session: Session,
    model: ResNet50,
    total_items: int,
    start: int = 0,
):
    """Convert images to convolution and write to database

    Parameters
    ----------
    table : str
        Name of table
    assets : List[Tuple[str, str, str]]
        List of urls
    session : Session
        Database session
    model : ResNet50
        Model for image processing
    total_items : int
        Total number of items to process
    """
    WRITE_EACH = 50
    result = []
    k = start
    for img_url, page_url, page_title, website in tqdm(assets):
        d = {}
        d["ID"] = k
        d["IMG_URL"] = img_url

        d["Convolution"] = ",".join(
            [str(x) for x in get_img_features(img_url, model)]
        ).encode("ascii")
        if not d["Convolution"]:
            continue

        d["PAGE_URL"] = page_url
        d["PAGE_TITLE"] = page_title
        d["WEBSITE"] = website
        result.append(d)
        k += 1
        if k % WRITE_EACH == 0:
            print("Writing to database...")
            session.insert(table, result)
            result = []
        elif k == total_items:
            print("Writing to database...")
            session.insert(table, result)
            result = []


def main():
    WEBSITES = [
        # "acorianooriental.pt",
        # "auroradolima.com",
        # "diariodosacores.pt",
        # "livraria.apostoladodaoracao.pt/revistas/mensageiro-digital",
        # "soberaniadopovo.pt",
        # "vozoperario.pt/jornal",
        # "jornalestarreja.com",
        # "guimaraesdigital.pt",
        # "jornalmariadafonte.blogspot.com",
        # "correiodoribatejo.pt",
        "correiodafeira.pt",
        "jornaldeabrantes.sapo.pt",
        "acomarcadearganil.pt",
        "facebook.com/jornaloconcelhodeestarreja",
        "salesianos.pt/bs",
        "jornalaguarda.com",
        "folhadetondela.pt",
        "cardealsaraiva.com",
        "noticiasdacovilha.pt",
        "jornalaordem.pt",
        "artigosjornaljoaosemana.blogspot.pt",
        "noticiasdegouveia.pt",
        "folhadodomingo.pt",
        "amigodopovo1916.blogspot.com",
        "odespertar.pt",
        "jornalodever.pt",
        "oalmonda.net",
        "ofigueirense.com",
        "correiodosacores.pt",
        "jornaldealbergaria.pt",
        "oilhavense.com",
        "osetubalense.com",
        "diariodominho.pt",
        "correiodeazemeis.pt",
        "adefesa.org",
        # "jn.pt",
        # "dnoticias.pt",
        # "dn.pt",
        # "publico.pt", # so tenho 5000 imagens, tirar mais daqui
    ]
    TOTAL_ITEMS = 5000 
    SEARCH_START = 0  # last item downloaded + 1
    TABLE_NAME = "master_db"

    print("0. Creating image processing model...\n")
    model = create_model(input_shape=[IMAGE_WIDTH, IMAGE_HEIGHT, 3])

    db_start = 12500 # last item in database + 1
    for w in WEBSITES:

        print(f"\n\nProcessing {w}...\n")

        print("1. Collecting urls...\n")
        assets = get_asset_list(
            website=w, total_items=TOTAL_ITEMS, start=SEARCH_START
        )

        print("2. Creating DB session...\n")
        session = Session()
        session.start()

        print("3. Converting to convolution...\n")
        start = time.time()
        convert_and_write_to_db(TABLE_NAME, assets, session, model, TOTAL_ITEMS, db_start)
        end = time.time()
        elapsed = round(end - start, 2)

        db_start += len(assets)

        print(f"4. Conversion complete in {elapsed} seconds.")


if __name__ == "__main__":
    main()
