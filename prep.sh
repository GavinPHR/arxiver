WORKING_DIR="/home/apps/data"
WGET='wget --load-cookies /tmp/cookies.txt "https://docs.google.com/uc?export=download&confirm=$(wget --quiet --save-cookies /tmp/cookies.txt --keep-session-cookies --no-check-certificate 'https://docs.google.com/uc?export=download&id=1WvnlhwG5GZijQBOcXRighzMOIOHQE5wQ' -O- | sed -rn 's/.*confirm=([0-9A-Za-z_]+).*/\1\n/p')&id=1WvnlhwG5GZijQBOcXRighzMOIOHQE5wQ" -O ttds_data.tar && rm -rf /tmp/cookies.txt'

mkdir $WORKING_DIR
cd $WORKING_DIR
`WGET`
tar -xvf $WORKING_DIR/ttds_data.tar
rm -rf $WORKING_DIR/ttds_data.tar