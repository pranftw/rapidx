from copy import deepcopy
from multiple_screens import run



params = {
  'module_path': 'modules/mnist',
  'batch_size': None
}

screen_cmds = [
  'cd ..',
  'source venv/bin/activate'
]


def get_reqd_params(params, reqd_var):
  BATCH_SIZE, = reqd_var
  reqd_params = deepcopy(params)
  reqd_params['batch_size'] = BATCH_SIZE
  reqd_params['output_dir'] = f'outputs/{BATCH_SIZE}'
  return reqd_params



if __name__=='__main__':
  BATCH_SIZES = [16, 32, 64]

  run(params, get_reqd_params, screen_cmds, BATCH_SIZES, max_runs=2, check_freq=10)