#  Faculty of IT, Monash University
#  FIT2014 Theory of Computation
#  2nd Semester, 2025
#  Assignment 1
#  Your name:  
#  Your Student ID:  

 BEGIN  {

     firstMatch = 1;

 }


 /Write your vertex-line pattern here, and also in prob2.txt/  { 
     #  This action statement spans several lines.
     #  You will need to add code in certain places:
     #  to control some for-loops and to complete some  printf  statements
     #  that print parts of the CNF expression.
     #  Every string  ####  must be replaced by something, not necessarily
     #  of the same length.

     #  Think: why might we want to flag whether we are at the first clause?
     if (firstMatch == 1) {firstMatch = 0} else {printf(####);}

        #  Think: what should we print if a vertex has no incoming edges?
        if (NF == 2)
        {
                printf(####);
        }
        else
        {
                #  this loop ensures the first condition of kernels is met
                printf(####);
                for (####)
                {
                        printf(####);
                }
                printf(####);

                # this loop ensures the second condition of kernels is met
                for (####)
                {
                         printf(####);
                }
        }
  }


 END  {
   printf("\n");
 }
