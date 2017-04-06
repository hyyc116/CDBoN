# generate unweighted network base on the reuqirement of largevis
python preprocessing.py  undirected ../data/weighted_network_filtered.txt > undirected_filtered.txt

# run largevis
echo "run largevis"
python LargeVis_run.py -input undirected_filtered.txt -output ai_net_2D_result_filtered.txt -threads 8 -fea 0

# preprocess
python preprocessing.py transform ai_net_2D_result_filtered.txt 1>ai_undi_2D_f.txt 2>ai_undi_index_f.txt

# clustering data base on 2D result
echo "run clustering base on 2D result "
python preprocessing.py clustering ai_undi_2D_f.txt 1>ai_undi_labels_f.txt  

# run visulization
echo "plot 2D graph"
python plot.py -input ai_undi_2D_f.txt -label ai_undi_labels_f.txt -output ai_undi_2D_plot_f -size $1 -index ai_undi_index_f.txt -words sorted_words.txt