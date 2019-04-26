#!/bin/bash

# Create a Docker network for communication between Docker containers for Apache Spark
docker network ls | grep 'spark-net' &> /dev/null
if [[ $? == 0 ]]; then
	echo 'Docker network already exists. Skipping network creation.'
else
	echo 'Creating new Docker network: spark-net'
	docker network create spark-net
fi

# Pull the latest image of Apache Spark master node from DockerHub
echo 'Pulling uselesscoder/alpine-spark-master:latest'
docker pull uselesscoder/alpine-spark-master:latest

# Running container image for Apache Spark master node
docker container ls | grep 'spark-master' &> /dev/null
if [[ $? == 0 ]]; then
	echo 'An instance of uselesscoder/alpine-spark-master as spark-master is already running. Skipping run.'
else
	echo 'Running new instance of uselesscoder/alpine-spark-master as spark-master'
	docker run --name spark-master -h spark-master --network spark-net -d uselesscoder/alpine-spark-master:latest
fi

# Pull the latest image of Apache Spark worker from DockerHub
echo 'Pulling uselesscoder/alpine-spark-worker:latest'
docker pull uselesscoder/alpine-spark-worker:latest

docker container ls | grep 'spark-worker-1' &> /dev/null
if [[ $? == 0 ]]; then
	echo 'An instance of uselesscoder/alpine-spark-worker as spark-worker-1 is already running. Skipping run.'
else
	echo 'Running new instance of uselesscoder/alpine-spark-worker:latest as spark-worker-1'
	docker run --name spark-worker-1 -h spark-worker-1 --network spark-net -d uselesscoder/alpine-spark-worker:latest
fi

docker container ls | grep 'spark-worker-2' &> /dev/null
if [[ $? == 0 ]]; then
	echo 'An instance of uselesscoder/alpine-spark-worker as spark-worker-2 is already running. Skipping run.'
else
	echo 'Running new instance of uselesscoder/alpine-spark-worker:latest as spark-worker-2'
	docker run --name spark-worker-2 -h spark-worker-2 --network spark-net -d uselesscoder/alpine-spark-worker:latest
fi

# Parsing passed command line arguments
POSITIONAL=()
while [[ $# -gt 0 ]]
do
	key="$1"
	case $key in
		-l | --link)
			LINK="$2"
			shift
			shift
			;;
		-c | --command)
			COMMAND="$2"
			shift
			shift
			;;
		*)
			POSITIONAL+=("$1")
			shift
			;;
	esac
done

# Restore positional arguments
set -- "${POSITIONAL[@]}"

# Fetch source code files
if [[ $LINK != '' ]]; then
	echo 'Downloading source code files'
	wget $LINK -O code.zip

	# Extract source code files
	echo 'Extracting source code files'
	unzip code.zip -d code

	# Copy the source code to Spark Master container
	echo 'Copying source code files to spark-master container'
	docker cp code spark-master:/code

	# Removing the local copy of source code files
	echo 'Removing the local copy of source code files'
	rm -rf code
fi

# Run the source code submitted by the user
if [[ $COMMAND != '' ]]; then
	docker exec spark-master bash -c "$COMMAND"
fi

docker exec -it spark-master bash