from typing import List, Tuple
import requests
from tqdm import tqdm


def get_assets(
    site_search: str, offset: int = 0, max_items: int = 200
) -> List[Tuple[str, str, str]]:
    """Get assets from Arquivo.pt

    Parameters
    ----------
    site_search : str
        Site to search
    offset : int, optional
        Offset, by default 0
    max_items : int, optional
        Max items, by default 200

    Returns
    -------
    List[Tuple[str, str, str]], int
        Assets
    """
    r = requests.get(
        f"https://arquivo.pt/imagesearch?siteSearch={site_search}&maxItems={max_items}&offset={offset}"
    )
    assets = [
        (i.get("imgLinkToArchive"), i.get("pageLinkToArchive"), i.get("pageTitle"), site_search)
        for i in r.json()["responseItems"]
    ]
    total_items = r.json()["totalItems"]

    return assets, total_items


def get_asset_list(
    website: str, total_items: int, start: int = 0, offset: int = 0
) -> List[Tuple[str, str, str]]:
    """Get asset list from Arquivo.pt

    Parameters
    ----------
    website : str
        Website to search
    total_items : int
        Total items to search

    Returns
    -------
    List[Tuple[str, str, str]]
        Assets
    """
    MAX_ITEMS_PER_REQUEST = min(total_items, 200)
    assets, TOTAL_ITEMS = get_assets(
        site_search=website, offset=offset, max_items=MAX_ITEMS_PER_REQUEST
    )
    total = min(total_items, TOTAL_ITEMS)

    for i in tqdm(range(offset + MAX_ITEMS_PER_REQUEST, total, MAX_ITEMS_PER_REQUEST)):
        res, _ = get_assets(
            site_search=website, offset=i, max_items=MAX_ITEMS_PER_REQUEST
        )

        assets += res

    return assets[start:total_items]


if __name__ == "__main__":
    WEBSITE = "publico.pt"
    assets = get_asset_list(website=WEBSITE, total_items=201)
    print(len(assets))
