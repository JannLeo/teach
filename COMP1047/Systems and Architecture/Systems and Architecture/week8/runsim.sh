#
# Generates results in columns ready to be plotted 
# The first column is lambda (the input rate)
# The second column is the simulation time
# Etc.
#

resfile=res1

rm -i $resfile 

seed= your student id # <<<<<<< CHANGE HERE

for lambda in 5 10 15 20 25 28 30 31 32 33 34 35; do
  ns lab1.tcl $lambda $seed 
  echo -n "Analyzing ... "
  echo -n "$lambda " >> $resfile; awk -f analyze-lab1.awk out.tr >> $resfile 
  echo "End."
  echo "Results summary line for the last simulation:"
  tail -1 $resfile 
  echo " "
done

printf "\n\n\tDone\n"

printf "\n\tThe results are in $resfile\n\n"

