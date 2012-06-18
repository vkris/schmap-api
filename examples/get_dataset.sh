# filename base, request id as parameters
for ((i=5000;i<=100000;i+=5000));
do
    bash -c "curl -o $1-chunk-$i.json --user username:password 'https://www.schmap.it/api/social_analysis/get_dataset?request_id=$2&cursor=$i'"
done
