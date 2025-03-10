import sys
import json
import config
from worker import BackTranslator, NLInferencer
from utils import Util, StatUtil

def backtrans_nli(result_path: str):
    with open(result_path) as fp:
        data = json.load(fp)
    
    btrans = BackTranslator(config.BACKTRANS_MODEL_PATH, config.BACKTRANS_GPUS)
    nli = NLInferencer(config.NLI_MODEL, config.NLI_API_BASE_URL, config.NLI_API_KEY)
    
    for i, d in enumerate(data):
        print(f'Processing {i} of {len(data)}')
        verified = d['verified']
        backtranslated = btrans.batch_generate(verified, config.BACKTRANS_SAMPLING_PARAMS)
        nli_outputs = [nli.generate(d['informal_statement'], gen, config.NLI_SAMPLING_PARAMS)
            for gen in backtranslated]
        translated = []
        for v, n in zip(verified, nli_outputs):
            if Util.extract_bold_text(n) == 'same':
                translated.append(v)
        d['translated'] = translated
        print(f'Finished {i} of {len(data)}, got {len(translated)} statements.')
    
    with open(result_path, 'w') as fp:
        json.dump(data, fp, ensure_ascii=False, indent=4)
    StatUtil.get_translated_stat(result_path)

if __name__ == '__main__':
    backtrans_nli(sys.argv[1])