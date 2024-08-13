# Slang Parser

This repository provides an example of a parser for a simple programming language called Slang. The parser is implemented using Python, Pylasu and ANTLR - as discussed in the article ["Implement Parsers with Pylasu"](https://tomassetti.me/implement-parsers-with-pylasu/). 

The project also uses:
* [pdm](https://pdm-project.org/latest/) for dependency management and packaging;
* [tox](https://tox.wiki/en/4.12.1/) for task automation and orchestration;
* [ruff](https://docs.astral.sh/ruff/) for linting and formatting;
* [sphinx](https://www.sphinx-doc.org/en/master/) for generating basic documentation;

## Development

Running `pdm run tox` the following tasks will be executed:

* `antlr` - generate ANTLR Parser/Lexer;
* `format` - format the source code;
* `lint` - lint the source code;
* `test` - run all unit tests;
* `docs` - generate documentation;

Each tasks can also be executed singularly:
```
pdm run tox -e <task_name>
```
or with other specific ones:
```
pdm run tox -e <task_name_0>,...,<task_name_n>
```

## DevContainer Support
This project includes a configuration for DevContainers, eliminating the need to install any dependencies locally.

#### **Prerequisites:** 
Ensure you have Docker and Visual Studio Code (with the Dev Containers extension) installed.

#### **Launching the DevContainer:**
- Open the project in Visual Studio Code
- When prompted, choose to reopen the project in the DevContainer
- Alternatively, you can manually select `Dev Containers: Rebuild Container` from the Command Palette.

#### **Using the DevContainer:**
- All necessary dependencies are installed automatically inside the container.
- You can use the terminal within the DevContainer to run the development tasks mentioned above, such as `pdm run tox`.