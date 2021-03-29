DATA_DIR="/workspace/src/data"

mkdir $DATA_DIR
mv $DATA_DIR/../ttds_data.tar $DATA_DIR
tar -xf $DATA_DIR/ttds_data.tar -C $DATA_DIR
rm -rf $DATA_DIR/ttds_data.tar
rm $DATA_DIR/vocabulary.pbz2
