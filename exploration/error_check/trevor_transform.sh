#!/bin/bash

find ./images -type f -name "*.txt" -exec sed -i "s/,/ /g" {} \;

