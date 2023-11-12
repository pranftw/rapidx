from tensorboard.backend.event_processing import event_accumulator



def get_scalar_values(tf_event_fpaths, reqd_tags, max_epochs=None, num_vals=1):
  # num_vals=1 -> get only the last(final) value at the end of all the epochs for scalars
  # max_epochs is used to check if execeution has finished by checking if last value of epoch+1==max_epochs
  # not checked if max_epochs=None
  values = {}

  for event_fpath in tf_event_fpaths:
    event_values = {}
    ea = event_accumulator.EventAccumulator(event_fpath, size_guidance={event_accumulator.SCALARS: num_vals})
    ea.Reload()

    try:
      epochs_completed = int(ea.scalars.Items('epoch')[-1].value)
    except KeyError:
      print(f'NOT FINISHED: {event_fpath}')
      continue
    if max_epochs is not None and epochs_completed+1!=max_epochs:
      print(f'NOT FINISHED: {event_fpath}, EPOCHS_COMPLETED: {epochs_completed+1}')
      continue
    
    for tag in reqd_tags:
      event_values[tag] = [item.value for item in ea.scalars.Items(tag)]
    values[event_fpath] = event_values
  return values