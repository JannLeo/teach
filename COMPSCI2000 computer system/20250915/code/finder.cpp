#include "finder.h"
using namespace std;

vector<int> prefix_function(const vector<int>& p ){
    int m = p.size();
    vector<int> pi(m,0);
    for(int i=1;i < m ; i++){
        int j = pi[i - 1];
        while(j > 0 && p[i] != p[j]){
            j = pi[j - 1];
        }
        if(p[i] == p[j]){
            j++;
        }
        pi[i] = j;
    }
}
