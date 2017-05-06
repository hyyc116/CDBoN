
for i in {281..470}
do
    start=`expr ${i} \* 2000`
    end=`expr ${start} + 2000`
    echo ${start}','${end}
    # echo ${i}

    # python cascade_statistics.py subgraphs data/aminer_citation_cascade.json ${start} ${end}

done