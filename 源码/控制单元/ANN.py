import torch
from torch import nn
from torch.nn import init
import numpy as np
import torchvision
import torchvision.transforms as transforms
from torchvision import datasets


class network(nn.Module):
    def __init__(self):
        super(network, self).__init__()
        self.layer = nn.Sequential(
            nn.Linear(2, 100),
            nn.ReLU(),
            nn.Linear(100,64),
            nn.ReLU(),
            nn.Linear(64, 4))

    def forward(self, x):
        x = x.view(x.size()[0], -1)
        x = self.layer(x)
        return x

net = network()

for name, param in net.named_parameters():
    if 'weight' in name:
        init.normal_(param, mean=0, std=0.01)
    if 'bias' in name:
        init.constant_(param, val=0)

# 损失函数使用交叉熵
criterion = nn.MSELoss()
# 优化函数使用 SGD
optimizer = torch.optim.Adam(net.parameters(), lr=0.04)
'''for epoch in range(24):
    train_l_sum =0
    f = open("position.txt",mode='r')
    a = f.readlines()
    g = open("train.txt",mode='r')
    b = g.readlines()
    for i in range(len(a)):
        p = a[i].strip('\n').split()
        x = float(p[0])
        y = float(p[1])
        input = torch.tensor([[x,y]]).float()
        output = net(input)
        q = b[i].strip("\n").split()
        num1 = float(q[0])
        num2 = float(q[1])
        num3 = float(q[2])
        num4 = float(q[3])
        ground_truth = torch.tensor([[num1,num2,num3,num4]]).float()
        l = criterion(output,ground_truth)
        optimizer.zero_grad()          
        l.backward() # 计算梯度
        optimizer.step()  # 随机梯度下降算法, 更新参数
        train_l_sum += l.item()
    print(epoch,train_l_sum/81)
    f.close()
    g.close()

torch.save(net.state_dict(), "my_model.pth")
model = network()
model.load_state_dict(torch.load("my_model.pth"))
model.eval()

print(model(torch.tensor([[0,20]]).float()))'''
