
## build cascade tree
# python cascade_statistics.py build_cascade data/aminer_citation_dict.json

## cascade size distribution
# python cascade_statistics.py cascade_size data/aminer_citation_cascade.json

## Cascade depth distribution
# python cascade_statistics.py cascade_depth data/aminer_citation_cascade.json


## Cascade subgraphs

nohup python cascade_statistics.py subgraphs data/aminer_citation_cascade.json 0 10 > run_0_10.log &

nohup python cascade_statistics.py subgraphs data/aminer_citation_cascade.json 10 100 > run_10_100.log &







