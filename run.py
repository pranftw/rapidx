from torch import nn
from lightning.pytorch.loggers import TensorBoardLogger
from data import Data
from utils import get_parser, get_module, LogCallback
import lightning.pytorch as pl
import torch
import os



if __name__=='__main__':
  parser = get_parser()
  args, _ = parser.parse_known_args()

  MODULE_PATH = args.module_path
  MODULE = args.module
  DEVICES = args.devices
  EPOCHS = args.epochs
  BATCH_SIZE = args.batch_size
  NUM_WORKERS = args.num_workers
  OUTPUT_DIR = args.output_dir
  PRINT_FREQ = args.print_freq
  METRICS = args.metrics

  Module = get_module(MODULE_PATH, MODULE)
  module_parser = Module.get_parser()
  module_args, _ = module_parser.parse_known_args() if module_parser is not None else (None, None)

  train_dl, val_dl, test_dl = Data(MODULE_PATH.strip('/').split('/')[-1], module_args, BATCH_SIZE, NUM_WORKERS)()

  model = Module(module_args)
  logger = TensorBoardLogger(save_dir=OUTPUT_DIR)
  log_callback = LogCallback(PRINT_FREQ, METRICS)
  trainer = pl.Trainer(accelerator='gpu', devices=DEVICES, max_epochs=EPOCHS, logger=logger, enable_checkpointing=False, callbacks=[log_callback])
  trainer.fit(model, train_dl, val_dl)
  trainer.test(model, test_dl)
  trainer.save_checkpoint(os.path.join(trainer.logger.log_dir, 'checkpoints', 'last.ckpt'))