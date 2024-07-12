run_rsync() {
  echo started syncing to node "$1"
  srun -p csedu -w "$1" --qos csedu-small --account cseduproject mkdir -p /scratch/"$USER/thesis-forecasting/data/preprocessed/rtcor_heavy_rain_labels/"
  srun -p csedu -w "$1" --qos csedu-small --account cseduproject rsync cn84:/scratch/"$USER"/thesis-forecasting/data/preprocessed/rtcor_heavy_rain_labels/ /scratch/"$USER"/thesis-forecasting/data/preprocessed/rtcor_heavy_rain_labels/ -ah --delete
  echo completed syncing to node "$1"
}

if [[ "$HOSTNAME" != "cn84"* ]]; then
  echo run this script from cn84
  exit
fi

# gpu nodes
run_rsync cn47
run_rsync cn48

# cpu nodes
run_rsync cn77
run_rsync cn78
