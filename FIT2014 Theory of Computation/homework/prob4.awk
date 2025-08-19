#  Faculty of IT, Monash University
#  FIT2014 Theory of Computation
#  2nd Semester, 2025
#  Assignment 1
#  Your name:  Haoxuan Zhang
#  Your Student ID:  34550720

 BEGIN  {

     firstMatch = 1;
     printf("sage -c 'print(propcalc.formula(\"");

 }


 /^[[:space:]]*([1-9][0-9]*([[:space:]]+[1-9][0-9]*)*)?[[:space:]]+:[[:space:]]+[1-9][0-9]*[[:space:]]*$/  { 
     #  This action statement spans several lines.
     #  You will need to add code in certain places:
     #  to control some for-loops and to complete some  printf  statements
     #  that print parts of the CNF expression.
     #  Every string  ####  must be replaced by something, not necessarily
     #  of the same length.

     #  Think: why might we want to flag whether we are at the first clause?
     if (firstMatch == 1) {firstMatch = 0} else {printf(" & ");}

        #  Think: what should we print if a vertex has no incoming edges?
        if (NF == 2)
        {
                printf("(v%d)", $2);
        }
        else
        {
                #  this loop ensures the first condition of kernels is met
                printf("(v%d", $NF);
                for (i = 1 ; i <= NF-2 ; i++)
                {
                        printf(" | v%d", $i);
                }
                printf(")");

                # this loop ensures the second condition of kernels is met
                for (i = 1 ; i <= NF-2 ; i++)
                {
                         printf(" & (~v%d | ~v%d)", $i, $NF);
                }
        }
  }


 END  {
   printf("\").is_satisfiable())'\n");
 }
