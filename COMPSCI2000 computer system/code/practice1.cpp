#include "practice1.h"
#include "algorithm"
using namespace std;

 vector<string> PotionCraft::getPotions() const{
    return inventory_;
 }

 void PotionCraft::brewPotion(string &name){
    inventory_.push_back(name);
 }

 string PotionCraft::consumePotion(string &name){
    auto it = find(inventory_.begin(), inventory_.end(), name);
    if (it != inventory_.end()) {
        inventory_.erase(it);
        return name;
    }
    return "";
 }
 void PotionCraft::brewMultiplePotions(vector<string> &potions){
    inventory_.insert(inventory_.end(), potions.begin(), potions.end());
 }

 vector<string> PotionCraft::fillExternalContainer(vector<string>& container){
    container.insert(container.end(), inventory_.begin(), inventory_.end());
    return container;
 }