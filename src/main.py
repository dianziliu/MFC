import math
import os
import sys
sys.path.append(".")
sys.path.append(os.path.dirname(__file__))
# os.environ["CUDA_VISIBLE_DEVICES"]="0"
import pickle
import pandas as pd
import tensorflow as tf
from absl import flags as tf_flags
from model import ADSE
from GroupDataLoader import GData_Loader
import numpy as np
from ExpertTSE import ExpertTSE
# from MuModel import MuADSE
from MuModel import MuADSE

ReviewShare=4
IntercShare=8
RatingShare=12

def prepare_group_info(data_loader, p, mode=12):
    """
        待完善
    """
    p = p[:-4]
    group_info = dict()
    group_info["num_user_group"] = int(math.sqrt(data_loader.num_user))
    group_info["num_item_group"] = int(math.sqrt(data_loader.num_item))

    sim_path_fmt="/mnt/Disk3/ysq/localFile/TSE/sim_res/{}_{}_{}_{}.pkl"

    with open(sim_path_fmt.format(p, "rating", "os", "user"), "rb") as f:
        group_info["user_rating"] = pickle.load(f) 
    with open(sim_path_fmt.format(p, "interc", "Jacc", "user"), "rb") as f:
        group_info["user_interc"] = pickle.load(f) 
    with open(sim_path_fmt.format(p, "review", "ADF", "user"), "rb") as f:
        group_info["user_review"] = pickle.load(f) 

    with open(sim_path_fmt.format(p, "rating", "os", "item"), "rb") as f:
        group_info["item_rating"] = pickle.load(f) 
    with open(sim_path_fmt.format(p, "interc", "Jacc", "item"), "rb") as f:
        group_info["item_interc"] = pickle.load(f) 
    with open(sim_path_fmt.format(p, "review", "ADF", "item"), "rb") as f:
        group_info["item_review"] = pickle.load(f) 

    return group_info

def prepare_group_info_random(data_loader, mode=12):
    group_info = dict()
    group_info["num_user_group"] = int(math.sqrt(data_loader.num_user))
    group_info["num_item_group"] = int(math.sqrt(data_loader.num_item))
    
    group_info["user_rating"] = np.random.randint(0, group_info["num_user_group"], data_loader.num_user)
    group_info["user_interc"] = np.random.randint(0, group_info["num_user_group"], data_loader.num_user)
    group_info["user_review"] = np.random.randint(0, group_info["num_user_group"], data_loader.num_user)
    group_info["item_rating"] = np.random.randint(0, group_info["num_item_group"], data_loader.num_item)
    group_info["item_interc"] = np.random.randint(0, group_info["num_item_group"], data_loader.num_item)
    group_info["item_review"] = np.random.randint(0, group_info["num_item_group"], data_loader.num_item)
    
    return group_info

if __name__ == "__main__":
    paths = [
        'Musical_Instruments_5.json',
        "Office_Products_5.json",
        'Grocery_and_Gourmet_Food_5.json',
        "Video_Games_5.json",
        "Sports_and_Outdoors_5.json",
    ]
    prefix = 'amazon_data'

    flags = tf_flags.FLAGS 	
    tf_flags.DEFINE_string('filename', '', 'name of file')
    tf_flags.DEFINE_string("res_dir", '', "name of dir to store result")
    tf_flags.DEFINE_integer('batch_size', 128, 'batch size')
    tf_flags.DEFINE_integer('emb_size', 100, 'embedding size')
    tf_flags.DEFINE_integer('num_class', 5, "num of classes")
    tf_flags.DEFINE_integer('epoch', 50, 'epochs for training')
    tf_flags.DEFINE_string('ckpt_dir', '', 'directory of checkpoint')
    tf_flags.DEFINE_string('train_test', 'train', 'training or test')
    tf_flags.DEFINE_string("glovepath", "glove", "glove path")
    tf_flags.DEFINE_string("res_path", "res/res.csv", "save predict res")
    tf_flags.DEFINE_float('test_size', 0.2, "set test size to split data")
    tf_flags.DEFINE_string('res', '', "res path to save")

    tf_flags.DEFINE_integer('mode', -1, "2,4,8表示三种层次的共享")
    tf_flags.DEFINE_integer('doc_layers', 3, "doc层注意力的层数")
    tf_flags.DEFINE_float('doc_dropout', .3, "doc层注意力的层数")
    tf_flags.DEFINE_float("group_scale", 1, "group scale based on sqrt(|U|)")
    tf_flags.DEFINE_float('epoch_size', 0.1, 'use sub epoch to fit model')
    tf_flags.DEFINE_string("routing_mode", "soft", "the routing mode of shared embedding, hard or soft")
    tf_flags.DEFINE_integer("use_reg", 0, "use reguler 1 or not 0")
    tf_flags.DEFINE_float('routing_lr', 0.001, 'routing_lr')

    flags(sys.argv)

    # for i in range(1):
    # filename = paths[0]
    filename = flags.filename
    flags.filename = os.path.join(prefix, filename)
    flags.res_dir = filename
    flags.ckpt_dir = os.path.join("CKPT_DIR", "MFC" + filename.split('.')[0])
    # flags.res = f"/mnt/Disk3/ysq/localFile/TSE/res/preunlikely{i}.csv"

    data_loader = GData_Loader(flags)
    
    ## 不太明白这块是干嘛的
    # if i == 0:
    #     data_loader.set_mode("r")
    #     print("revise")
    # elif i == 1:
    # data_loader.set_mode("n")
    # print("most likely")
    # else:
    #     data_loader.set_mode("rd")
    #     print("random")

    ## 1. 准备训练数据
    group_info = prepare_group_info(data_loader, filename)
    
    ## 2. 创建了3个专家模型
    expert = ExpertTSE(flags, data_loader, group_info=group_info, layer="layer1")
    expert2 = ExpertTSE(flags, data_loader, group_info=group_info, layer="layer2")
    expert3 = ExpertTSE(flags, data_loader, group_info=group_info, layer="layer3")
    
    ## 3. 创建了最终的预测模型
    model = MuADSE(flags, data_loader, group_info=group_info, expert=expert, expert2=expert2, expert3=expert3, task="ctsr")

    model.get_model(summary=True)
    
    ## 4. 模型训练 
    if flags.epoch_size == -1:
        res = model.train(data_loader)
        res_Df = pd.DataFrame(res)
        print(res_Df)
        if flags.res != "":
            res_Df.to_csv(flags.res, index=False)
    elif flags.epoch_size == 1:
        res = model.train_subfit_subdata(data_loader)
        res_Df = pd.DataFrame(res)
        print(res_Df)
        if flags.res != "":
            res_Df.to_csv(flags.res, index=False)
    elif 0 <= flags.epoch_size < 1:
        res = model.train_subfit_subdata(data_loader, flags.epoch_size)
        res_Df = pd.DataFrame(res)
        print(res_Df)

    else:
        print(flags.epoch_size, "epoch_size error")
        res = model.train_subfit(data_loader, epoch_size=flags.epoch_size)
        print(res)
    if flags.res!= "":
        print('save res')
        res_Df.to_csv(flags.res, index=False)