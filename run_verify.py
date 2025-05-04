import sys
import json
import config
import pandas as pd
from multiprocessing import Pool
from tqdm import tqdm
from worker import Translator, Verifier
from utils import Util, StatUtil

ver = Verifier(config.LEAN_HEADER, config.LEAN_TEST_PATH, config.LAKE_BIN)


def verify_single(formal):
    generated = Util.remove_informal_prefix(formal)
    verified, message = ver.verify(generated)
    return verified, message


def verify(data_path: str, result_path: str):
    df = pd.read_json(data_path)

    results = []
    messages = []

    right = 0
    total = 0

    with Pool(8) as pool:
        pbar = tqdm(pool.imap(verify_single, df["formal_statement"]), total=len(df["formal_statement"]))
        for res, msg in pbar:
            results.append(res)
            messages.append(msg)
            total += 1
            right += int(res)
            pbar.set_postfix({"accuracy": right / total})

    df["verified"] = results
    df["messages"] = messages
    df.to_json(result_path)
    print("done!")
    print(df["verified"].value_counts())


if __name__ == "__main__":
    verify(sys.argv[1], sys.argv[2])
