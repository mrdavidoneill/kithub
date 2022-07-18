# DB backup

## To backup

```bash
docker-compose stop db
docker run --rm --volumes-from tm470_db_1 -v ~/backup:/backup ubuntu bash -c "cd /var/lib/mysql && tar cvf /backup/kithub.tar ."
```

## To restore

```bash
docker volume create db_data_20220407_1630
docker run --rm -v db_data_20220407_1630:/recover -v ~/backup:/backup ubuntu bash -c "cd /recover && tar xvf /backup/kithub.tar"

# Change docker-compose volume to db_data_20220407_1630 and external: true
docker-compose start db

```

# Deploying on Raspberry Pi 3B+

Install Docker
Install Docker-compose

```bash
python3 install --upgrade pip
pip3 install docker-compose
```

At this point, docker compose won't work

```bash
sudo mkdir /etc/prelink.conf.d
sudo echo -b /home/ubuntu/.local/bin/docker-compose > /etc/prelink.conf.d/dockercomposefix
```

# Use local registry

## Use HTTP

# if /etc/docker/daemon.json doesn't exist

```bash
sudo touch /etc/docker/daemon.json
sudo nano /etc/docker/daemon.json
```

Edit file to include insecure registry

```json
{
  "insecure-registries": ["192.168.2.65:5000"]
}
```
