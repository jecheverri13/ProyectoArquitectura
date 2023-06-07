# Processor simulator

## Start development

### Requirements

- Python 3.10.x

### Installing dependencies

Create a virtual environment.

```shell
python -m venv venv
```

Activate the environment. (Remember to activate it on your IDE).

```shell
source venv/bin/activate
```

When finishing work you could deactivate the environment.

```shell
deactivate
```

Install pip dependencies

```shell
pip install -r requirements.txt
```

Anytime you install a new package add that to the requirements.txt file

```shell
pip freeze > requirements.txt
```

### Creating directories

If you need to create a new directory that contains python modules inside create an `__init__.py` file inside it.
This is used to indicate Python it is a package directory.

### Documentation

Create a docstring at the start of each Python file.
Create a docstring for each class/function.
Use typehints.
