import threading

class Wallet:
    def __init__(self):
        """Initialize an empty wallet."""
        self.resources = {}
        self.lock = threading.Lock()
        self.condition = threading.Condition(self.lock)
    


    def get(self, resource):
        """Returns the amount of a given `resource` in this wallet."""
        with self.lock:
            if resource in self.resources:
                return self.resources[resource]
            else:
                return 0
        
        
                

    def change(self, resource, delta):
        """
        Modifies the amount of a given `resource` in this wallet by `delta`.
        - If `delta` is negative, this function MUST NOT RETURN until the resource can be satisfied.
            (This function MUST BLOCK until the wallet has enough resources to satisfy the request.)
        - Returns the amount of resources in the wallet AFTER the change has been applied.
        """
        with self.condition:
            while delta < 0 and self.resources.get(resource, 0) + delta < 0:
                self.condition.wait()
            
            self.resources[resource] = self.resources.get(resource, 0) + delta
            self.condition.notify_all()
            return self.resources.get(resource)
            
        
    def try_change(self, resource, delta):
        """
        Like change, but if change would block
        this method instead leaves the resource unchanged and returns False.
        """
        with self.condition:
            if delta < 0 and self.resources.get(resource,0) + delta < 0:
                return False
            self.resources[resource] = self.resources.get(resource, 0) + delta
            self.condition.notify_all()
            return self.resources.get(resource, 0)
        

    def transaction(self, **delta):
        """
        Like calling change(key, value) for each key:value in `delta`, except:
        - All changes are made at once. If any change would block, the entire transaction blocks.
            Only continues once *all* the changes can be made as one atomic action.
        - Returns a dict of {resource:new_value} for all resources in the transaction.
        """
        with self.condition:
            # while True:
            #     can_change = True
            #     for key, value in delta.items():
            #         if value < 0 and value + self.resources.get(key, 0)< 0:
            #             can_change = False
            #             break
            #     if can_change:
            #         break
                
            #     self.condition.wait()
            while True:
                can_change = True
                if value + self.resources.get(self, key) < 0:
                    can_change = False
                    break
                    
                if (can_change):
                    break
                    
                self.condition.wait()  
            for resource, value in delta.items(): 
                new_value = value + self.resources.get(resource, 0)
                self.resources[resource] = new_value
            self.condition.notify_all()
            return {res: self.resources[res] for res in delta}
                        
                        
                        
                    