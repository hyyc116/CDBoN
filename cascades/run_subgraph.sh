
#subgraph 
for i in {2..15}
do
    echo ${i}
    python cascade_statistics.py gen_sub ${i}> 'subN/subs_${i}.txt'
done
