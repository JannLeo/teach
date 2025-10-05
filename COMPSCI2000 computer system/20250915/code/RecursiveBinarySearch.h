
#include <vector>
using namespace std;

class RecutsiveBinarySearch {
    public:
    bool search(const vector<int> & a, int target);
    private:
    int search (const vector<int> & a, int x, int lo,int hi);
};
