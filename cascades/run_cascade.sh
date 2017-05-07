
## build cascade tree
# python cascade_statistics.py build_cascade data/aminer_citation_dict.json

## cascade size distribution
# python cascade_statistics.py cascade_size data/aminer_citation_cascade.json

## Cascade depth distribution
# python cascade_statistics.py cascade_depth data/aminer_citation_cascade.json


## Cascade subgraphs
# echo '0,10'
# nohup python cascade_statistics.py subgraphs data/aminer_citation_cascade.json 0 10 > run_0_10.log &
# echo '10,100'
# nohup python cascade_statistics.py subgraphs data/aminer_citation_cascade.json 10 100 > run_10_100.log &


for i in {1..8}
do
    start=`expr ${i} \* 1000`
    end=`expr ${start} + 1000`
    echo ${start}','${end}
    # echo ${i}

    python cascade_statistics.py subgraphs data/aminer_citation_cascade.json ${start} ${end} 1> subs/'${start}'_'${end}'.data' 2>'run_'${start}'_'${end}'.log'

done





