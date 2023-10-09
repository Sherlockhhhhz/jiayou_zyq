import torch
import matplotlib.pyplot as plt # 画图
import torch.nn.functional as F # 激励函数

x=torch.unsqueeze(torch.linspace(-1,1,100),dim=1) #x data(tensor),shape=(100,1)
y=-x.pow(3)+2*x.pow(2)+0.2*torch.rand(x.size()) # noisy y data (tensor), shape=(100, 1)
# y=math.sin(x)+0.2*torch.rand(x.size())

class Net(torch.nn.Module): #继承 torch 的module （固定）
    # 定义层的信息，n_feature多少个输入, n_hidden每层神经元, n_output多少个输出
    def __init__(self, n_feature, n_hidden, n_output):
        super(Net,self).__init__()    #继承__init__功能 （固定）
        #定理每层用什么样的形式
        self.hidden1 = torch.nn.Linear(n_feature,n_hidden) # 定义隐藏层，线性输出
        self.hidden2 = torch.nn.Linear(n_hidden, n_hidden)  # 定义输出层线性输出
        self.hidden3 = torch.nn.Linear(n_hidden, n_hidden)  # 定义输出层线性输出
        self.predict=torch.nn.Linear(n_hidden,n_output)   # 定义输出层线性输出

    # 定义神经网络前向传递的过程，把__init__中的层信息一个一个的组合起来
    def forward(self, x):    # x是输入信息就是data，这同时也是module中的forward功能
        #正向传播输入值，神经网络分析出输出值
        x = F.relu(self.hidden1(x))    #激励函数（隐藏层的线性值）
        x = F.relu(self.hidden2(x))
        x = F.relu(self.hidden3(x))
        x = self.predict(x)    #输出值
        return x

net=Net(n_feature=1, n_hidden= 20, n_output=1)
print(net)  # 打印net 的结构

#optimizer 是训练的工具
optimizer = torch.optim.SGD(net.parameters(),lr=0.01)    #传入net的所有参数，学习率
loss_func = torch.nn.MSELoss()    #预测值和真实值的误差计算公式（均方差）

for t in range(2000): # 训练的步数2000步
    prediction = net(x)    #喂给net训练数据x, 每迭代一步，输出预测值
    loss=loss_func(prediction,y)    #计算预测值和真实值之间的误差
    optimizer.zero_grad() #清空上一步的残余更新参数值
    loss.backward()    #误差反向传播，计算参数更新值
    optimizer.step()    #将参数更新值施加到net的parameters上

    if t%5 == 0:  # 每五步绘一次图
        #plot and show learning process
        plt.cla()
        plt.scatter(x.data.numpy(), y.data.numpy())
        plt.scatter(x.data.numpy(), prediction.data.numpy())
        plt.text(0.5,0,'Loss=%.4f'%loss.data.numpy(),fontdict={'size':20,'color':'red'})
        plt.pause(0.02)#画的图只存在0.1秒

plt.show()