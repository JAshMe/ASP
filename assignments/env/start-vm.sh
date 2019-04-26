#!/bin/bash

# Please make sure that you run this file while the current working Dir is assignments/vm_data

# Parsing passed command line arguments

cd assignments

POSITIONAL=()
while [[ $# -gt 0 ]]
do
	key="$1"
	case $key in
		-u | --user-name)
			USERNAME="$2"
			shift
			shift
			;;
		-p | --port)
			PORT="$2"
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

if [[ $USERNAME != '' ]]; then
	mkdir -p vm_data/$USERNAME
	cd vm_data/$USERNAME
else
	exit
fi

vagrant status | grep 'running (virtualbox)' &> /dev/null
if [ $? == 0 ]; then
	echo 'VM instance for this user is already running..'
	exit
fi

vagrant status | grep 'saved (virtualbox)' &> /dev/null
if [[ $? == 0 ]]; then
	vagrant up
	exit
fi

cp ../../env/Vagrantfile .

sed -i '1i VM_NAME = "'$USERNAME'"' Vagrantfile
sed -i '2i VM_SHELL_PORT = '$PORT Vagrantfile

vagrant up