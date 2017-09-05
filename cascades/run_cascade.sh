
## build cascade tree
echo 'build cascade'
# python tools/build_cascade.py ../data/aminer_reference.json 

echo 'generate statistics data'
## gen statistics data of citation number cascade_size depth degree
# python tools/gen_stats.py data/aminer_citation_cascade.json

echo 'generate distribution'
## plot fundamental indicators [citation count, cascade size, cascade depth, in and out degree]
# python tools/dis_plot.py

echo 'generate distribution over citation'
### plot indicators distribution over citation count
# python tools/plot_dis_over_count.py
# python tools/plot_dis_over_count.py 1 0 0
# python tools/plot_dis_over_count.py 1 0 1
# python tools/plot_dis_over_count.py 1 1 0
# python tools/plot_dis_over_count.py 1 1 1
# python tools/plot_dis_over_count.py 0 0 0
# python tools/plot_dis_over_count.py 0 0 1
# python tools/plot_dis_over_count.py 0 1 0
# python tools/plot_dis_over_count.py 0 1 1

### plot sub-cascades patterns
python tools/sub_cascade.py data/aminer_citation_cascade.json



