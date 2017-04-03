#!/bin/bash
cd /data/projects/G-818523/web_crawl/recursive_crawler
echo $SITE;echo $OUT_DIR;echo $NO
nohup scrapy crawl RecursiveSpider -a url=$SITE -a out_dir=$OUT_DIR -a file_name_prefix=$NO &> $NO.out &

# pid=$!

sleep 47h; sleep 10m
ps -ef |grep "scrapy crawl RecursiveSpider -a url=$SITE" |grep -v grep > /dev/null
if [ $? -ne "0" ]; then
  echo $SITE,$NO >> finished_481_1350.txt
else
  echo $SITE,$NO >> unfinished_481_1350.txt
fi
