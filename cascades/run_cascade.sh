
## build cascade tree
# python cascade_statistics.py build_cascade data/aminer_citation_dict.json

## cascade size distribution
# python cascade_statistics.py cascade_size data/aminer_citation_cascade.json

## Cascade depth distribution
# python cascade_statistics.py cascade_depth data/aminer_citation_cascade.json


## Cascade subgraphs
for i in {1..460}
do
    start=$[i*0]
    end=$[i*1000]
    echo '$start , $end'
    # python cascade_statistics.py subgraphs data/aminer_citation_cascade.json $start $end

    start=$[i*1000]
    end=$[i*2000]
    echo '$start , $end'
    # python cascade_statistics.py subgraphs data/aminer_citation_cascade.json $start $end

done





