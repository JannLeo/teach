#include <iostream>
#include "sort_demo.h"


struct BubbleSort : public Sort{
    vector<int> sort(vector<int> list) override{
        for(int i = 0; i < list.size(); i++){
            for(int j = 0; j < list.size() - (i + 1); j++){
                if(list[j] > list[j + 1]){
                    int temp = list[j];
                    list[j] = list[j + 1];
                    list[j + 1] = temp;
                }
            }
        }
        return list;
    }
};
