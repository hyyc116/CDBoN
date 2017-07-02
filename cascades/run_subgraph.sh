
#subgraph 
for i in {2..15}
do
    echo ${i}
    python cascade_statistics.py gen_sub > subs/subs_${i}.txt
done
