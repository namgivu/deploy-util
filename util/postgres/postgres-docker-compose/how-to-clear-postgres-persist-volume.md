```bash 
#view the mapped folder of the volume
local-machine $ docker ps #will get container name as $CONTAINER_NAME

#view mapped volume ref. https://stackoverflow.com/a/30133768/248616
docker inspect -f '{{ .Mounts }}' ${CONTAINER_NAME} #will get $VOLUME_PATH `/var/lib/docker/volumes/aa_dbdatavol/_data` - in full: [{volume aa_dbdatavol /var/lib/docker/volumes/aa_dbdatavol/_data /var/lib/postgresql/data local rw true }]

#delete $VOLUME_PATH and must re-create it
sudo rm -rf $VOLUME_PATH
  && sudo mkdir -p $VOLUME_PATH

```