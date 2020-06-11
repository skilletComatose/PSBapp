echo -e "\n------------------------"
echo " >> Stopping api container"
docker stop api
echo "--------------------------- "

echo "\n >> Removing api container "
docker rm api
echo  "------------------------"

echo "\n >> Listing containers "
docker ps
echo  "------------------------"
