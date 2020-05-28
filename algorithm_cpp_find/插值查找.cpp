//
// Created by ninerui on 2020/5/28.
//

#include <cstdio>

int array[10] = {1, 4, 9, 16, 27, 31, 33, 35, 45, 64};

int InsertionSearch(int data) {
    int low = 0;
    int high = 10 - 1;
    int mid = -1;
    int comparisons = 1;
    int index = -1;

    while (low <= high) {
        printf("比较 %d 次\n", comparisons);
        printf("low : %d, list[%d] = %d\n", low, low, array[low]);
        printf("high : %d, list[%d] = %d\n", high, high, array[high]);

        comparisons++;
        mid = low + (((double) (high - low) / (array[high] - array[low])) * (data - array[low]));
        printf("mid = %d\n", mid);

        // 没有找到
        if (array[mid] == data) {
            index = mid;
            break;
        } else {
            if (array[mid] < data) {
                low = mid + 1;
            } else {
                high = mid - 1;
            }
        }
    }

    printf("比较次数: %d\n", --comparisons);
    return index;
}

int main() {
    int location = InsertionSearch(27);  //测试代，查27，可以找到
    if (location != -1) {
        printf("查找元素顺序为: %d\n", (location + 1));
    } else {
        printf("没有查找到");
    }
    return 0;
}