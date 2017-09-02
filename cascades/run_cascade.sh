
## build cascade tree
# python cascade_statistics.py build_cascade data/aminer_citation_dict.json

## gen statistics data of citation number cascade_size depth degree
# python cascade_statistics.py gen_stat data/aminer_citation_cascade.json

## plot fundamental indicators [citation count, cascade size, cascade depth, in and out degree]
# python cascade_statistics.py stat_plot data/aminer_citation_cascade.json

### plot indicators distribution over citation count
python tools/plot_dis_over_count.py heat


