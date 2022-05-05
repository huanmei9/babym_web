chmod 777 ./scripts/*.sh
rm -rf ../flv/*
killall -1 srs
python3 python/post_flv.py &
exit 0