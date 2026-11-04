# VN-CSS-Scenario
A recursive model of electricity production in Vietnam

(c) Dr. Minh Ha-Duong, CNRS, 2017  < minh.haduong@gmail.com >

All files licensed under the  Creative Commons Attribution-ShareAlike 4.0 International
see file LICENSE.TXT unless noted otherwise


## Reproductibility in three steps:
```bash
git clone https://github.com/MinhHaDuong/VN-CSS-Scenario.git
cd VN-CCS-Scenario/ 
make
```

## Installation and use:

 The code is in Python 3 (locked on 3.11)
it imports  hashlib, sys, copy, functools  from the standard library
it imports  pandas, matplotlib, numpy, scipy  from the scientific python core packages
it uses statsmodels from the PyPI

Dependencies are declared in `pyproject.toml` and locked in `uv.lock`
(Python 3.11, pandas < 2, numpy < 2: the code uses `DataFrame.append`).
With [uv](https://docs.astral.sh/uv/) installed, `uv sync` builds the `.venv`;
`make` runs every recipe through `uv run --frozen`, so no activation is needed.

The builds uses a standard  `Makefile`  with

+  `make`         run the model, all sensitivity analysis to build all tables and figures.

+  `make test`    perform regression tests, docstests, and scripted tests (if any)

+  `make reg_tests_reset`   copy results tables from the current dir into tables.tocompare/

+  `make clean`   delete results files

+  `make cleaner` delete results files and Python cache files

## Development:

Under Linux, spyder3 reads editor configuration from `~/.config/pep8`
```[pep8]
max-line-length = 100
ignore=W503,E402
```

## Directory organization:

1. Files in `data/` are raw data collected (PDF, XLS, web pages) from the web.

2. Intermediate CSV or TXT (when used), are also in `data/`

3. Files starting with data_X mostly make available the data found in `data/X/`

4. Files starting with an Upper case define the class with that name: Plan, Parameter, Run

5. Files starting with plan_ instanciate a `Plan` object

6. Files starting with parameter_ instanciate a `Parameter` object

7. Files starting with run_ instanciate one or more `Run` object-s

8. Files starting with test_ are used by the  pytest  framework.

7. Files in `tables.tocompare` are used for regression testing. Use `make reg_tests_reset` to populate/update it.

## Code quality:
[![codebeat badge](https://codebeat.co/badges/37b259d7-4684-43a4-a78a-662f834ce83e)](https://codebeat.co/projects/github-com-minhhaduong-vn-ccs-scenario-master)

[![Codacy Badge](https://api.codacy.com/project/badge/Grade/a10c950d7cb24809bbe6d78552f7ffcf)](https://www.codacy.com/app/minh.haduong/VN-CSS-Scenario?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=MinhHaDuong/VN-CSS-Scenario&amp;utm_campaign=Badge_Grade)
