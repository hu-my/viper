# ViperGPT: Visual Inference via Python Execution for Reasoning

This is the code for the paper [ViperGPT: Visual Inference via Python Execution for Reasoning](https://viper.cs.columbia.edu) by [Dídac Surís](https://www.didacsuris.com/)\*, [Sachit Menon](https://sachit-menon.github.io/)\* and [Carl Vondrick](https://www.cs.columbia.edu/~vondrick/).

![teaser](teaser.gif "Teaser")

## Quickstart
Clone recursively:
```bash
git clone --recurse-submodules https://github.com/cvlab-columbia/viper.git
```

After cloning:
```bash
cd viper
export PATH=/usr/local/cuda/bin:$PATH
bash setup.sh  # This may take a while. Make sure the vipergpt environment is active
cd GLIP
python setup.py clean --all build develop --user
cd ..
echo YOUR_OPENAI_API_KEY_HERE > api.key
```
Then you can start exploring with the `main_simple.ipynb` notebook. For running on datasets instead of individual 
examples, use `main_batch.py` as discussed later on.

> :warning: WARNING: ViperGPT runs code generated by a large language model. We do not have direct control over this 
> code, so it can be dangerous to run it, especially if modifications to the API are made (the current prompts do not 
> have any dangerous functions like interaction with the filesystem, so it is unlikely that any malicious code can be 
> generated). We cannot guarantee that the code is safe, so use at your own risk, or run in a sandboxed environment.
> For this reason, the default `execute_code` parameter in the config is `False`. Set it to `True` if you would like the 
> generated code to be executed automatically in `main_batch.py`, otherwise you can execute it yourself (as in 
> `main_simple.ipynb`). 


> :information_source: NOTE: OpenAI discontinued support for the Codex API on March 23rd, 2023. This repository implements
> GPT-3.5 Turbo and GPT-4 as alternatives, but we have not tested them extensively; as they are chat models and not completion, their behavior likely differs.

## Detailed Installation
The easiest way to get started exploring ViperGPT is through `main_simple.ipynb`. To run it, you will need to do the following:
1. Clone this repository with its submodules.
2. Install the dependencies. See the see [Dependencies](#Dependencies).
3. Download two pretrained models (the rest are downloaded automatically). See [Pretrained models](#Pretrained-models).
4. Set up the OpenAI key. See [OpenAI key](#OpenAI-key).

### Cloning this Repo

```bash
git clone --recurse-submodules https://github.com/cvlab-columbia/viper.git
```

### Dependencies

First, create a conda environment using `setup_env.sh` and then install our modified version of GLIP. 
To do so, just `cd` into the `viper` directory, and run:

```bash
export PATH=/usr/local/cuda/bin:$PATH
bash setup_env.sh
conda activate vipergpt
cd GLIP
python setup.py clean --all build develop --user
```

Please make sure to install GLIP as described (i.e., from our provided repo) as we have updated the CUDA kernels to be 
compatible with newer versions of PyTorch, which are required for other models.

### Pretrained models

Note that ViperGPT may inherit biases from the pretrained models it uses. These biases may be reflected in the outputs 
generated by our model. It is recommended to consider this potential bias when using ViperGPT and interpreting its 
outputs.

This repository implements more models than the ones described in the paper, which can be useful for further research.
Most of the implemented modules automatically download the pretrained models. However, there are four models that 
need to be downloaded manually, if they are to be used. They have to be stored in the same directory 
`/path/to/pretrained_models`, by default `./pretrained_models/`, which has to be specified in the configuration (see [Configuration](#Configuration)).

We provide the convenience script `download_models.sh` to perform this download for you; you can set the variable $PRETRAINED_MODEL_PATH match your config's `/path/to/pretrained_models/`.

#### Pretrained model system requirements

Many of the models used are very large, and require quite a bit of GPU memory. In particular, GLIP and BLIP2 are especially large. Please use smaller variants of those models if running on hardware that cannot support the larger ones; however, this comes at the expense of performance.

### OpenAI key

To run the OpenAI models, you will need to configure an OpenAI key. This can be done by signing up for an account [e.g. here](https://platform.openai.com/), and then creating a key in [account/api-keys](https://platform.openai.com/account/api-keys).
**Create a file `api.key` and store the key in it.**

## Running the code

Once the previous steps are done, you can run the Jupyter Notebook `main_simple.ipynb`. This notebook contains 
the code to try ViperGPT on your own images. The notebook is well documented, and it describes how to use the code.

## Dataset

You can run ViperGPT on a pre-defined set of query-image/video pairs as well. In order to do that, you will have to 
create a `queries.csv` file, which contains the queries and the filenames for the corresponding images/videos. The format of the file is
`query,answer,image_name/video_name`. The answer is optional, and only needed for evaluation. See `data` for an example.

Your dataset directory will contain the `queries.csv` file as well as the images/videos in the `images`/`videos` 
directory. Add the path to the dataset directory in the configuration (see [Configuration](#Configuration)).

## Configuration

All the configuration parameters are defined in `configs/base_config.yaml`. In order to run the code,
modify the paths in the parameters `path_pretrained_models` and optionally `dataset.data_path` to point to the correct 
directories.

For every new configuration you need to run, create a new yaml file in the `configs` directory (like `my_config.yaml`), 
and modify the parameters you need to change. The parameters in the new file will overwrite 
the ones in `base_config.yaml`. Any number of configuration files can be specified, they will be merged in the order 
they are specified in the command line.

The `multiprocessing` parameter refers to *both* the batch (every sample is run by a different worker) and the models 
(every model runs in its own process).

## Running the code on a dataset, without the Jupyter notebook

The code can be run using the following command:

```bash
CONFIG_NAMES=your_config_name python main_batch.py
```

`CONFIG_NAMES` is an environment variable that specifies the configuration files to use.

If you want to run the code using multiprocessing, set `multiprocessing: True` in the config file.

It is especially important to consider the risks of executing arbitrary code when running in a batch; in particular, if you modify the API or any inputs to Codex, be mindful to not include potentially damaging abilities such as file modification/deletion.

## Code structure

The code is prepared to run in a multiprocessing manner, from two points of view. First, it runs the models in parallel,
meaning that each pretrained model runs in its own process. Second, it runs the samples in parallel, meaning that 
several workers are created to run the samples for a given batch. There is a producer-consumer queuing mechanism where 
the processes controlling the models are the consumers of inputs coming from the workers that run each sample 
(producer). Our implementation allows for batching of samples, which means that several workers can send their inputs to
the same model process, which will run them as a batch, and return the output to each worker separately. 

The code has comments and docstrings, but here is a brief overview of the code structure:
- `vision_models.py`: Contains the code for the pretrained models. Each one of them is a subclass of `BaseModel`.
Implementing a new model is easy. Just create a new class that inherits from `BaseModel` and implement the `forward` 
method, as well as the `name` method. The latter will be used to call the model. 
- `vision_processes.py`: Acts as a bridge between the models and the rest of the code. It contains the code for to start 
all the required processes, whether multiprocessing or not. It automatically detects all the new models implemented in
`vision_models.py`. It defines a `forward` method that takes a name as input (as well as arguments), and calls the 
appropriate model.
- `main_batch.py` and `main_simple.ipynb`: These are the main files to run the code. The former runs the whole dataset and 
is suited for parallel processing of samples, while the latter runs a single image/video and is suited for debugging.
- `image_patch.py` and `video_segment.py`: These are the classes that represent the image patches and video segments.
They contain all the methods that call the `forward` method of `vision_processes.py` and therefore call the models.
- `configs`: Directory containing the configuration files. The configuration files are in YAML format, and read using 
OmegaConf.
- `datasets`: Directory containing the code for the datasets. The datasets are subclasses of `torch.utils.data.Dataset`.
- `prompts`: Directory containing the prompts for Codex and GPT-3. The Codex ones define the API specifications.
- `utils.py`, `useful_lists` and `base_models`: Auxiliary files containing useful functions, lists and pretrained model 
implementations.

## Citation

If you use this code, please consider citing the paper as:

```
@article{surismenon2023vipergpt,
    title={ViperGPT: Visual Inference via Python Execution for Reasoning},
    author={D\'idac Sur\'is and Sachit Menon and Carl Vondrick},
    journal={arXiv preprint arXiv:2303.08128},
    year={2023}
}
```