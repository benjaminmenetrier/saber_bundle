#!/bin/bash
#SBATCH --job-name=timing_32_20_4_c0_regular
#SBATCH --output=/home/sbbm/jedi-run/timing_32_20_4_c0_regular/timing_32_20_4_c0_regular-%J.out
#SBATCH --error=/home/sbbm/jedi-run/timing_32_20_4_c0_regular/timing_32_20_4_c0_regular-%J.out
#SBATCH --qos=np
#SBATCH --time=01:00:00
#SBATCH --account=nores
#SBATCH --nodes=1
#SBATCH --ntasks=32
#SBATCH --cpus-per-task=1

# Go to the directory
cd /home/sbbm/jedi-run/timing_32_20_4_c0_regular

# Run executable
export OMP_NUM_THREADS=${SLURM_CPUS_PER_TASK}
srun /home/sbbm/build/jedi-bundle_intel2021.4.0/bin/saber_quench_error_covariance_toolbox.x timing_32_20_4_c0_regular.yaml > timing_32_20_4_c0_regular.out

# Process listing
rm -f timing_32_20_4_c0_regular.txt
for subr in "nicas_setup_sampling" "nicas_setup_interp" "nicas_setup_convol" "nicas_setup_norm" "nicas_apply_interp_lin" "nicas_apply_interp_com" "nicas_apply_convol_sqrt_lin" "nicas_apply_convol_sqrt_com" "nicas_apply_norm"; do
  grep -si ${subr} timing_32_20_4_c0_regular.out >> timing_32_20_4_c0_regular.txt
done