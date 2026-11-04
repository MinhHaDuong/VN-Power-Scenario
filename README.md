# VN-Power-Scenario
A recursive model of electricity production in Vietnam

(c) Minh Ha-Duong, An Ha Truong, CNRS, 2016–2018  < minh.haduong@gmail.com >

All files licensed under the Creative Commons Attribution-ShareAlike 4.0 International,
see file `LICENSE`, unless noted otherwise.

## What the model does

The model estimates the costs and CO2 emissions of Vietnam's electricity sector
from 2016 to 2050 under alternative power development plans, starting from the
installed capacity history since 1975. It is a recursive
simulation with an annual time step, based on OSeMOSYS equations.

+ A `Plan` is a year-by-year path of capacity additions and retirements for
  13 technologies: coal, gas, oil, big hydro, small hydro, biomass, wind, solar,
  coal with CCS, gas with CCS, biomass with CCS, imports, and pumped storage.
  The baseline plan is Vietnam's Power Development Plan 7 Adjusted (PDP7A),
  extended from 2030 to 2050, with past capacities from the EVN 2016 annual report.
  Nuclear plants planned in PDP7A are replaced by gas, since the nuclear
  program was suspended in 2016.
+ A `Parameter` set holds the technical and economic assumptions: overnight costs,
  plant lifetimes, capacity factors, emission factors, fuel prices, discount rate,
  and carbon price. The reference uses median values from the OpenEI and IPCC
  reviews, a 6% discount rate, and a carbon price reaching 100 USD/tCO2 in 2050.
+ A `Run` combines a plan and a parameter set. It computes electricity produced,
  construction, fuel, and O&M costs, salvage value, CO2 emitted and captured,
  and the system levelized cost of electricity (LCOE). A pair of runs gives the
  cost difference and the cost of avoided emissions.

## Publications and studies

**Carbon capture and storage.** `make all-CCS` builds the tables and figures of

> Ha-Duong, Minh, and Hoang Anh Nguyen-Trinh. 2017. "Two scenarios for carbon
> capture and storage in Vietnam." *Energy Policy* 110: 559–569.
> https://doi.org/10.1016/j.enpol.2017.08.040

The paper refers to this repository under its former name, VN-CSS-Scenario;
GitHub redirects the old URL here. The With CCS plan (High CCS in the paper)
keeps coal dominant, with gas CCS pilots in 2024 and 2029 and the conversion
of coal and gas plants to CCS from 2035 to 2050. In the reference case it raises the system
LCOE from 60.5 to 69.9 USD/MWh and captures 2.7 GtCO2 to 2050.
`run_sensitivity_analysis_ccs.py` varies the discount rate, carbon price,
and other parameters.

**More gas, and international fuel price risk.** `make all-moreGas` builds the
tables and figures of an unpublished working draft (Minh Ha-Duong, 2018,
"Diversifying Vietnam electricity mix to reduce CO2 emissions and exposure to
international coal and gas prices risk"), which extends a student modeling
project by Alice Duval and Benjamin Vandenbussche (2018, "Diversifier le secteur
électrique vietnamien par plus de gaz peut-il réduire l'exposition au risque-prix
des combustibles fossiles ?"). The More gas plan installs as much new gas capacity
as coal capacity each year. At domestic fuel prices, its system LCOE is
58.0 USD/MWh against 60.5 for the baseline, a difference the draft judges small
against fuel price and parameter uncertainty, while emissions fall by 1.4 GtCO2.
`prices_data_international.py` generates correlated trajectories of imported
coal and gas prices (geometric Brownian motion fitted on World Bank series;
BP and EIA series are in `data/` but switched off in the code), and
`run_sensitivity_lcoe.py` computes the LCOE distribution over 100 such
trajectories for both plans.


## Reproducibility in three steps
```bash
git clone https://github.com/MinhHaDuong/VN-Power-Scenario.git
cd VN-Power-Scenario/
make
```
This uses [uv](https://docs.astral.sh/uv/) when installed; see below.

## Installation and use

The code is in Python 3 (locked on 3.11).
It imports hashlib, collections, functools, random, sys, and warnings from the standard library,
pandas, matplotlib, numpy, and scipy from the scientific Python core packages,
and statsmodels from PyPI.

Dependencies are declared in `pyproject.toml` and locked in `uv.lock`
(Python 3.11, pandas < 2, numpy < 2: the code uses `DataFrame.append`).
With uv installed, `uv sync` builds the `.venv`;
`make` runs every Python recipe through `uv run --frozen`, so no activation is needed.
Inside an already activated virtual environment, or where uv is absent,
recipes run the tools directly.

The build uses a standard `Makefile` with

+  `make`               build all tables and figures for both papers, in parallel (`make all -j`).

+  `make all-CCS`       build the tables and figures of the CCS paper only.

+  `make all-moreGas`   build the tables and figures of the international prices paper only.

+  `make test`          run the regression tests, doctests, and scripted tests.
                        It keeps the generated outputs; `git status` stays clean.

+  `make regtest-reset` re-record the expected regression outputs in `_regtest_outputs/`,
                        after a change of results you have checked and accept.

+  `make coverage`      build the HTML coverage report in `htmlcov/`; it runs the tests
                        with coverage unless `coverage.xml` already exists.

+  `make lint`, `make docstyle`, `make codestyle`   run pylint, pydocstyle, and pycodestyle.

+  `make clean`         delete the generated tables and figures.

+  `make cleaner`       also delete Python caches and coverage files.

Each output is rebuilt when the script that produces it changes, not when a module
it imports or a file in `data/` changes. After changing the model or the data, rebuild everything
with `make clean all`.

The generated tables and figures are listed in `.gitignore`.

## Development

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

## Directory organization

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

10. `init.py` holds common functions, constants, and units.

11. Files starting with `test_` are used by the pytest framework.

12. Files in `_regtest_outputs/` are the expected outputs for regression testing
    (pytest-regtest). Use `make regtest-reset` to update them.
