#!/bin/bash

export GOROOT=/usr/local/go
export GOPATH=~/go
export PATH=$GOPATH/bin:$GOROOT/bin:$PATH
go get github.com/yudai/gotty
sudo groupadd docker
sudo usermod -aG docker $USER