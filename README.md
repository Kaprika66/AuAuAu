# AuAuAu
Transport or something



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
