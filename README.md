# Timing Analysis for SOME/IP Service Discovery

This repository contains a python code that computes the `discovery time` for a given Client/Service pair using SOME/IP Service Discovery (SD). The `discovery time` is the time taken by the client to discover the desired service, by means of the Service Discovery process.

The scripts implementing the analysis are contained in the `notebooks/timing/` folder, specifically the `notebooks/timing/timing_analysis.py` script.

## Install

You can install the package by running the following command:

```python
pip install git+https://github.com/Galfurian/someip_timing_analysis.git --user
```

## Uninstall

You can remove the package by running the following command:

```python
pip uninstall someip-timing-analysis
```

## Folder Structure

- `someip_timing_analysis` : Contains the python source code to perform SOME/IP analyses:
- `notebooks` : The root contains a series of jupyter notebooks that shows how the timing analysis works;
