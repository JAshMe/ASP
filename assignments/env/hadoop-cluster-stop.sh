#!/bin/bash

# Stop any running instance of Apache Hadoop master node
docker container ls | grep 'hadoop-master' &> /dev/null
if [[ $? == 0 ]]; then
	echo 'Stopping running instance of hadoop-master'
	docker container stop hadoop-master
	# Remove existing container of Apache Spark master node
	echo 'Removing existing instance of spark-master'
	docker container rm hadoop-master
fi

docker container ls | grep 'hadoop-slave1' &> /dev/null
if [[ $? == 0 ]]; then
	echo 'Stopping running instance of hadoop-slave1'
	docker stop hadoop-slave1
	echo 'Removing existing instance of hadoop-slave1'
	docker rm hadoop-slave1
fi

docker container ls | grep 'hadoop-slave2' &> /dev/null
if [[ $? == 0 ]]; then
	echo 'Stopping running instance of hadoop-slave2'
	docker stop hadoop-slave2
	echo 'Removing existing instance of hadoop-slave2'
	docker rm hadoop-slave2
fi

# Remove existing Docker network
docker network ls | grep 'hadoop-net' &> /dev/null
if [[ $? == 0 ]]; then
	echo 'Removing existing hadoop-net Docker network'
	docker network rm hadoop-net
fi