# filename base, request id as parameters

# The first request wiht no cursor argument
bash -c "curl -o toyota-followers-chunk-0.json --user gensent:eb6j89kpbrtryy 'https://www.schmap.it/api/social_analysis/get_dataset?request_id=527'"
for ((i=5000;i<=100000;i+=5000));
do
    bash -c "curl -o $1-chunk-$i.json --$3:$4 'https://www.schmap.it/api/social_analysis/get_dataset?request_id=$2&cursor=$i'"
done
