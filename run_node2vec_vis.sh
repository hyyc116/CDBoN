#filter out edge of which weight is 1
echo 'filter out degree with 1'
python preprocessing.py filtered $1 $2 > $1_filtered.txt

#train node2vec
echo 'training node2vec'
python ../node2vec/src/main.py --input $1_filtered.txt --output $1_emd.txt --weighted

# preprocess
echo 'transform emb to index and embedding file'
python preprocessing.py transform $1_emd.txt 1>${1}.emb 2>${1}_index.txt

# run largevis
echo "run largevis"
python LargeVis_run.py -input ${1}.emb -output ${1}_2D.txt -threads 8

# clustering data base on 2D result
echo "run clustering base on 2D result "
python preprocessing.py clustering ${1}_2D.txt 1>${1}_labels.txt  

# from index to author name and paper count
echo 'get author name and their paper count'
python preprocessing.py ac ${1}_index.txt > $1_sorted_words.txt

# run visulization
# -size $1 
echo "plot 2D graph"
python plot.py -input ${1}_2D.txt -label ${1}_labels.txt -output ${1}_plot.pdf -index ${1}_index.txt -words ${1}_sorted_words.txt

echo 'DONE'