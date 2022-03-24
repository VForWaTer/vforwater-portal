#!/bin/bash

if [ $1 == "copy" ]
  then
    for i in $(find -type d -name 'migrations')
      do
        #echo $i
        cp -rv $i "$(dirname $i)/migrations_copy"

      done
elif [ $1 == "copyPlay" ]
  then
    for i in $(find -type d -name 'migrations')
      do
        #echo $i
        cp -rv $i "$(dirname $i)/migrations_playCopy"

      done
elif [ $1 == "copyDemo" ]
  then
    for i in $(find -type d -name 'migrations')
      do
        #echo $i
        cp -rv $i "$(dirname $i)/migrations_demoCopy"

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
elif [ $1 == "use_demo" ]
  then
      for i in $(find -type d -name 'migrations_demoCopy')
        do
          cp -rv "$(dirname $i)/migrations" "$(dirname $i)/migrations_org"
          rm -rf "$(dirname $i)/migrations"
          cp -rv $i "$(dirname $i)/migrations"
          rm -rf "$(dirname $i)/migrations_org"

        done
elif [ $1 == "use_play" ]
  then
      for i in $(find -type d -name 'migrations_playCopy')
        do
          cp -rv "$(dirname $i)/migrations" "$(dirname $i)/migrations_org"
          rm -rf "$(dirname $i)/migrations"
          cp -rv $i "$(dirname $i)/migrations"
          rm -rf "$(dirname $i)/migrations_org"

        done
elif [ $1 == "switchMigrations" ]
  then
      for i in $(find -type d -name 'migrations_copy')
        do
           echo $i
#          cp -rv "$(dirname $i)/migrations" "$(dirname $i)/migrations_org"
#          rm -rf "$(dirname $i)/migrations"
#          cp -rv $i "$(dirname $i)/migrations"
#          rm -rf "$(dirname $i)/migrations_copy"
#          rm -rf "$(dirname $i)/migrations_org"
#
        done
elif [ $1 == "deleteCopy" ]
  then
      for i in $(find -type d -name 'migrations_copy')
        do
          rm -rf "$(dirname $i)/migrations_copy"

        done
elif [ $1 == "deleteMigrations" ]
  then
      for i in $(find -type d -name 'migrations')
        do
          rm -rf "$(dirname $i)/migrations"

        done
elif [ $1 == "restoreMigrations" ]
  then
      for i in $(find -type d -name 'migrations_copy')
        do
          cp -rv $i "$(dirname $i)/migrations"

        done
else
    echo "Error: Parameter '"$1"' is not allowed. Allowed are 'copy', 'deleteCopy', 'switchMigrations' and 'undoCopy'."

fi


