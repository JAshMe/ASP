#!/bin/bash

cd assignments
# Parsing passed command line arguments
POSITIONAL=()
while [[ $# -gt 0 ]]
do
	key="$1"
	case $key in
		-e | --environment)
			ENVIRONMENT="$2"
			shift
			shift
			;;
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
		-u | --user-name)
			USERNAME="$2"
			shift
			shift
			;;
		*)
			POSITIONAL+=("$1")
			shift
			;;
	esac
done

if [[ $USERNAME != '' ]]; then
	mkdir -p vm_data/$USERNAME
	cd vm_data/$USERNAME
else
	exit
fi

vagrant status | grep 'running (virtualbox)' &> /dev/null
if [ $? == 0 ]; then
	if [[ $ENVIRONMENT == 'ap_sp' ]]; then
		SPARK_CLUSTER_COMMAND='~/spark-cluster-start.sh -l '$LINK' -c '"\"$COMMAND\""
		echo $SPARK_CLUSTER_COMMAND
		FINAL_COMMAND='~/go/bin/gotty -w -p 8080 '$SPARK_CLUSTER_COMMAND
		vagrant ssh -c "$FINAL_COMMAND" &
	fi
	if [[ $ENVIRONMENT == 'ap_hp' ]]; then
		HADOOP_CLUSTER_COMMAND='~/hadoop-cluster-start.sh -l '$LINK' -c '"\"$COMMAND\""
		echo $HADOOP_CLUSTER_COMMAND
		FINAL_COMMAND='~/go/bin/gotty -w -p 8080 '$HADOOP_CLUSTER_COMMAND
		vagrant ssh -c "$FINAL_COMMAND" &
	fi
else
	echo 'VM instance for this user is not running. Please run start-vm.sh script before starting deployment.' 
	exit
fi