#include <string>
#include <vector>
using namespace std;
class Finder{
    public:
    virtual ~Finder() = default;
    virtual vector<int> findSubstrings(const string & s1,const string & s2) = 0;
};