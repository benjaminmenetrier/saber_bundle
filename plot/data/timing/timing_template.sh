#!/bin/bash
#SBATCH --job-name=__FILENAME__
#SBATCH --output=__TESTSUBDIR__/__FILENAME__-%J.out
#SBATCH --error=__TESTSUBDIR__/__FILENAME__-%J.out
#SBATCH --qos=np
#SBATCH --time=01:00:00
#SBATCH --account=nores
#SBATCH --nodes=1
#SBATCH --ntasks=__NTASK__
#SBATCH --cpus-per-task=1

# Go to the directory
cd __TESTSUBDIR__

# Run executable
export OMP_NUM_THREADS=${SLURM_CPUS_PER_TASK}
srun /home/sbbm/build/jedi-bundle_intel2021.4.0/bin/saber_quench_error_covariance_toolbox.x __FILENAME__.yaml > __FILENAME__.out

# Process listing
rm -f __FILENAME__.txt
for subr in "nicas_setup_sampling" "nicas_setup_interp" "nicas_setup_convol" "nicas_setup_norm" "nicas_apply_interp_lin" "nicas_apply_interp_com" "nicas_apply_convol_sqrt_lin" "nicas_apply_convol_sqrt_com" "nicas_apply_norm"; do
  grep -si ${subr} __FILENAME__.out >> __FILENAME__.txt
done