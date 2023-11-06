from itertools import product
import subprocess
import os
import time



def validate_run():
  screen_windows = get_screen_windows()
  assert len(screen_windows)==1, f'Only one active screen window must be present during execution! Ideally run on a new screen session!'
  assert screen_windows==['0'], f'The screen window number of the active screen must be 0! Ideally run on a new screen session!'


def get_screen_windows():
  screen_windows = subprocess.run('tmux list-windows -F "#I"', shell=True, capture_output=True).stdout.decode().strip()
  screen_windows_list = screen_windows.split('\n')
  return screen_windows_list


def get_command(params, init_command='python run.py'):
  command = init_command
  for option_name, option_value in params.items():
    command+=f' --{option_name} {option_value}'
  return command


def create_screen_windows(num_windows):
  for _ in range(num_windows):
    subprocess.Popen(f'tmux new-window -d', shell=True)


def check_execution_status(tmp_fpath):
  all_statuses = {}
  if not os.path.exists(tmp_fpath):
    return False
  with open(tmp_fpath) as fp:
    statuses = fp.readlines()

  for status in statuses:
    window_status, window_num = status.split()
    if window_status=='STARTED':
      all_statuses[window_num] = 1
    elif window_status=='FINISHED':
      all_statuses[window_num] = 0
    else:
      raise ValueError(f'Invalid window status {window_status} for window {window_num}!')
  return sum(list(all_statuses.values()))==0 # returns True if all have finished, else False


def group_configs(configs, max_runs):
  grouped_configs = []
  i=0
  while i+max_runs<=len(configs):
    grouped_configs.append(configs[i:i+max_runs])
    i+=max_runs
  else:
    if i!=len(configs):
      grouped_configs.append(configs[i:])
  return grouped_configs


def run(params, get_reqd_params, screen_cmds, *vars, max_runs=10, check_freq=300, kill_after_completion=True):
  def execute(reqd_var, newly_added_screen_window):
    reqd_params = get_reqd_params(params, reqd_var)
    preprocesses = [f'echo STARTED {newly_added_screen_window} >> {tmp_fpath}']
    postprocesses = [f'echo FINISHED {newly_added_screen_window} >> {tmp_fpath}']
    if kill_after_completion:
      postprocesses.append(f'tmux kill-window -t {newly_added_screen_window}')
    cmds_to_be_run = ';'.join(screen_cmds+preprocesses+[get_command(reqd_params)]+postprocesses)
    subprocess.Popen(f'tmux send-keys -t {newly_added_screen_window} "{cmds_to_be_run}" Enter', shell=True)

  all_configs = tuple(product(*vars))
  grouped_configs = group_configs(all_configs, max_runs)

  for configs in grouped_configs:
    tmp_fpath = os.path.join(os.getcwd(), 'run.tmp')
    validate_run()
    create_screen_windows(len(configs))
    newly_added_screen_windows = [str(i) for i in range(1, len(configs)+1)]

    for reqd_var, newly_added_screen_window in zip(configs, newly_added_screen_windows):
      execute(reqd_var, newly_added_screen_window)  
    
    while True:
      has_finished = check_execution_status(tmp_fpath)
      if has_finished:
        subprocess.run(f'rm -r {tmp_fpath}', shell=True)
        break
      time.sleep(check_freq)
