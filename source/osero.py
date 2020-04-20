#osero.py
#オセロの盤面を保持するクラスStateの定義

import random
import math

class State:
    def __init__(self, pieces=None, enemy_pieces=None, depth=0, scale=8):
        self.dxy = ((1, 0),(1, 1),(0, 1),(-1, 1),(-1, 0),(-1, -1),(0, -1), (1, -1))
        self.pass_end = False
        
        self.pieces = pieces
        self.enemy_pieces = enemy_pieces
        self.depth = depth
        self.scale = scale
        
        if pieces == None or enemy_pieces == None:
            #初期配置
            self.pieces = [0] * (self.scale**2)
            self.pieces[27] = self.pieces[36] = 1
            self.enemy_pieces = [0] * (self.scale**2)
            self.enemy_pieces [28] = self.enemy_pieces[35] = 1
        
    def piece_count(self, pieces):
        count = 0
        for i in pieces:
            if i == 1:
                count += 1
        return count
    
    def is_lose(self):
        return self.is_done() and self.piece_count(self.pieces) < self.piece_count(self.enemy_pieces)
        
    def is_draw(self):
        return self.is_done() and self.piece_count(self.pieces) == self.piece_count(self.enemy_pieces)
        
    def is_done(self):
        return (self.piece_count(self.pieces) + self.piece_count(self.enemy_pieces) == self.scale**2) or self.pass_end
        
    def next(self, action):
        state = State(self.pieces.copy(), self.enemy_pieces.copy(), self.depth + 1)
        #石の配置、ひっくり返す
        if action != self.scale**2:
            state.is_legal_action_xy(action%self.scale, int(action/self.scale), True) #x軸はあまり、y軸は商
        #相手の盤面
        w = state.pieces
        state.pieces = state.enemy_pieces
        state.enemy_pieces = w
            
        #今回もパス、相手の合法手もパスしかない場合
        if action == self.scale**2 and state.legal_actions() == [self.scale**2]:
            state.pass_end = True
        return state
        
    def legal_actions(self):
        actions = []
        for j in range(self.scale):
            for i in range(self.scale):
                if self.is_legal_action_xy(i, j):
                    actions.append(i + j * self.scale)

        if len(actions) == 0:
            actions.append(self.scale**2)
        return actions
        
    def is_legal_action_xy(self, x, y, flip=False):
        
        #指定の方向に対して合法手の条件を満たしているか
        def is_legal_action_xy_dxy(x, y, dx, dy):
            x_s, y_s = x, y
            x, y = x + dx, y + dy
            #盤面からはみ出す、相手の石がない
            if y < 0 or self.scale <= y or x < 0 or self.scale <= x or self.enemy_pieces[x+y*self.scale] != 1:
                return False
                
            for j in range(self.scale):
                #石がない
                if y < 0 or self.scale <= y or x < 0 or self.scale <= x or \
                    (self.enemy_pieces[x+y*self.scale] == 0 and self.pieces[x+y*self.scale]==0):
                    return False
                #自分の石があった
                if self.pieces[x+y*self.scale] == 1:
                    #間の敵の石を自分のものにする
                    if flip:
                        for i in range(self.scale):
                            x, y = x-dx, y-dy
                            #print(x,y)
                            if x_s == x and y_s == y:
                                return True
                            self.pieces[x+y*self.scale] = 1
                            self.enemy_pieces[x+y*self.scale] = 0
                    return True
                x, y = x + dx, y + dy
            return False
        
        #すでに石がおいてある
        if self.enemy_pieces[x+y*self.scale] == 1 or self.pieces[x+y*self.scale] == 1:
            return False
            
        flag = False
        for dx, dy in self.dxy:
            if is_legal_action_xy_dxy(x, y, dx, dy):
                flag = True
        if flag:
            if flip:
                self.pieces[x+y*self.scale] = 1
        return flag
        
    def is_first_player(self):
        return self.depth % 2 == 0
        
    def __str__(self):
        ox = ('o', 'x') if self.is_first_player() else ('x', 'o')
        str = ''
        for i in range(self.scale ** 2):
            if self.pieces[i] == 1:
                str += ox[0]
            elif self.enemy_pieces[i] == 1:
                str += ox[1]
            else:
                str += '-'
            if i % self.scale == self.scale - 1:
                str += '\n'
        return str

if __name__ == '__main__':
    import sys
    def random_action(state):
        legal_actions = state.legal_actions()
        return legal_actions[random.randint(0, len(legal_actions)-1)]

    state = State()
    print(state)
    while True:
        if state.is_done():
            if state.is_lose() and state.is_first_player():
                print('あやちゃんのまけです')
                break
            if state.is_lose():
                print('ぼくのまけです')
                break
        if state.is_first_player():
            print('x yで指定')
            [x, y] = input().split(' ')
            action = int(x) + int(y) * state.scale
            print(action)
        else:
            action = random_action(state)
        #print(action)
        state = state.next(action)
        print(state)
        print()