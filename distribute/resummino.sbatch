#!/bin/bash

#SBATCH --job-name=array
#SBATCH --time=1-00:00:00
#SBATCH --partition=normal,p0klasen
#SBATCH --ntasks=1
#SBATCH --mem=1G
#SBATCH -a 1-2000%2000
#SBATCH --mail-type=ALL
#SBATCH --mail-user=a_neuw01@uni-muenster.de 


# 29610
# 4935
dire="./output_**"
arr=2000
jobc=$(find . -wholename "$dire/*.sh" | wc -l)
jj=$(($jobc/$arr+1))
n=$((${SLURM_ARRAY_TASK_ID}))

while [ $n -le $jobc ]
do
    file=$(find . -wholename "$dire/*.sh" | sed -n ${n}p)
    #echo $file
    bash $file
    n=$(($n+arr))
done
