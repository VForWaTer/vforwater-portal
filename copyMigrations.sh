#!/bin/bash

if [ $1 == "copy" ]
  then
    for i in $(find -type d -name 'migrations')
      do
        #echo $i
        cp -rv $i "$(dirname $i)/migrations_copy"

      done
elif [ $1 == "undoCopy" ]
  then
      for i in $(find -type d -name 'migrations_copy')
        do
          cp -rv "$(dirname $i)/migrations" "$(dirname $i)/migrations_org"
          rm -rf "$(dirname $i)/migrations"
          cp -rv $i "$(dirname $i)/migrations"
          rm -rf "$(dirname $i)/migrations_copy"
          rm -rf "$(dirname $i)/migrations_org"

        done
else
    echo "Error: Parameter '"$1"' is not allowed. Allowed are 'copy' and 'undoCopy'."

fi


