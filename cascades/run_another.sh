
for i in {1..9}
do
    start=`expr ${i} \* 100`
    end=`expr ${start} + 100`
    echo ${start}','${end}
    # echo ${i}

    python cascade_statistics.py subgraphs data/aminer_citation_cascade.json ${start} ${end} 1> 'run_'${start}'_'${end}'.log' 2>>'run_'${start}'_'${end}'.log'

done
