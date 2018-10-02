import sys
import pandas as pd
import os


def load_league(file_dir):
    data = pd.read_csv(file_dir)

    print(data)
