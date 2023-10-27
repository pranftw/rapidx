from lightning.pytorch.callbacks import Callback
import importlib
import argparse
import sys
import os
import glob



class LogCallback(Callback):
  def __init__(self, print_freq=1, metrics=['loss']):
    self.print_freq = print_freq
    self.metrics = metrics

  def on_train_batch_end(self, trainer, pl_module, outputs, batch, batch_idx):
    self.validate_outputs(outputs)
    for metric in self.metrics:
      pl_module.log(f'train_{metric}', outputs[metric], on_step=False, on_epoch=True, prog_bar=True, logger=True)
  
  def on_validation_batch_end(self, trainer, pl_module, outputs, batch, batch_idx, dataloader_idx=0):
    self.validate_outputs(outputs)
    for metric in self.metrics:
      pl_module.log(f'val_{metric}', outputs[metric], on_step=False, on_epoch=True, prog_bar=True, logger=True)
  
  def on_test_batch_end(self, trainer, pl_module, outputs, batch, batch_idx, dataloader_idx=0):
    self.validate_outputs(outputs)
    for metric in self.metrics:
      pl_module.log(f'test_{metric}', outputs[metric], on_step=False, on_epoch=True, logger=False)

  def on_train_epoch_end(self, trainer, pl_module):
    if pl_module.current_epoch%self.print_freq==0:
      print('')

  def on_test_epoch_end(self, trainer, pl_module):
    for metric in self.metrics:
      print(f'test_{metric}: {trainer.callback_metrics[f"test_{metric}"].item():5f}')
  
  def validate_outputs(self, outputs):
    assert isinstance(outputs, dict), 'Outputs must be a dict!'
    for metric in self.metrics:
      assert outputs.get(metric) is not None, f'Metric {metric} not found in outputs!'


def get_parser():
  parser = argparse.ArgumentParser()
  parser.add_argument('--module_path', type=str, required=True)
  parser.add_argument('--module', type=str, default='Module')
  parser.add_argument('--devices', type=int, nargs='*', default=[0])
  parser.add_argument('--epochs', type=int, default=10)
  parser.add_argument('--batch_size', type=int, default=16)
  parser.add_argument('--num_workers', type=int, default=4)
  parser.add_argument('--output_dir', type=str, default='outputs')
  parser.add_argument('--print_freq', type=int, default=1)
  parser.add_argument('--metrics', type=str, nargs='*', default=['loss'])
  return parser


def setup_module(module_path):
  sys.path.append(module_path)
  pkgs_path = glob.glob(os.path.join(module_path, '*/lib/*/site-packages')) or None
  if pkgs_path is not None:
    assert len(pkgs_path)==1, f'Found multiple site-packages directory! {pkgs_path}'
    sys.path.append(pkgs_path[0])


def get_module(module_path, module):
  setup_module(module_path)
  lgt_module = importlib.import_module('lgt_module')
  Module = lgt_module.__getattribute__(module)
  return Module