# PyProduct 

## Dependencies

### Using Virtual Environments
An environment is just a place for dependencies like external libs like FastAPI and numpy, so the global libs for your system wont be disrupted. I think. Python has its own command for it:
```shell
$ python -m venv <name_of_venv_directory>
```
Then activate it with the scripts in venv\Scripts\ which will show up on the terminal as (venv) or (<name_of_venv_directory>)

### Using pip
Use the requirements.txt to install libs:
```shell
$ pip install -r requirements.txt
```


## Running the Server
```shell
$ uvicorn main:app --reload
```