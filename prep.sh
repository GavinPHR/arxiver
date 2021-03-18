DATA_DIR="/workspace/src/data"

mkdir $DATA_DIR
mv $DATA_DIR/../../ttds_data.tar $DATA_DIR
tar -xvf $DATA_DIR/ttds_data.tar
rm -rf $DATA_DIR/ttds_data.tar
