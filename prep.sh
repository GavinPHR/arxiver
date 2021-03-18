WORKING_DIR="/workspace/src/indexes"

mkdir $WORKING_DIR
mv $WORKING_DIR/../ttds_data.tar $WORKING_DIR
tar -xvf $WORKING_DIR/ttds_data.tar
rm -rf $WORKING_DIR/ttds_data.tar