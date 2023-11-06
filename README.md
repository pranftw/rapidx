# rapidx
#### rapidx - A toolbox that integrates with PyTorch Lightning which helps in running and managing multiple codebases

### Docs/comments will be added soon. Please bear until then. Highly recommended to play around and customize it even more acoording to your needs.

## Motivation
Suppose you've embarked on a PyTorch based deep learning research project that involves experimenting with ideas from multiple papers with each of them having their own separate codebases. Each of these codebases usually have their own set of requirements that needs to be managed through activating the right virtual environment during execution, their own way of logging metrics, separate set of commandline arguments, different code structure, training pipelines and whatnot. Managing all these is a messy affair. Hence in order to streamline the entire process, **rapidx** was created which stands for Rapid Experimentation(it's lame, ik, but ehh).

## Features
  - Manage multiple virtual environments, each with its own set of requirements and activated dynamically while a particular module is being executed.
  - Streamlines logging metrics
  - Training pipeline implemented through `LightningModule` that brings uniformity
  - All configs handled through `argparse` and args specific to a particular module can be specified
  - Logging through `TensorBoardLogger`
  - A single `run.py` file to interface with all the codebases
  - `multiple_screens.py` allows you to run a module with different configs in parallel within a TMUX session. Useful for testing multiple experiment configs or hyperparameter tuning

## Installation
```bash
git clone https://github.com/pranftw/rapidx.git
cd rapidx
python -m venv venv # create a virtual environment
source venv/bin/activate # activate the virtual environment
pip install -r requirements.txt # install requirements
```

## Example
A basic MNIST example is provided for reference.
```bash
cd modules/mnist
python -m venv mnist_venv # create a virtual environment for this module
source mnist_venv/bin/activate # activate the virtual environment
pip install -r requirements.txt # install requirements
deactivate
cd ../..
source venv/bin/activate # activate the common virtual environment
python run.py --module_path modules/mnist
# running multiple configs. make sure you're in a TMUX session with only window 0 present
cd scripts
python run_mnist.py
```

## Instructions/Notes
  - Create a subdir with the module name in `modules`
  - If the original codebase' training pipeline is in plain PyTorch, convert it to PyTorch-Lightning yourself or ask copilot to do it haha
  - Within each module implement a PyTorch-Lightning `LightningModule` module that is present either as `lgt_module.py` file or `lgt_module` package
  - Each module might've its own requirements that needs to be installed, so make sure that it is done
  - Currently only virtual env is supported for each module (conda environment might be supported in the future if required)
  - Ensure that each `LightningModule` child implements a `get_parser()` static method which helps parse arguments related to the module
  - Implement a method to return the dataloaders in `data.py` corresponding to the name of the module
  - Outputs of all *_step in `LightningModule` needs to be returned as a dict

## Code Structure
  - `data.py` - Contains the dataloaders
  - `run.py` - Main file which is used to execute modules
  - `utils.py` - Helper functions
  - Each module in `modules` dir contains either `lgt_module.py` or `lgt_module` package which will be utilized by
  `run.py` to execute the module


## If you use this software in your work, please cite it using the following BibTeX
```
@software{Sastry_rapidx_2023,
author = {Sastry, Pranav},
month = nov,
title = {{rapidx - A toolbox that integrates with PyTorch-Lightning which helps in running and managing multiple codebases}},
url = {https://github.com/pranftw/rapidx},
version = {0.0.1},
year = {2023}
}
```