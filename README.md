# VN-Power-Scenario
A recursive model of electricity production in Vietnam

(c) Minh Ha-Duong, An Ha Truong, CNRS, 2016–2018  < minh.haduong@gmail.com >

All files licensed under the Creative Commons Attribution-ShareAlike 4.0 International,
see file `LICENSE`, unless noted otherwise.

The model is a recursive simulation based on OSeMOSYS equations. It produces the
tables and figures of two papers: one on carbon capture and storage (CCS) in
Vietnam's power development plan, one on the sensitivity of the plan's costs to
international coal and gas prices ("moreGas").


## Reproducibility in three steps:
```bash
git clone https://github.com/MinhHaDuong/VN-Power-Scenario.git
cd VN-Power-Scenario/
make
```
This needs [uv](https://docs.astral.sh/uv/); see below.

## Installation and use:

The code is in Python 3 (locked on 3.11).
It imports hashlib, collections, functools, random, sys, and warnings from the standard library,
pandas, matplotlib, numpy, and scipy from the scientific Python core packages,
and statsmodels from PyPI.

Dependencies are declared in `pyproject.toml` and locked in `uv.lock`
(Python 3.11, pandas < 2, numpy < 2: the code uses `DataFrame.append`).
With uv installed, `uv sync` builds the `.venv`;
`make` runs every recipe through `uv run --frozen`, so no activation is needed.
Inside an already activated virtual environment, or where uv is absent,
recipes run the tools directly.

The build uses a standard `Makefile` with

+  `make`               build all tables and figures for both papers, in parallel (`make all -j`).

+  `make all-CCS`       build the tables and figures of the CCS paper only.

+  `make all-moreGas`   build the tables and figures of the international prices paper only.

+  `make test`          run the regression tests, doctests, and scripted tests.
                        It leaves the working tree as it found it: generated outputs are kept.

+  `make regtest-reset` re-record the expected regression outputs in `_regtest_outputs/`,
                        after a change of results you have checked and accept.

+  `make coverage`      run the tests with coverage and build the HTML report in `htmlcov/`.

+  `make lint`, `make docstyle`, `make codestyle`   run pylint, pydocstyle, and pycodestyle.

+  `make clean`         delete the generated tables and figures.

+  `make cleaner`       also delete Python caches and coverage files.

Each output is rebuilt only when its own script changes, not when a module it imports
or a file in `data/` changes. After changing the model or the data, rebuild everything
with `make clean all`.

The generated tables and figures are listed in `.gitignore`.

## Development:

`pylintrc` sets the maximum line length to 100.
pycodestyle reads user settings from `~/.config/pycodestyle`, for instance
```
[pycodestyle]
max-line-length = 100
ignore = W503,E402
```

The file `pre-commit` is a git hook running `make cleaner`, `docstyle`, `codestyle`,
and `test` before each commit. To install it, from the `.git/hooks` directory run
`ln ../../pre-commit pre-commit`; skip it with `git commit --no-verify`.
Note that it uses `git stash`, and that `make cleaner` deletes the generated outputs.

## Directory organization:

1. Files in `data/` are raw data collected (PDF, XLS, ODS, CSV, web pages) from the web.

2. Intermediate CSV or TXT (when used), are also in `data/`.

3. Files starting with `data_X` mostly make available the data found in `data/X/`.

4. Files starting with an upper case letter define the class with that name: `Plan`, `Parameter`, `Run`.

5. Files starting with `plan_` instantiate a `Plan` object.

6. Files starting with `parameter_` instantiate a `Parameter` object.

7. Files starting with `run_` instantiate one or more `Run` objects.

8. Files `prices_data_*.py`, `production_data_local.py`, and `price_fuel.py` build the
   coal and gas price and production series, including random international price
   trajectories, for the international prices paper.

9. Files starting with `figure_` plot figures for the papers.

10. `init.py` holds common functions, constants and units.

11. Files starting with `test_` are used by the pytest framework.

12. Files in `_regtest_outputs/` are the expected outputs for regression testing
    (pytest-regtest). Use `make regtest-reset` to update them.
