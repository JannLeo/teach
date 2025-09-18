#include <vector>
using namespace std;

class Sort{
   public:
   virtual ~Sort() = default;
   virtual vector<int> sort(vector<int> list) = 0;
};

class BubbleSort : public Sort{
   public:
   virtual ~BubbleSort() = default;
    vector<int> sort(vector<int> list) override;
};
