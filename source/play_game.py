from tensorflow.keras.models import load_model
from osero import State
from mcts import pv_mcts_action
import csv
from datetime import datetime
if __name__ == '__main__':
    model = load_model('./model/best.h5')

    state = State()

    next_action = pv_mcts_action(model, 1.0)
    print(state)
    history = []
    while True:
        try:
            if state.is_done():
                break
            if state.is_first_player():
                print('x yで場所を指定')
                [x, y] = input().split(' ')
                action = int(x) + int(y) * 8
                if action < 0 or action > 64:
                    continue
            else:
                action = next_action(state)

            state = state.next(action)
            history.append(str(action%8) + ' ' + str(int(action/8)))
            print(state)
            print(str(action%8) +' '+str(int(action/8)))
        except:
            break
    now_time = datetime.now()
    with open('./{0:%Y%m%d%H%M%S}.csv'.format(now_time),'w') as f:
        writer = csv.writer(f, lineterminator="\n")
        writer.writerows(history)


