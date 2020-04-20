from dual_network import dual_network
from make_data import self_play
from train import train_network
from evaluate import evaluate_network

dual_network()

for i in range(10):
    print('Train',i,'------------')
    self_play()

    train_network()

    update_best_player = evaluate_network()
