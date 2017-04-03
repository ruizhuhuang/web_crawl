NODE_LIST=`scontrol show hostnames $SLURM_NODELIST`
NODE_NUM=`echo $NODE_LIST|awk '{FS = " "};{print NF}'`
# remove header
tail -n +2 $1 > websites
nline=`wc -l websites | awk '{print $1}'`
nline_per_task=`echo "($nline/$NODE_NUM + 1)" | bc`

awk -v nline_per_task=$nline_per_task 'NR%nline_per_task==1{x="websites_"++i;}{print > x}'  websites

count=1


#rm -rf /data/projects/G-818523/web_crawl/recursive_crawler/finished.txt /data/projects/G-818523/web_crawl/recursive_crawler/unfinished.txt
echo $1
echo $2
export OUT_DIR=$2

for n in `echo $NODE_LIST`;
do 
    if [ -e websites_${count} ]; then
        while read p; 
        do
	    export SITE=`echo $p | awk 'BEGIN {FS=","};{print $2}'`
	    export NO=`echo $p | awk 'BEGIN {FS=","};{print $3}'`
	    ssh -n $n "cd /data/projects/G-818523/web_crawl/recursive_crawler; echo $SITE;echo $OUT_DIR;echo $NO; export SITE=$SITE;export NO=$NO;export OUT_DIR=$OUT_DIR; nohup /data/projects/G-818523/web_crawl/run_scrapy.sh >& a.out & "
	echo "aaa"
        done < websites_${count} 
    fi
    let count+=1
done



