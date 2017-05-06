
for i in {941..1884}
do
    start=`expr ${i} \* 500`
    end=`expr ${start} + 500`
    echo ${start}','${end}
    # echo ${i}

    python cascade_statistics.py subgraphs data/aminer_citation_cascade.json ${start} ${end}

done