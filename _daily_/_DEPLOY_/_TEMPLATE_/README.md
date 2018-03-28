This folder contains all utilities shared among different `distro deployment` 
`distro` means STAGING, PRODUCTION, etc

#about `load-config.sh` 
This helps to create a distro deployment folder for you
Usage
```bash
./load-config.sh /path/to/distro/folder
```

#about `create-symlink.sh` 
We use symlink to clone utilities to your distro folder - this helps utility code synced/updated from one original source/file 
Usage
```bash
#create link
./create-symlink.sh /path/to/distro/folder 

#rollback created link
./create-symlink.sh /path/to/distro/folder rollback 
```

#sum-up
```bash
cd '/path/to/containing/folder'
DISTRO_DEPLOY='/path/to/distro/folder'
./load-config.sh    "$DISTRO_DEPLOY" 
./create-symlink.sh "$DISTRO_DEPLOY" 
```
