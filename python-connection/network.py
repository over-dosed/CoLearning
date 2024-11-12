# OSC client setup / send predicted landmarks over OSC
from pythonosc import udp_client
osc_ip = "127.0.0.1"
osc_port = 12000
client = udp_client.SimpleUDPClient(osc_ip, osc_port)

"""Small example OSC server

This program listens to several addresses, and prints some information about
received packets.
"""
import argparse
from pythonosc.dispatcher import Dispatcher
from pythonosc import osc_server

import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np

# 定义4层神经网络
class Posenet(nn.Module):
    def __init__(self, input_size, hidden_size, output_size):
        super(Posenet, self).__init__()
        self.fc1 = nn.Linear(input_size, hidden_size)
        self.fc2 = nn.Linear(hidden_size, hidden_size)
        self.fc3 = nn.Linear(hidden_size, hidden_size)
        self.fc4 = nn.Linear(hidden_size, output_size)

    def forward(self, x):
        x = torch.relu(self.fc1(x))
        x = torch.relu(self.fc2(x))
        x = torch.relu(self.fc3(x))
        x = self.fc4(x)
        return x

# 全局变量定义
input_size = 17  # 输入层神经元数量（17个关节点坐标）
hidden_size = 64  # 隐藏层神经元数量
output_size = 17  # 输出层数量（同样是17个坐标）
model = Posenet(input_size, hidden_size, output_size)
criterion = nn.MSELoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)
# training_data = [] 
training_data = None

def body_data_handler(unused_addr, args, body):
    """
    接收body数据并处理
    """
    print("Received body data:", body)
    try:
        process_body_data(body)
        train_model()
    except ValueError:
        pass

def process_body_data(body):
    """
    处理接收到的body数据，将其转化为Tensor并加入训练数据。
    """
    data = np.array(body, dtype=np.float32)
    if data.size == input_size:
        training_data = data

def train_model():
    """
    训练模型
    """
    # model.train()
        
    # inputs = torch.tensor(training_data, dtype=torch.float32)

    # optimizer.zero_grad()
    # outputs = model(inputs)
    # output_numpy = outputs.clone().detach().numpy()
    # for landmark_idx in range(17):
    #     landmark = output_numpy[landmark_idx]
    #     client.send_message(f"/landmark/{landmark_idx}", landmark)

    # loss = criterion(outputs)
    # loss.backward()
    # optimizer.step()
    # print("Loss:", loss.item())

    client.send_message(f"/landmark", [22, 33])
  

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip",
        default="127.0.0.1", help="The ip to listen on")
    parser.add_argument("--port",
        type=int, default=4444, help="The port to listen on")
    args = parser.parse_args()

    dispatcher = Dispatcher()
    dispatcher.map("/body", body_data_handler, "Body")

    server = osc_server.ThreadingOSCUDPServer(
        (args.ip, args.port), dispatcher)
    print("Serving on {}".format(server.server_address))
    server.serve_forever()