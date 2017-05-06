
## build cascade tree
# python cascade_statistics.py build_cascade data/aminer_citation_dict.json

## cascade size distribution
# python cascade_statistics.py cascade_size data/aminer_citation_cascade.json

## Cascade depth distribution
# python cascade_statistics.py cascade_depth data/aminer_citation_cascade.json


## Cascade subgraphs
for i in {1..910}
do
    # start=`expr ${i}\*${1}`
    # end=$[i*1000]
    # echo ${start}','${end}
    ${i}

    # python cascade_statistics.py subgraphs data/aminer_citation_cascade.json $start $end

    # start=$[i*1000]
    # end=$[i*2000]
    # echo ${start}','${end}
    # python cascade_statistics.py subgraphs data/aminer_citation_cascade.json $start $end

done





