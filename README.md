# SAGE Galaxy Formation Model - Particle Swarm Optimization

This project performs Particle Swarm Optimization (PSO) on the SAGE semi-analytic galaxy formation model to calibrate its free parameters against observational constraints.

## Overview

The SAGE PSO system allows you to automatically calibrate parameters in the SAGE semi-analytic galaxy formation model to match various observational constraints. The system:

- Uses Particle Swarm Optimization to efficiently search the parameter space
- Supports multiple observational constraints (stellar mass function, black hole mass function, etc.)
- Handles parallelization for faster computation
- Works both on local machines and HPC clusters with SLURM
- Generates diagnostic visualizations of results

## Requirements

- Python 3.x
- NumPy
- SciPy
- Pandas
- Matplotlib
- Seaborn
- h5py
- openmp
- openmpi
- gcc

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/sage-pso.git
   cd sage-pso
   ```

2. Ensure you have SAGE compiled and available:
   ```bash
   # Example path to SAGE binary
   export SAGE_BINARY=/path/to/sage
   ```

3. Install required Python packages:
   ```bash
   pip install numpy scipy pandas matplotlib seaborn h5py
   ```

## Usage

### Basic Run

1. Configure your run in `run_pso.sh`:
   ```bash
   # Edit the configuration parameters
   nano run_pso.sh
   ```

2. Run the optimization:
   ```bash
   ./run_pso.sh
   ```

### Key Configuration Options

- `CONFIG_PATH`: Path to the SAGE configuration file
- `BASE_PATH`: Path to the SAGE executable
- `OUTPUT_PATH`: Path to store the output files
- `PARTICLES`: Number of particles in the swarm
- `ITERATIONS`: Maximum number of iterations for the optimization
- `TEST`: Statistical test to use for evaluating the fit (e.g., "student-t")
- `CONSTRAINTS`: Comma-separated list of observational constraints (see below)
- `CSVOUTPUT`: Path to save the PSO results as a CSV file
- `SPACEFILE`: Path to the search space definition file
- `SNAPSHOT`: Snapshot number to analyze (redshift-dependent)
- `SIM`: Simulation type (0=miniUchuu, 1=miniMillennium, 2=MTNG)
- `BOXSIZE`: Size of simulation box in Mpc/h
- `VOL_FRAC`: Volume fraction of simulation
- `OMEGA0`: Omega_0 cosmological parameter
- `H0`: h_0 cosmological parameter

### Search Space Definition

The `space.txt` file defines the search space for the PSO. Each line contains:

```
ParameterName,PlotLabel,IsLogFlag,LowerBound,UpperBound
```

Example:
```
SfrEfficiency,SFE,0,0.001,0.1
FeedbackReheatingEpsilon,eHeat,0,0.05,3.0
FeedbackEjectionRatio,eEject/eHeat,0,0.005,0.15
ReIncorporationFactor,eRein,0,0.01,0.3
RadioModeEfficiency,eRadio,0,0.001,0.15
QuasarModeEfficiency,eQuasar,0,0.001,0.015
BlackHoleGrowthRate,eBhgrow,0,0.005,0.2
```

### Supported Observational Constraints

The following constraints are available:

#### Stellar Mass Function (SMF) at various redshifts:
- `SMF_z0`: z = 0
- `SMF_z02`: z = 0.2
- `SMF_z05`: z = 0.5
- `SMF_z08`: z = 0.8
- `SMF_z10`: z = 1.0
- `SMF_z11`: z = 1.1
- `SMF_z15`: z = 1.5
- `SMF_z20`: z = 2.0
- `SMF_z24`: z = 2.4
- `SMF_z31`: z = 3.1
- `SMF_z36`: z = 3.6
- `SMF_z46`: z = 4.6
- ... (through z = 10.4)

#### Black Hole Constraints:
- `BHMF_z0` to `BHMF_z100`: Black Hole Mass Function at redshifts 0 to 10
- `BHBM_z0`: Black Hole - Bulge Mass Relation at z = 0
- `BHBM_z20`: Black Hole - Bulge Mass Relation at z = 2.0

#### Halo Stellar Mass Relation:
- `HSMR_z0` to `HSMR_z40`: Halo Stellar Mass Relation at redshifts 0 to 4.0

### Applying Constraint Weights

You can adjust the weight of each constraint using the asterisk syntax:
```
CONSTRAINTS="SMF_z0*0.5,BHBM_z0*0.3,BHMF_z0*0.2"
```

You can also limit the domain range for constraints:
```
CONSTRAINTS="SMF_z0(8-11)*1.0"
```

### HPC Usage

For running on HPC clusters with SLURM, enable HPC mode with additional options:

```bash
python main.py -H -C 16 -M 4000m -w 2:00:00 -a myaccount -q standard -u username [other options]
```

Where:
- `-H`: Enable HPC mode
- `-C`: Number of CPUs per SAGE instance
- `-M`: Memory per SAGE instance
- `-w`: Walltime for jobs
- `-a`: Account for job submission
- `-q`: Queue/partition to submit to
- `-u`: Username for SLURM

## Output and Diagnostics

After running the PSO, several output files and visualizations are generated in the output directory:

1. **Parameter values**: CSV files with optimized parameter values
2. **Iteration plots**: Shows how the model fits to observational data across iterations
3. **Parameter correlations**: Visualizations of parameter relationships and uncertainties
4. **Diagnostic plots**: Various plots showing convergence and constraint satisfaction

The main diagnostic plots include:
- Stellar Mass Function comparisons
- Black Hole Mass Function comparisons
- Black Hole - Bulge Mass relations
- Halo Stellar Mass Relations
- Parameter distribution plots
- Correlation plots between parameters

## Project Structure

- `main.py`: Main entry point for the PSO process
- `pso.py`: Implementation of the PSO algorithm
- `constraints.py`: Implementations of observational constraints
- `execution.py`: Handles the execution of SAGE for particle evaluation
- `analysis.py`: Functions for analyzing the results
- `diagnostics.py`: Creates diagnostic visualizations
- `common.py`: Common utility functions
- `routines.py`: Utility functions for reading and processing data
- `pso_uncertainty.py`: Analysis of parameter uncertainties

## Troubleshooting

### Common Issues

1. **SAGE binary not found**: 
   ```
   Error: No SAGE binary found, specify one via -b
   ```
   Solution: Ensure the SAGE binary path is correct in your script.

2. **Missing data files**:
   ```
   Error: File not found
   ```
   Solution: Check that all required observational data files are in the correct location.

3. **HPC job failures**:
   Solution: Check SLURM logs in the output directory for specific error messages.

4. **Memory issues**:
   Solution: Reduce the number of particles or increase the memory allocation.

## References

If using this code in academic work, please cite the following papers:

- SAGE model: Croton et al. (2016)
- Observational constraints:
  - Stellar Mass Function: Driver et al. (2022), Shuntov et al. (2024)
  - Black Hole Mass Function: Zhang et al. (2023)
  - Black Hole - Bulge Mass Relation: Häring & Rix (2004)
  - Halo Stellar Mass Relation: Moster et al. (2013)

## License

This code is released under the GNU General Public License v3. See the LICENSE file for details.