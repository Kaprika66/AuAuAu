# Electron Transport in Molecular Junction
Our project is a continuation of the [study carried out by Dr Topolnicki and coworkers](https://pubs.acs.org/doi/full/10.1021/acs.jpcc.1c03210).

The aim is to develop a method for predicting key factors for electron transport in molecular junction. We work on data collected from Molecular Dynamics symulations of 8000 molecular junctions. Each file contains the chemical structure of the molecule along with linkers attached to the gold electrodes on both sides. For every one of them the electron transport coefficient was calculated. Discovering the factors that increase the efficiency of the process under study will allow better junctions to be designed. 



# Instalation

`For windows users:`  
*You may encounter difficulties during 
setting up this project (especially tensorflow decision forest library is not available on windows, and newest tensorflow versions >= 2.12 do not support GPU acceleration), so if wish to run it on microsoft OS it is recommended to use [WSL](https://techcommunity.microsoft.com/t5/windows-11/how-to-install-the-linux-windows-subsystem-in-windows-11/m-p/2701207).  
You may be also interested how to integrate WSL with visual studio code. Guide how to do it should be available [here](https://code.visualstudio.com/docs/remote/wsl).*

----
  

- Make sure you have [conda](https://conda.io/projects/conda/en/latest/user-guide/install/index.html) installed on yor system.
- Create conda environment from file:
```bash
conda env create  --file conda.yml
```
- Activate it
```bash
conda activate auauau_env
```
- Install dependencies from poetry.lock

----
`Note:`   
*This project was created on tensorflow 2.12 so this version will be installed automatically. It may be incompatible with your graphic card driver and cuda version, in that case it will still work, but without GPU acceleration. If you care about GPU you should create environment manually. List of all necessary packages can be found in [pyproject.toml](pyproject.toml) and [conda.yml](conda.yml) files.*

----
```bash
poetry install
```

- Setup pre-commit if you want to use git.
```bash
pre-commit install
```
