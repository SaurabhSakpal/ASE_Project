#!/bin/bash

modelFile="examples/homeautomation.xml"
array=("1 200 20 .50" "2 200 50 .50" "3 200 75 .50" "4 200 100 .50" "5 200 150 .50" "6 200 200 .50" "7 200 100 .20" "8 200 100 .30" "9 200 100 .40" "10 200 100 .50" "11 200 100 .60" "12 200 100 .70" "13 200 100 .80")

for config in "${array[@]}"; do
	python testOptimizers.py $modelFile $config
done