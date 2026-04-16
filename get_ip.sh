#!/bin/bash


ens160ip=$(ip a | grep -i brd | awk -F" " '{print $2}' | sed 's/\/24//g' | tail -1)

echo $ens160ip
