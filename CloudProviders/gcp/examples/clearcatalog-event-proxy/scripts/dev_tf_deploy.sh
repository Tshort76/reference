#!/bin/bash

cd ..

mkdir -p dist
timestamp=$(date +%s)
zip_obj="clearcatalog_event_proxy_src_$timestamp.zip"
zip_path="dist/$zip_obj"

# Zip the source code
zip -r $zip_path ./src

zipped_src="`pwd`/$zip_path"

echo "zipped source $zipped_src"

cd terraform/environments/datacatalog-irc-glb-dev

if [ $# -eq 0 ]
then
    echo "Running terraform PLAN.  Pass any argument to the script to apply changes"
    terraform plan -var "local_source_path=$zipped_src"
else
    echo "Running terraform APPLY"
    terraform apply -var "local_source_path=$zipped_src"
fi
