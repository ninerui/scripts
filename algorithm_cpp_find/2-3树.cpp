//
// Created by ninerui on 2020/5/28.
//

two_three *search23(two_three *t, element x) {
    while (t) {
        if (x < t->data_l) {
            t = t->left_child;
        } else if (x > t->data_l && x < t->data_r) {
            t = t->middle_child;
        } else if (x > t->data_r) {
            t = t->right_child;
        } else {
            return t;
        }
    }
    return NULL;
}