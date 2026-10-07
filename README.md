# Brayton Cycle Problem

A small **100% Python** computational analysis for the Brayton-cycle question.

## Parameter ranges

- Compressor isentropic efficiency, **ηc: 0.40–0.95**
- Turbine isentropic efficiency, **ηt: 0.40–0.95**
- Combustor pressure ratio, **πcc: 0.60–0.99**

The calculation evaluates **29,791 combinations** using 31 points for each parameter.

## Python implementation

The complete calculation and plotting are contained in:

`Brayton_Cycle_3D_Parameter_Study.py`

Install the required packages:

```bash
pip install numpy matplotlib
```

Then run:

```bash
python Brayton_Cycle_3D_Parameter_Study.py
```

The script calculates the Brayton-cycle thermal efficiency and generates the 3-D graph in `plots/3D_parameter_study.svg`.

## 3-D parameter study

The 3-D graph is generated directly by the Python script using **Matplotlib** from the full 29,791-point parameter sweep. No pre-generated graph image is stored in the repository.

Run:

```bash
python Brayton_Cycle_3D_Parameter_Study.py
```

The script creates `plots/3D_parameter_study.png` locally.

## Project contents

- **Python:** calculation + 3-D visualization
- **NumPy:** numerical parameter sweep
- **Matplotlib:** graph generation
- **No MATLAB files required**
