#include "sort_demo.h"
#include <vector>
#include <stack>
#include <algorithm>
#include <iostream>
using namespace std;

struct QuickSort : public Sort{
    vector<int> sort(vector<int> list) override{
        if(list.size() < 2){
            return;
        }
        quickSortRec(list,0,list.size() - 1);
        return list;
    }
    private:
    static int indexForSegment(int lo, int hi){
        int len = hi - lo +1;
        return (len>=3)? lo+2 : lo + len -1;
    }
    static int partition(vector<int>& a, int lo, int hi){
        int pidx = min(indexForSegment(lo,hi), hi);
        int pivot = a[pidx];
        int i = lo - 1 ;
        for(int j = lo; j < hi; j++){
            if(a[j] < pivot){
                i++;
                swap(a[i], a[j]);
            }
        }
        swap(a[i + 1], a[pidx]);
        return i + 1;
    }
    static void quickSortRec(vector<int> & a,int lo,int hi){
        if(lo >= hi) return;
        int pidx = partition(a,lo,hi);
        quickSortRec(a,lo,pidx - 1);
        quickSortRec(a,pidx + 1,hi);
    }
    static void quickSortIter(vector<int> & a){
        stack<pair<int,int>> st;
        st.push({0,(int)a.size() - 1});
        while(!st.empty()){
            auto [lo,hi] = st.top();
            st.pop();
            if(lo >= hi) continue;
            int p = partition(a,lo,hi);
            if(p -1 - lo > hi - p -1){
                st.push({lo,p - 1});
                st.push({p+1,hi});
            }
            else{
                st.push({p+1,hi});
                st.push({lo,p - 1});
            }
        }
    }
};
