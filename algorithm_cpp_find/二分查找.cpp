//
// Created by ninerui on 2020/5/28.
//

#include <cstdio>
#include <cstdlib>

#define keyType int
typedef struct {
    keyType key;//查找表中每个数据元素的值
} ElemType;

typedef struct {
    ElemType *elem;//存放查找表中数据元素的数组
    int length;//记录查找表中数据的总数量
} SSTable;

//创建查询数据
void Create(SSTable **st, int length) {
    (*st) = (SSTable *) malloc(sizeof(SSTable));
    (*st)->length = length;
    (*st)->elem = (ElemType *) malloc((length + 1) * sizeof(ElemType));
    printf("输入表中的数据元素：\n");
    //根据查找表中数据元素的总长度，在存储时，从数组下标为 1 的空间开始存储数据
    for (int i = 1; i <= length; i++) {
        scanf("%d", &((*st)->elem[i].key));
    }
}

//折半查找函数 key为要查找的元素
int Search_Bin(SSTable *str, keyType key) {
    int low = 1;//初始状态 low 指针指向第一个关键字
    int high = str->length;//high 指向最后一个关键字
    int mid;
    while (low <= high) {
        mid = (low + high) / 2;//int 本身为整形，所以，mid 每次为取整的整数
        if (str->elem[mid].key == key)//如果 mid 指向的同要查找的相等，返回 mid 所指向的位置
        {
            return mid;
        } else if (str->elem[mid].key > key)//如果mid指向的关键字较大，则更新 high 指针的位置
        {
            high = mid - 1;
        }
            //反之，则更新 low 指针的位置
        else {
            low = mid + 1;
        }
    }
    return 0;
}

int main() {
    SSTable *str;
    int num;
    printf("请输入创建数据元素的个数：\n");
    scanf("%d", &num);
    Create(&str, num);
    getchar();
    printf("请输入要查找的数据：\n");
    int key;
    scanf("%d", &key);
    int location = Search_Bin(str, key);
    if (location == 0) {
        printf("没有查找到");
    } else {
        printf("要查找的%d的顺序为：%d", key, location);
    }
    return 0;
}