# -*- coding: utf-8 -*-


from numpy import *

Sudoku = zeros((9, 9), dtype = int32)
Solution = zeros((9, 9), dtype = int32)# 解阵列

"""#################栈类#################"""
class Stack:
    # self
    def __init__(self):
        self.items = []
    # 检查栈是否为空
    def isEmpty(self):
        return len(self.items) == 0
    # 入栈
    def push(self, item):
        self.items.append(item)
    # 出栈
    def pop(self):
        return self.items.pop()
    # 提取栈顶元素
    def peek(self):
        if not self.isEmpty():
            return self.items[len(self.items) - 1]
    # 获取栈中元素个数
    def size(self):
        return len(self.items)

"""#################定义栈等#################"""
# 栈类
S = Stack()
# 栈内元素
for p in range(1, 81):
    # S_Map1, S_Map2, S_Map3, ……, S_Map80
    S_Map = "S_Map" + "%d" %p
    exec(S_Map + " = zeros((9, 9), dtype = int32)")
# 单解标识
FSingleSolution = False

def Solve_Sudoku(Map, mode):
    # 单解跳出
    global FSingleSolution
    if FSingleSolution == True:
        return Map,True
    # 候选数阵列
    Candidates = ones((9, 9, 9), dtype = int32)
    # 检查是否求解完毕
    FComplete = True
    for i in range(0, 9):
        for j in range(0, 9):
            if Map[i][j] == 0:
                FComplete = False
                break
    # 求解完毕
    if FComplete == True:
        # 输出解
        print "Solution Accomplished!"
        global Solution
        Solution = Map.copy()# 独立复制
        # 找到单解后返回
        if mode == 0:
            FSingleSolution = True
            return Map,True
        # 返回操作并出栈
        if S.isEmpty() == False:
            Map = S.peek().copy()
            S.pop()
        return Map,True
    # 未求解完毕
    else:
        # 更新候选数阵列
        for i in range(0, 9):
            for j in range(0, 9):
                if Map[i][j] != 0:
                    # 列
                    for m in range(0, 9):
                        if Map[m][j] == 0:
                            Candidates[m][j][Map[i][j] - 1] = 0
                    # 行
                    for n in range(0, 9):
                        if Map[i][n] == 0:
                            Candidates[i][n][Map[i][j] - 1] = 0
                    # 单元九宫格
                    for m in range(3 * (i // 3), 3 * (i // 3) + 3):
                        for n in range(3 * (j // 3), 3 * (j // 3) + 3):
                            if Map[m][n] == 0:
                                Candidates[m][n][Map[i][j] - 1] = 0
        # 寻找最少候选数
        Min = 9
        for m in range(0, 9):
            for n in range(0, 9):
                count = sum(Candidates[m][n][:])
                if count < Min:
                    Min = count
                    Min_i = m
                    Min_j = n
        # 候选数为0(无解分支)
        if Min == 0:
            if 0 in Map:
                return None, False
            else:
                # 返回操作并出栈
                Map = S.peek().copy()
                S.pop()
                return Map,True
        # 存在候选数
        else:
            # 逐一假设
            for k in range(1, Min + 1):
                # 入栈
                p = "%d" %(S.size() + 1)
                S_Map = "S_Map" + p
                exec(S_Map + " = Map.copy()")
                exec("S.push(" + S_Map + ")")# S.push(S_Map【S.size()+1】)
                # 填入候选数
                count = 0
                for o in range(0, 9):
                    count = count + Candidates[Min_i][Min_j][o]
                    if count == k:#有k个候选数则只需要尝试k次
                        break
                Map[Min_i][Min_j] = o + 1
                if Solve_Sudoku(Map, mode)[1] != False:
                    Map = Solve_Sudoku(Map, mode)[0]
                else:
                    return None, False
                # 单解跳出
                if FSingleSolution == True:
                    return Map,True
            # 返回操作并出栈
            if S.isEmpty() == False:
                Map = S.peek().copy()
                S.pop()
            return Map,True
            

tmp = [1,2,3,4,5,6,7,8,9]
def check_sudoku(Map):
    #
    if len(Map)<>9:
        return False
    #
    for j in Map:
        if sorted(j)<>tmp:
            return False
    #
    for i in range(9):
        if sorted([j[i] for j in Map])<>tmp:
            return False
    #
    for n in range(3):
        for k in range(3):
            flag = []
            for i in range(n*3,n*3+3):
                for j in range(k*3,k*3+3):
                    flag.append(Map[i][j])
            if sorted(flag)<>tmp:
                return False
    return True

def main():
    #Print_Sudoku(Sudoku)
    Solve_Sudoku(Sudoku, 0)# 搜索单解
    #Solve_Sudoku(Sudoku, 1)# 搜索所有解
    #Print_Sudoku(Solution)

"""#################main#################"""
if __name__ == '__main__':
    main()