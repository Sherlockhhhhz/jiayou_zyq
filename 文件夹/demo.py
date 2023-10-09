import torch
import torch.nn as nn
import matplotlib.pyplot as plt
import numpy as np

# 生成一些随机的训练数据
np.random.seed(0)
X = np.random.rand(100, 1) * 10
y = 2 * X.squeeze() + 1 + np.random.randn(100)

# 将数据转换为PyTorch张量
X = torch.tensor(X, dtype=torch.float32)
y = torch.tensor(y, dtype=torch.float32)

# 定义一个简单的线性模型
class LinearRegressionModel(nn.Module):
    def __init__(self):
        super(LinearRegressionModel, self).__init__()
        self.linear = nn.Linear(1, 1)  # 输入特征维度为1，输出维度为1

    def forward(self, x):
        return self.linear(x)

# 初始化模型
model = LinearRegressionModel()

# 定义损失函数和优化器
criterion = nn.MSELoss()
optimizer = torch.optim.SGD(model.parameters(), lr=0.01)

# 训练模型
num_epochs = 1000
for epoch in range(num_epochs):
    model.train()
    outputs = model(X)
    loss = criterion(outputs, y)
    optimizer.zero_grad()
    loss.backward()
    optimizer.step()

    if (epoch+1) % 100 == 0:
        print(f'Epoch [{epoch+1}/{num_epochs}], Loss: {loss.item():.4f}')

# 可视化训练结果
predicted = model(X).detach().numpy()

plt.scatter(X, y, label='Original data')
plt.plot(X, predicted, label='Fitted line', color='red')
plt.legend()
plt.show()