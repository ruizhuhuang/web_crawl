#!/bin/bash

if [ $# -lt "5" ]; then
  echo "This script requires three arguments:"
  echo "  Reservation"
  echo "  time for the job"
  echo "  Allocation"
  echo "  Input csv with header"
  echo "  Output Directory"
  exit -1
fi


export reservation=$1
export t=$2
export allocation=$3
export input_csv=$4
export output_dir=$5


sbatch -J streaming_apps -o job.%j.out -p hadoop --reservation=$reservation -N 10 -n 10 -t $t -A $allocation << ENDINPUT
#!/bin/bash

/bin/bash dist_crawl.sh $input_csv $output_dir 
sleep 48h

ENDINPUT
