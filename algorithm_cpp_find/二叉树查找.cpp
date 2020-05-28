//
// Created by ninerui on 2020/5/28.
//
#include<cstdlib>

//非递归查找算法
BSTNode *BST_Search(BiTree T, ElemType key, BSTNode *&p) {
    //查找函数返回指向关键字值为key的结点指针，不存在则返回NULL
    p = NULL;
    while (T != NULL && key != T->data) {
        p = T;                          //指向被查找结点的双亲
        if (key < T->data)
            T = T->lchild;              //查找左子树
        else
            T = T->rchild;              //查找右子树
    }
    return T;
}

//递归算法
Status Search_BST(BiTree T, int key, BiTree f, BiTree *p) {
    //查找BST中是否存在key，f指向T双亲，其初始值为NULL
    //若查找成功，指针p指向数据元素结点，返回true；
    //若失败，p指向查找路径上访问的最后一个结点并返回false
    if (!T) {
        *p = f;
        return false;
    } else if (key == T->data) {                      //查找成功
        *p = T;
        return true;
    } else if (key < T->data)
        return Search_BST(T->lchild, key, T, p);   //递归查找左子树
    else
        return Search_BST(T->rchild, key, T, p);   //递归查找右子树

}