import sys
import json
import config
from worker import Translator, Verifier
from utils import Util, StatUtil

def translate_verify(data_path: str, result_path: str):
    with open(data_path, 'r') as fp:
        data = json.load(fp)
    
    trans = Translator(config.TRANS_MODEL_PATH, config.TRANS_GPUS)
    ver = Verifier(config.LEAN_HEADER, config.LEAN_TEST_PATH, config.LAKE_BIN)

    for i, d in enumerate(data):
        print(f'Processing {i} of {len(data)}')
        generated = trans.generate(d['id'], d['informal_statement'], config.TRANS_SAMPLING_PARAMS)
        generated = [Util.remove_informal_prefix(g) for g in generated]
        verified = ver.batch_verify_item(generated)
        d['verified'] = verified
        print(f'Finished {i} of {len(data)}, got {len(verified)} statements')
    
    with open(result_path, 'w') as fp:
        json.dump(data, fp, ensure_ascii=False, indent=4)
    StatUtil.get_verified_stat(result_path)

if __name__ == '__main__':
    translate_verify(sys.argv[1], sys.argv[2])