class MergeSort:
    # merge two sorted list together
    def merge(self, left, right):
        res = []
        while len(left) != 0 and len(right) != 0:
            if left[0] < right[0]:
                res.append(left[0])
                left.remove(left[0])
            else:
                res.append(right[0])
                right.remove(right[0])
        if len(left) == 0:
            res = res + right
        else:
            res = res + left
        return res
    # merge sort algorithm
    def merge_sort(self, nums):
        if len(nums) <= 1:
            return nums
        middle = len(nums) // 2 # Find the middle point and devide it
        left = nums[:middle]
        right = nums[middle:]
        left = self.merge_sort(left) # recursively do merge sort
        right = self.merge_sort(right)
        return list(self.merge(left, right)) # merge two sorted list 

    def solve(self, nums):
        #TODO Starts
        #You need add code here and you are not allowed to modify code elsewhere
        #TOD Ends
        return nums

def load_data():
    f = open('unsorted.txt')
    lines = f.readlines()
    f.close()
    nums = [int(line.strip()) for line in lines]
    return nums

def save_result(nums):
    f = open('sorted.txt', 'w')
    for n in nums:
        f.write(str(n)+'\n')
    f.close()


if __name__ == '__main__':
    unsorted_list = load_data()
    ms = MergeSort()
    sorted_list = ms.solve(unsorted_list)
    save_result(sorted_list)
    print(sorted_list)

