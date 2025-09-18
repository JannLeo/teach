#include <string>
#include <vector>
#include "sort_demo.h"
using namespace std;

class QuickSort : public Sort{
    public:
    vector<int> sort(vector<int> list) override;
    private:
    static int indexForSegment(int lo, int hi);
    static void quickSortRec(vector<int> & a,int lo,int hi);
    static int partition(vector<int>& a, int lo, int hi);
    static void quickSortIter(vector<int> & a);
};