#include "RecursiveBinarySearch.h"

bool RecutsiveBinarySearch::search(const vector<int> & a, int target){
    return search(a,target,0,a.size() - 1) != -1;
}

int RecutsiveBinarySearch::search(const vector<int> & a, int x, int lo, int hi){
    if(lo > hi) return -1;
    int mid = lo + (hi - lo) / 2;
    if(a[mid] == x) return mid;
    if(a[mid] > x) return search(a,x,lo,mid - 1);
    return search(a,x,mid + 1,hi);
}
