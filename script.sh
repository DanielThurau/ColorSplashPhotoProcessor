#!/bin/bash
export AWS_DEFAULT_REGION=us-west-1
for i in {1..16}
do 
	sam local invoke
done
