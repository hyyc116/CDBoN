
for i in {471..950}
do
    start=`expr ${i} \* 1000`
    end=`expr ${start} + 1000`
    echo ${start}','${end}
    # echo ${i}

    python cascade_statistics.py subgraphs data/aminer_citation_cascade.json ${start} ${end}

done