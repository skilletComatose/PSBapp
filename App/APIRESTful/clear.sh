echo -e "\n------------------------"
echo " >> Stopping containers"
docker stop api
docker stop db1
echo "--------------------------- "

echo "\n >> Removing api container "
docker rm api
echo  "------------------------"

echo "\n >> Listing containers "
docker ps
echo  "------------------------"
