#!/bin/bash

# Stop any running instance of Apache Spark master node
docker container ls | grep 'spark-master' &> /dev/null
if [[ $? == 0 ]]; then
	echo 'Stopping running instance of spark-master'
	docker container stop spark-master
	# Remove existing container of Apache Spark master node
	echo 'Removing existing instance of spark-master'
	docker container rm spark-master
fi

docker container ls | grep 'spark-worker-1' &> /dev/null
if [[ $? == 0 ]]; then
	echo 'Stopping running instance of spark-worker-1'
	docker stop spark-worker-1
	echo 'Removing existing instance of spark-worker-1'
	docker rm spark-worker-1
fi

docker container ls | grep 'spark-worker-2' &> /dev/null
if [[ $? == 0 ]]; then
	echo 'Stopping running instance of spark-worker-2'
	docker stop spark-worker-2
	echo 'Removing existing instance of spark-worker-2'
	docker rm spark-worker-2
fi

# Remove existing Docker network
docker network ls | grep 'spark-net' &> /dev/null
if [[ $? == 0 ]]; then
	echo 'Removing existing spark-net Docker network'
	docker network rm spark-net
fi