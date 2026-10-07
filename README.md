# Brayton Cycle Problem

A small computational analysis for the Brayton-cycle question.

## Parameter ranges

- Compressor isentropic efficiency, **ηc: 0.40–0.95**
- Turbine isentropic efficiency, **ηt: 0.40–0.95**
- Combustor pressure ratio, **πcc: 0.60–0.99**

The calculation evaluates **29,791 combinations** using 31 points for each parameter.

## Python implementation

Run:

`Brayton_Cycle_3D_Parameter_Study.py`

The script calculates the cycle thermal efficiency and generates the 3-D parameter plot.

## 3-D parameter study

The color represents calculated Brayton-cycle thermal efficiency.

![3-D Brayton cycle parameter study](plots/3D_parameter_study.svg)

## MATLAB version

The original MATLAB implementation is also retained:

`Brayton_Cycle_3D_Parameter_Study.m`
