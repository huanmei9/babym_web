chmod 777 ./scripts/*.sh
rm -rf ../flv/*
killall -1 srs
python python/post_flv.py &
exit 0