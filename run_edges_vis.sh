#filter out edge of which weight is 1
echo 'filter out degrees with 1'
python preprocessing.py filtered $1 $2 > $1_filtered.txt

# generate unweighted network base on the reuqirement of largevis
echo 'transform two directed graph'
python preprocessing.py  undirected $1_filtered.txt > $1_twodirected.txt

# run largevis
echo "run largevis"
python LargeVis_run.py -input $1_twodirected.txt -output ${1}_graph.txt -threads 8 -fea 0

# preprocess
echo 'transform'
python preprocessing.py tg ${1}_graph.txt 1>${1}_graph_2D.txt 2>${1}_graph_index.txt

# clustering data base on 2D result
echo "run clustering base on 2D result "
python preprocessing.py clustering ${1}_graph_2D.txt 1>${1}_graph_labels.txt  

# from index to author name and paper count
echo 'get author name and their paper count'
python preprocessing.py ac ${1}_graph_index.txt > ${1}_graph_sorted_words.txt

# run visulization
echo "plot 2D graph"
python plot.py -input ${1}_graph_2D.txt -label ${1}_graph_labels.txt -output ${1}_graph_2D_plot.pdf -index ${1}_graph_index.txt -words ${1}_graph_sorted_words.txt -size 10