#!/bin/bash

# Run
testdir=/home/sbbm/jedi-run
cd ${testdir}

# Parameters
N=600

# Resol/ratio
for NTASK in "32"; do
  for RATIO in "10" "20" "30" "40"; do
    for RESOL in "4" "6" "8" "10"; do
      for INTERP in "c0"; do
        for GRID_TYPE in "regular"; do
          if test ${RATIO} -gt ${RESOL}; then
            # File name
            filename=timing_${NTASK}_${RATIO}_${RESOL}_${INTERP}_${GRID_TYPE}

            # Test sub-directory
            testsubdir=${testdir}/${filename}
            mkdir -p ${testsubdir}

            # Compute RH
            RH=`echo 'import math;n=4*'${N}'+16;gamma=2.0*math.pi*6371229/n;rh='${RATIO}'*gamma;print(rh)' | python`

            # Compute universe length-scale
            ULS=`echo 'print('${RH}'*1.5)' | python`

            # Update template yaml
            sed -e s/__N__/${N}/g -e s/__ULS__/${ULS}/g -e s/__RH__/${RH}/g -e s/__GRID_TYPE__/${GRID_TYPE}/g -e s/__RESOL__/${RESOL}/g -e s/__INTERP__/${INTERP}/g timing_template.yaml > ${testsubdir}/${filename}.yaml

            # Update template script
            sed -e s:__TESTSUBDIR__:${testsubdir}:g -e s/__FILENAME__/${filename}/g -e s/__NTASK__/${NTASK}/g timing_template.sh > ${testsubdir}/${filename}.sh

            # Launch script
            sbatch ${testsubdir}/${filename}.sh
          fi
        done
      done
    done
  done
done

# Scaling
for RATIO in "20"; do
  for RESOL in "8"; do
    for NTASK in "16" "32" "64" "128"; do
      for INTERP in "c0"; do
        for GRID_TYPE in "regular"; do
          if test ${RATIO} -gt ${RESOL}; then
            # File name
            filename=timing_${NTASK}_${RATIO}_${RESOL}_${INTERP}_${GRID_TYPE}

            # Test sub-directory
            testsubdir=${testdir}/${filename}
            mkdir -p ${testsubdir}

            # Compute RH
            RH=`echo 'import math;n=4*'${N}'+16;gamma=2.0*math.pi*6371229/n;rh='${RATIO}'*gamma;print(rh)' | python`

            # Compute universe length-scale
            ULS=`echo 'print('${RH}'*1.5)' | python`

            # Update template yaml
            sed -e s/__N__/${N}/g -e s/__ULS__/${ULS}/g -e s/__RH__/${RH}/g -e s/__GRID_TYPE__/${GRID_TYPE}/g -e s/__RESOL__/${RESOL}/g -e s/__INTERP__/${INTERP}/g timing_template.yaml > ${testsubdir}/${filename}.yaml

            # Update template script
            sed -e s:__TESTSUBDIR__:${testsubdir}:g -e s/__FILENAME__/${filename}/g -e s/__NTASK__/${NTASK}/g timing_template.sh > ${testsubdir}/${filename}.sh

            # Launch script
            sbatch ${testsubdir}/${filename}.sh
          fi
        done
      done
    done
  done
done

# Interpolation type
for RATIO in "20"; do
  for RESOL in "8"; do
    for NTASK in "32"; do 
      for INTERP in "c1" "si"; do
        for GRID_TYPE in "regular"; do
          if test ${RATIO} -gt ${RESOL}; then
            # File name
            filename=timing_${NTASK}_${RATIO}_${RESOL}_${INTERP}_${GRID_TYPE}

            # Test sub-directory
            testsubdir=${testdir}/${filename}
            mkdir -p ${testsubdir}

            # Compute RH
            RH=`echo 'import math;n=4*'${N}'+16;gamma=2.0*math.pi*6371229/n;rh='${RATIO}'*gamma;print(rh)' | python`

            # Compute universe length-scale
            ULS=`echo 'print('${RH}'*1.5)' | python`

            # Update template yaml
            sed -e s/__N__/${N}/g -e s/__ULS__/${ULS}/g -e s/__RH__/${RH}/g -e s/__GRID_TYPE__/${GRID_TYPE}/g -e s/__RESOL__/${RESOL}/g -e s/__INTERP__/${INTERP}/g timing_template.yaml > ${testsubdir}/${filename}.yaml

            # Update template script
            sed -e s:__TESTSUBDIR__:${testsubdir}:g -e s/__FILENAME__/${filename}/g -e s/__NTASK__/${NTASK}/g timing_template.sh > ${testsubdir}/${filename}.sh

            # Launch script
            sbatch ${testsubdir}/${filename}.sh
          fi
        done
      done
    done
  done
done