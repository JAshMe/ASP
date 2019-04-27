#!/bin/bash

# Create a Docker network for communication between Docker containers for Apache Hadoop
docker network ls | grep 'hadoop-net' &> /dev/null
if [[ $? == 0 ]]; then
	echo 'Docker network already exists. Skipping network creation.'
else
	echo 'Creating new Docker network: hadoop-net'
	docker network create hadoop-net
fi

# Pull the latest image of Apache Hadoop from DockerHub
echo 'Pulling uselesscoder/apache-hadoop:latest'
docker pull uselesscoder/apache-hadoop:latest

# Running container image for Apache Hadoop master node
docker container ls | grep 'hadoop-master' &> /dev/null
if [[ $? == 0 ]]; then
	echo 'An instance of uselesscoder/apache-hadoop as hadoop-master is already running. Skipping run.'
else
	echo 'Running new instance of uselesscoder/apache-hadoop as hadoop-master'
	docker run -itd --network hadoop-net -p 50070:50070 -p 8088:8088 --name hadoop-master -h hadoop-master uselesscoder/apache-hadoop:latest
fi

docker container ls | grep 'hadoop-slave1' &> /dev/null
if [[ $? == 0 ]]; then
	echo 'An instance of uselesscoder/apache-hadoop as hadoop-slave1 is already running. Skipping run.'
else
	echo 'Running new instance of uselesscoder/apache-hadoop as hadoop-slave1'
	docker run -itd --network hadoop-net --name hadoop-slave1 -h hadoop-slave1 uselesscoder/apache-hadoop:latest
fi

docker container ls | grep 'hadoop-slave2' &> /dev/null
if [[ $? == 0 ]]; then
	echo 'An instance of uselesscoder/apache-hadoop as hadoop-slave2 is already running. Skipping run.'
else
	echo 'Running new instance of uselesscoder/apache-hadoop as hadoop-slave2'
	docker run -itd --network hadoop-net --name hadoop-slave2 -h hadoop-slave2 uselesscoder/apache-hadoop:latest
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
	echo 'Copying source code files to hadoop-master container'
	docker cp code hadoop-master:/code

	# Removing the local copy of source code files
	echo 'Removing the local copy of source code files'
	rm -rf code
fi

docker exec hadoop-master bash -c "~/start-hadoop.sh"

# Run the source code submitted by the user
if [[ $COMMAND != '' ]]; then
	docker exec hadoop-master bash -c "$COMMAND"
fi

docker exec -it hadoop-master bash