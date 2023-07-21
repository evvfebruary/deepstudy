import pandas as pd
from typing import TypedDict
from collections import abc


class AnkiCard(TypedDict):
    question: str
    answer: str


def save_cards(anki_cards_list: abc.Sequence[AnkiCard], savepath: str) -> str:
    pd.DataFrame.from_records(anki_cards_list).to_csv(savepath, index=False, header=False)
    return savepath


def combine_anki_cards_csv(anki_cards_files: abc.Sequence[str], savepath: str = './anki_cards.csv') -> str:
    cards_df = []
    for anki_cards_file in anki_cards_files:
        card_df = pd.read_csv(anki_cards_file, header=None)
        cards_df.append(card_df)
    pd.concat(cards_df, axis=0, ignore_index=True).to_csv(savepath, index=False, header=False)
    return savepath
