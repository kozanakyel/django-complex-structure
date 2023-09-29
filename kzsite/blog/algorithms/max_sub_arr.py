from typing import List

class FindMaxSubArrService:
    @staticmethod
    def find_max_sub_arr_brute_force(arr: List):
        sums: list[int] = [0]
        for a in arr:
            sums.append(sums[-1]+a)
        max_sum = -1e100
        left_index = -1
        right_index = -1
        for i in range(len(arr)):
            for j in range(i, len(arr)):
                if sums[j + 1] - sums[i] > max_sum:
                    max_sum = sums[j + 1] - sums[i]
                    left_index = i
                    right_index = j
        return left_index, right_index, max_sum
    
    @staticmethod
    def find_max_crossing_subarray(arr, low, mid, high):
        left_sum = -1e100
        sum = 0
        for i in range(mid - 1, low - 1, -1):
            sum = sum + arr[i]
            if sum > left_sum:
                left_sum = sum
                max_left = i
        right_sum = -1e100
        sum = 0
        for j in range(mid, high):
            sum = sum + arr[j]
            if sum > right_sum:
                right_sum = sum
                max_right = j
        return max_left, max_right, left_sum + right_sum

    @staticmethod
    def find_maximum_subarray(arr, low, high):
        if low >= high:
            return -1, -1, -1e100
        if low + 1 == high:
            return low, low, arr[low]
        mid = (low + high) // 2
        left_low, left_high, left_sum = FindMaxSubArrService.find_maximum_subarray(arr, low, mid)
        right_low, right_high, right_sum = FindMaxSubArrService.find_maximum_subarray(arr, mid, high)
        cross_low, cross_high, cross_sum = FindMaxSubArrService.find_max_crossing_subarray(arr, low, mid, high)
        if left_sum >= right_sum and left_sum >= cross_sum:
            return left_low, left_high, left_sum
        if right_sum >= left_sum and right_sum >= cross_sum:
            return right_low, right_high, right_sum
        return cross_low, cross_high, cross_sum
    