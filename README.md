# Jupyter notebooks for data processing and analysis

This repository contains Jupyter notebooks related to the PhD thesis entitled

> Modeling and simulation of convection-dominated species transfer at rising bubbles

This project was funded by the German Reseach Foundation (DFG) within the priority program [SPP1740 Reactive Bubbly Flows](http://www.dfg-spp1740.de/) under the grand *BO 1879/13-2*. The work was supervised by [Prof. Dr. rer. nat. Dieter Bothe](mailto:bothe@mma.tu-darmstadt.de) and conducted at the [Institute for Mathematical Modeling and Analysis](https://www.mma.tu-darmstadt.de/index/index.en.jsp) at the Technical University of Darmstadt.

## Dependencies

The Jupyter notebooks may be executed using
- a local installation of all relevant Python packages or
- the provided Docker image (recommended).

### Docker

Why should you bother using Docker and the (small) logistic overhead it creates? The provided Docker image contains a Jupyter and Python environment with all dependencies to run notebooks and scripts. This encapsulation of dependencies ensures that all results are reproducible independent of the underlaying host operating system and the software stack installed thereon. Also results containing some *random* component, e.g. the initialization of model weights, are to some extend reproducible. Such notebooks contain a *seed* for numpy and pyTorch in the first notebook cell. You will obtain the published results by running *Kernel -> Restart & Run All*. Repeatedly executing some of the cells will lead to varying results.

Any installed version of [Docker](https://docs.docker.com/install/) larger than **1.10** will be able to pull and execute the Docker image hosted on [Dockerhub](https://hub.docker.com/r/andreweiner/jupyter-environment). There are convenience scripts to create and start a Docker container which require root privileges. To avoid running the scripts with *sudo*, follow the [post-installation steps](https://docs.docker.com/install/linux/linux-postinstall/).

### Local execution

The notebooks and modules are implemented in Python 3. Non-standard packages installed on the Docker image are:

- Ipython: 7.8.0
- Matplotlib: 2.1.1
- Numpy: 1.13.3
- Pandas: 0.22.0
- PyTorch: 1.2.0+cpu
- Scikit Learn: 0.21.3

Further information may be found in [this](https://github.com/AndreWeiner/phd_notebooks/blob/master/notebooks/show_package_versions.ipynb) notebook and in the [Dockerfile](https://github.com/AndreWeiner/phd_notebooks/blob/master/Dockerfile).

## Getting the data

The full data set required to run the notebooks and to reproduce all temporary and final results can be downloaded [here](https://tudatalib.ulb.tu-darmstadt.de/bitstream/handle/tudatalib/2267.2/full_notebook_data_18_03_2020.tar.gz?sequence=2&isAllowed=y). Move the downloaded tar-ball to the top-level folder of the repository such that the output of *ls* looks similar to

```
~$ ls
full_notebook_data_18_03_2020.tar.gz  notebooks README.md ...
```

To extract the archive, run:
```
tar xvzf full_notebook_data_18_03_2020.tar.gz
```
The archive contains raw data and intermediate results produced by some of the notebooks. The raw data was produced using Basilisk (two-phase volume-of-fluid simulations) and OpenFOAM (single phase flow dynamics and species transport). For more information, refer to the [Basilisk repository](https://github.com/AndreWeiner/phd_basilisk), the [OpenFOAM repository](https://github.com/AndreWeiner/phd_openfoam), and chapter 6.1 of my [thesis](https://tuprints.ulb.tu-darmstadt.de/cgi/users/home?screen=EPrint%3A%3AView&eprintid=11405). The general workflow to obtain a species transport solution may be outlined as follows:

1. run a Basilisk volume-of-fluid simulation
2. use the [process_plic_data.ipynb](https://github.com/AndreWeiner/phd_notebooks/blob/master/notebooks/process_plic_data.ipynb) to assemble and clean the Basilisk PLIC (piecewise linear interface calculation) data
3. optional: use [process_logs.ipynb](https://github.com/AndreWeiner/phd_notebooks/blob/master/notebooks/process_logs.ipynb) if you ran your simulations on a cluster with multiple restarts; this script might have to be modified depending on your resources and batch system
4. create the STL files to be used in OpenFOAM; for ellipsoidal and spherical cap bubbles have a look at [basilisk_2D_shape_approximation_simple.ipynb](https://github.com/AndreWeiner/phd_notebooks/blob/master/notebooks/basilisk_2D_shape_approximation_simple.ipynb); for dimpled ellipsoidal and skirted bubbles refer to [basilisk_2D_shape_approximation_complex.ipynb](https://github.com/AndreWeiner/phd_notebooks/blob/master/notebooks/basilisk_2D_shape_approximation_complex.ipynb)
5. run single phase flow dynamics and species transport in OpenFOAM
6. run Jupyter notebooks for post-processing

## Running notebooks

### Docker

The script [create_jupyter_container.sh](https://github.com/AndreWeiner/phd_notebooks/blob/master/create_jupyter_container.sh) creates a special container with all relevant mappings between host and container (directories and files). The script has to be executed **once only**:

```
./create_jupyter_container.sh
```
To start the container and access the notebooks, run:

```
./start_notebooks.sh
```
and open the URL displayed in the command line in your web browser. The URL should start with *http://127.0.0.1:8888/?token=...*

### Local execution

With a standard Jupyter installation and all required packages available on the system, a notebook may be started by running:

```
jupyter-notebook name_of_the_notebook.ipynb
```

## Creating the Docker image

The Docker image is tagged with the Git hash based on which the image was created. To create an image based on the last commit, run:
```
docker build -t andreweiner/jupyter-environment:$(git log -1 --format=%h) .
```

## How to reference

The Jupyter notebooks in this repository accompany the following publication:

```
@phdthesis{tuprints11405,
            year = {2020},
         address = {Darmstadt},
          school = {Technical University of Darmstadt, Mathematical Modeling and Analysis},
          author = {Andre Weiner},
           title = {Modeling and simulation of convection-dominated species transfer at rising bubbles},
           month = {February},
            url = {http://tuprints.ulb.tu-darmstadt.de/11405/}
}
```
