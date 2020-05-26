echo -e "\n------------------------"
echo " >> Stopping containers"
docker stop api
docker stop db1
echo "--------------------------- "

echo "\n >> Removing containers "
docker rm api
docker rm db1
echo  "------------------------"

echo "\n >> Listing containers "
docker ps
echo  "------------------------"
