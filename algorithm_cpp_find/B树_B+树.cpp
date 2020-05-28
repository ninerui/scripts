//
// Created by ninerui on 2020/5/28.
//

BTNode *BTree_recursive_search(const BTree tree, KeyType key, int *pos) {
    int i = 0;
    while (i < tree->keynum && key > tree->key[i]) {
        ++i;
    }

    // 查找关键字
    if (i < tree->keynum && tree->key[i] == key) {
        *pos = i;
        return tree;
    }

    // tree 为叶子节点，找不到 key，查找失败返回
    if (tree->isLeaf) {
        return NULL;
    }

    // 节点内查找失败，但 tree->key[i - 1]< key < tree->key[i]，
    // 下一个查找的结点应为 child[i]

    // 从磁盘读取第 i 个孩子的数据
    disk_read(&tree->child[i]);

    // 递归地继续查找于树 tree->child[i]
    return BTree_recursive_search(tree->child[i], key, pos);
}
