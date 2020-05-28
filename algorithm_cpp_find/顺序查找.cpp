#include <cstdio>
#include <cstdlib>

#define keyType int
typedef struct {
    keyType key;  // 查找表中每个数据元素的值
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

//顺序查找函数，其中key为要查找的元素
int Search_seq(SSTable *str, keyType key) {
    //str->elem[0].key=key;//将关键字作为一个数据元素存放到查找表的第一个位置，起监视哨的作用
    int len = str->length;
    //从最后一个数据元素依次遍历，一直遍历到数组下标为0
    for (int i = 1; i < len + 1; i++)   //创建数据从数组下标为1开始，查询也从1开始
    {
        if (str->elem[i].key == key) {
            return i;
        }
    }
    //如果 i=0，说明查找失败；查找成功返回要查找元素key的位置i
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
    int location = Search_seq(str, key);
    if (location == 0) {
        printf("查找失败");
    } else {
        printf("要查找的%d的顺序为：%d", key, location);
    }
    return 0;
}