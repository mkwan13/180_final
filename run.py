import sys
import json
import shutil

sys.path.insert(0, 'src') # add library code to path
from etl import getData
from lightdump import getDump

DATA_PARAMS = 'config/data-params.json'
TEST_PARAMS = 'config/test-params.json'

def load_params(fp):
    with open(fp) as fh:
        param = json.load(fh)

    return param
	
def main(targets):

    if 'test-project' in targets:
        cfg = load_params(DATA_PARAMS)
        data = getDump(**cfg)
        get_data(data)

	if 'data-test' in targets:
        	cfg = load_params(TEST_PARAMS)
        	get_data(data)
	else:
		cfg = load_params(DATA_PARAMS)
        get_data(**cfg)

    
if __name__ == '__main__':
    targets = sys.argv[1:]
    main(targets)
