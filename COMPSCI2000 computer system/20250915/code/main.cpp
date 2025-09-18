#include <iostream>
#include <vector>
#include <sstream>
#include "RecursiveBinarySearch.h"
#include "QuickSort.h"
using namespace std;
int main(){
    string line;
    getline(cin,line);
    vector<int> nums;
    stringstream ss(line);
    int num;
    while(ss >> num){
        nums.push_back(num);
    }
    QuickSort quicksort;
    quicksort.sort(nums);
    RecutsiveBinarySearch binarySearch;
    bool found = binarySearch.search(nums,1);
    cout << (found ? "true" : "false") << endl;
    for(int n:nums){
        cout << " "<<n << endl;
    }
    cout<< endl;
}
