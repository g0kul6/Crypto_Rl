import os
import sys
from datetime import date
now = date.today()
path_dir = os.path.abspath(os.getcwd())
folder_name = "/CHECKPOINT/checkpoint{}/".format(now)
images_dir = path_dir + folder_name + "point_images/"
test_dir = path_dir + folder_name + "test/"
import matplotlib.pyplot as plt
import numpy as np
import wandb
import torch 

import argparse
parser = argparse.ArgumentParser()
#algo
parser.add_argument("--algo",type=str,default="vpg",required=True)
#feature extractor
parser.add_argument("--feature_extractor",type=str,default="mlp",required=True)
#reward type
parser.add_argument("--reward_type",type=str,default="sr",required=True)
args = parser.parse_args()

def plot_action_state(action_path,state_path,rewards_path,cumulative_rewards_path):
    actions = np.load(action_path)
    states = np.load(state_path)
    rewards = np.load(rewards_path)
    cumulative_rewards = np.load(cumulative_rewards_path)
    buy_count = 0
    buys = []
    index_buys = []
    sell_count = 0
    sells = []
    index_sells = []
    hold_count = 0
    holds = []
    index_holds = []
    plt.plot(range(len(states[1:1001,0,0])),states[1:1001,0,0])
    for i in range(len(actions[0:1000])):
        if actions[i] == 0:
            hold_count += 1
            index_holds.append(i)
            holds.append(states[1+i,0,0])
        elif actions[i] == 1:
            buy_count += 1
            index_buys.append(i)
            buys.append(states[1+i,0,0])
        elif actions[i] == 2:
            sell_count +=1
            index_sells.append(i)
            sells.append(states[1+i,0,0])
    plt.scatter(index_holds,holds,color="r",label="hold")
    plt.scatter(index_buys,buys,color="g",label="buy")
    plt.scatter(index_sells,sells,color="b",label="sell")
    plt.title('hold:{},buy:{},sell:{}'.format(hold_count,buy_count,sell_count))
    plt.legend()
    plt.savefig("{}{}_{}_{}.png".format(images_dir,args.algo,args.feature_extractor,args.reward_type))
    plt.show()
    print("hold:",hold_count,"buy:",buy_count,"sell:",sell_count)
    
    
    
if __name__== '__main__':
    plot_action_state(action_path=test_dir+"/action_{}_{}_{}.npy".format(args.algo,args.feature_extractor,args.reward_type),
                    state_path=test_dir+"/state_{}_{}_{}.npy".format(args.algo,args.feature_extractor,args.reward_type),
                    rewards_path=test_dir+"/rewards_{}_{}_{}.npy".format(args.algo,args.feature_extractor,args.reward_type),
                    cumulative_rewards_path=test_dir+"/cumulative_rewards_{}_{}_{}.npy".format(args.algo,args.feature_extractor,args.reward_type))