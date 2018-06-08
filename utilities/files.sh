#!bin/bash
## v1.2
##
## This script finds all file extensions in the current dir and all subdirs
## and lists them by extension. Also gives a count list of those extensions
## This script only executes, if filecount has changed, so no unnecessary 
## rewrites occur. This script was initially written for a server cronjob.
## Script created and owned by Richard Rudolph
##

cd ..

outfile="utilities/files.txt" 

listfiles() {

printf "##########################\n" > $outfile
printf "### All files sorted   ###\n" >> $outfile
printf "### by extension in    ###\n" >> $outfile
printf "### alphabetical order ###\n" >> $outfile
printf "##########################\n" >> $outfile
printf "\n" >> $outfile

printf "Total file count: $totalcount\n\n" >> $outfile

extensions=(`find . -type f -name "*.*" | sed "s|.*\.||" | sort -u`)

printf "There are ${#extensions[@]} extensions\n\n" >> $outfile
printf "%10s %15s %10s\n" "No" "Type" "Lines"  >> $outfile

for i in "${extensions[@]}"
do
	lines=`find . -type f -name "*.$i" | xargs wc -l | grep 'total' | awk '{ SUM += $1; print $1}'`
	count=`find . -type f -name "*.$i" | wc -l`
	printf "%10s %15s %10s\n" $count $i $lines  >> $outfile;
done

printf "\n" >> $outfile

for i in "${extensions[@]}"
do
	printf "### $i files ###\n" >> $outfile
	printf "\n" >> $outfile
	find . -type f -name "*.$i" >> $outfile
	printf "\n" >> $outfile
done
}


## Control if file number has changed. If not, no rewrite of file necessary
totalcount=`find . -type f | wc -l`
lastcount=`sed -n '7{s/Total file count: // ; p}' 'utilities/files.txt'`

if [ $totalcount != $lastcount ]
	then
		listfiles
fi	
	
