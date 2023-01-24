# Timing Analysis for SOME/IP Service Discovery
This repository contains a python code that computes the `discovery time` for a given Client/Service pair using SOME/IP Service Discovery (SD). The `discovery time` is the time taken by the client to discover the desired service, by means of the Service Discovery process.

The scripts implementing the analysis are contained in the `notebooks/timing/` folder, specifically the `notebooks/timing/timing_analysis.py` script.

## Folder Structure
- `notebooks`: The root contains a series of jupyter notebooks that shows how the timing analysis works;
  - `notebooks/figure`: Contains figures that are produced by the notebooks;
  - `notebooks/plot`: Contains python scripts for visualizing SOME/IP scenarios;
  - `notebooks/timing`: Contains python scripts for computing SOME/IP discovery time;
