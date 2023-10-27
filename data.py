from torch.utils.data import DataLoader, random_split
from utils import setup_module
import importlib
import os



class Data:
  def __init__(self, module_name, module_args, batch_size, num_workers, root='./downloaded_data'):
    self.module_name = module_name
    self.module_args = module_args
    self.batch_size = batch_size
    self.num_workers = num_workers
    self.root = root
  
  def __call__(self):
    return self.__getattribute__(self.module_name)()
  
  def mnist(self):
    setup_module('modules/mnist')
    transforms = importlib.import_module('torchvision').__getattribute__('transforms')
    MNIST = importlib.import_module('torchvision.datasets').__getattribute__('MNIST')

    transform = transforms.Compose([
      transforms.ToTensor(),
      transforms.Normalize((0.5,), (0.5,)),
    ])
    train_set = MNIST(root=self.root, train=True, download=True, transform=transform)
    val_set, test_set = random_split(MNIST(root=self.root, train=False, download=True, transform=transform), [0.5, 0.5])
    train_dl = DataLoader(train_set, batch_size=self.batch_size, num_workers=self.num_workers, shuffle=True)
    val_dl, test_dl = [DataLoader(dset, batch_size=self.batch_size, num_workers=self.num_workers) for dset in [val_set, test_set]]
    return train_dl, val_dl, test_dl