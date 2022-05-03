#!/bin/bash
python3 -m pip install --upgrade pip
python3 -m pip install --upgrade build
python3 -m build
python3 -m pip install -U sphinx && mkdir docs && cd docs && sphinx-quickstart && make html
