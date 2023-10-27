from torchvision.models import resnet18
from torch import nn
import torch
import lightning.pytorch as pl
import torchmetrics
import torch.nn.functional as F



class Module(pl.LightningModule):
  def __init__(self, args):
    super().__init__()
    self.args = args
    self.resnet = resnet18(num_classes=10)
    self.resnet.conv1 = nn.Conv2d(1, 64, kernel_size=7, stride=2, padding=3, bias=False)
    self.accuracy = torchmetrics.Accuracy('multiclass', num_classes=10)
  
  def forward(self, inputs):
    return self.resnet(inputs)
  
  def configure_optimizers(self):
    return torch.optim.Adam(self.parameters(), 1e-3)
  
  def training_step(self, train_batch, batch_idx):
    loss, accuracy = self.step(train_batch)
    return {'loss': loss}
  
  def validation_step(self, val_batch, val_idx):
    loss, accuracy = self.step(val_batch)
    return {'loss': loss}
  
  def test_step(self, test_batch, test_idx):
    loss, accuracy = self.step(test_batch)
    return {'loss': loss}
  
  def step(self, batch):
    inputs, targets = batch
    outputs = self.forward(inputs)
    preds = self.get_preds(outputs)
    loss = F.cross_entropy(outputs, targets)
    accuracy = self.accuracy(preds, targets)
    return loss, accuracy
  
  def get_preds(self, outputs):
    return torch.argmax(F.softmax(outputs, dim=1), dim=1)
  
  @staticmethod
  def get_parser():
    pass