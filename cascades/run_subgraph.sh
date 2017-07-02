
#subgraph 
for i in {2..20}
do
    echo ${i}
    python cascade_statistics.py gen_sub ${i} 1>'subN/subs_'${i}'.txt' 2>'subN/log_'${i}'.txt' 
done
