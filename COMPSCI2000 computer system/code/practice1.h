#ifndef PRACTICE1_H
#define PRACTICE1_H
#include <stdio.h>
#include <stdlib.h>
#include <string>
#include <vector>
using namespace std;
class PotionCraft{
    public:
    
    vector<string> getPotions() const;

    void brewPotion(string &name);

    string consumePotion(string name);

    void brewMultiplePotions(vector<string> &potions);

    vector<string> fillExternalContainer(vector<string>& container);

    private:
    vector<string> inventory_;
};


#endif