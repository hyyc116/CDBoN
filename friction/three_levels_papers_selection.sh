# ## run paper distribution and citation
# python citation_dis_age.py data/aminer_citation_dict.json

# ## after analyzing the paper distribution and citation age of this dataset, we first do the data statistics before 2006

# ## get statistics of citation distribution and plot figures
# python citation_nums.py data/aminer_citation_dict.json 2005


## random select three cited levels papers
# python sampling_three_levels.py data/aminer_citation_dict.json 2005


## plot timely speed / cy_cyi_yi
python Citation_friction.py co_three_levels data/low_selected_papers.json data/medium_selected_papers.json data/high_selected_papers.json cy_delta_cyi_yi all 0 0 700

## plot average speed / cy_cyi_dyi
python Citation_friction.py co_three_levels data/low_selected_papers.json data/medium_selected_papers.json data/high_selected_papers.json cy_cyi_dyi all 0 0 400

## plot average time / cy_yi_dcyi
python Citation_friction.py co_three_levels data/low_selected_papers.json data/medium_selected_papers.json data/high_selected_papers.json cy_yi_dcyi all 1 0.001 100

## plot time required to receive certain citations / co_ti_i
python Citation_friction.py co_three_levels data/low_selected_papers.json data/medium_selected_papers.json data/high_selected_papers.json co_ti_i all 0 0 60
python Citation_friction.py co_three_levels data/low_selected_papers.json data/medium_selected_papers.json data/high_selected_papers.json co_ti_i 10 0 0 60
python Citation_friction.py co_three_levels data/low_selected_papers.json data/medium_selected_papers.json data/high_selected_papers.json co_ti_i 100 0 0 60

# plot time required to receive one more citation / co_delta_ti
python Citation_friction.py co_three_levels data/low_selected_papers.json data/medium_selected_papers.json data/high_selected_papers.json co_delta_ti 10 0 0 40
python Citation_friction.py co_three_levels data/low_selected_papers.json data/medium_selected_papers.json data/high_selected_papers.json co_delta_ti 100 0 0 40
python Citation_friction.py co_three_levels data/low_selected_papers.json data/medium_selected_papers.json data/high_selected_papers.json co_delta_ti all 0 0 40



###### plot co_ti_i
# python Citation_friction.py co_three_levels data/low_selected_papers.json data/medium_selected_papers.json data/high_selected_papers.json co_ti_i all

##### plot co_delta_ti
# python Citation_friction.py co_three_levels data/low_selected_papers.json data/medium_selected_papers.json data/high_selected_papers.json co_delta_ti 10

# python Citation_friction.py co_three_levels data/low_selected_papers.json data/medium_selected_papers.json data/high_selected_papers.json co_delta_ti 100

# python Citation_friction.py co_three_levels data/low_selected_papers.json data/medium_selected_papers.json data/high_selected_papers.json co_delta_ti all


#### plot co_ti_di
# python Citation_friction.py co_three_levels data/low_selected_papers.json data/medium_selected_papers.json data/high_selected_papers.json co_ti_di 10

# python Citation_friction.py co_three_levels data/low_selected_papers.json data/medium_selected_papers.json data/high_selected_papers.json co_ti_di 100

# python Citation_friction.py co_three_levels data/low_selected_papers.json data/medium_selected_papers.json data/high_selected_papers.json co_ti_di all

#### plot cy_cyi_yi accumulative count
# python Citation_friction.py co_three_levels data/low_selected_papers.json data/medium_selected_papers.json data/high_selected_papers.json cy_cyi_yi all

#### plot cy_delta_cyi_yi density count
# python Citation_friction.py co_three_levels data/low_selected_papers.json data/medium_selected_papers.json data/high_selected_papers.json cy_delta_cyi_yi all
### plot cy_cyi_dyi
# python Citation_friction.py co_three_levels data/low_selected_papers.json data/medium_selected_papers.json data/high_selected_papers.json cy_cyi_dyi all

# python Citation_friction.py co_three_levels data/low_selected_papers.json data/medium_selected_papers.json data/high_selected_papers.json cy_yi_dcyi all

# python Citation_friction.py co_three_levels data/low_selected_papers.json data/medium_selected_papers.json data/high_selected_papers.json cy_delta_yi all
# # 
# python Citation_friction.py co_three_levels data/low_selected_papers.json data/medium_selected_papers.json data/high_selected_papers.json cy_delta_cyi_ddelta_yi all
# # 
# python Citation_friction.py co_three_levels data/low_selected_papers.json data/medium_selected_papers.json data/high_selected_papers.json cy_delta_yi_ddelta_cyi all

# python Citation_friction.py scatter_levels data/low_selected_papers.json data/medium_selected_papers.json data/high_selected_papers.json

# python Citation_friction.py citation_ages data/aminer_citation_dict.json

# python Citation_friction.py citation_num data/aminer_citation_dict.json
