#include <vector>
#include <iostream>
using namespace std;

void buildModFibTail(int target,int num,long long prev2,long long prev1,vector<int> &out){
    if(num >= target) return;
    long long next = prev1*prev2;
    out.push_back(next);

    buildModFibTail(target,num+1,prev1,next,out);
    
}



vector<int> modifiedFibonacci(int n){
    vector<int> res;
    if (n <= 0) {
        return res;
    }
    res.reserve(n);
    res.push_back(2);
    if(n==1) return res;
    res.push_back(3);
    if(n==2) return res;
    buildModFibTail(n,2,2,3,res);
    return res;
}
int main(){
    auto v = modifiedFibonacci(10);
    for(auto i:v){
        cout << i << endl;
    }
}