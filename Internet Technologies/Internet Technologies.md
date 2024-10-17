
202409110002
后台姓名：潘昕玥
用户ID：34260
用户1V1昵称：潘昕玥
学生需求类型：作业辅导
学生基础：还可以
期望上课时间：尽快 墨尔本时间
学生DUE时间：9.13
用户类型：1v1老用户
院校：UMEL
年级：研一
专业：IT
科目代码：COMP90007
科目名称：Internet Technologies
备注：
1. 需要老师辅导作业主要讲第三题和第四题，第一题也需要老师提前看看。
2. 课前要做好课前沟通，学生想要尽快上课 需要老师细心认真备课以及做好课前沟通，学生对老师高要求。

For **Question 3** and **Question 4** from your network analysis project, here's how you can approach them based on the information provided in the project description:对于网络分析项目中的**问题 3**和**问题 4** ，您可以根据项目描述中提供的信息来处理它们：

### **Question 3: Measuring delay and jitter (4 marks)问题3：测量延迟和抖动（4分）**

#### **3.1 Wireshark Capture for Ping3.1 Wireshark 捕获 Ping**

1. Use Wireshark to capture the network trace when running the 

   ```
   ping
   ```

    command. Use one of the hosts from 

   Table 1

    (e.g., 

   ```
   iperf.he.net
   ```

    from the USA).

   运行`ping`命令时使用 Wireshark 捕获网络跟踪。使用**表 1**中的主机之一（例如，来自美国的`iperf.he.net` ）。

   - Steps:
     - Open Wireshark and set up a capture filter to capture only ping (ICMP) traffic. The filter can be set as `icmp`.打开 Wireshark 并设置捕获过滤器以仅捕获 ping (ICMP) 流量。过滤器可以设置为`icmp` 。
     - Run the command `ping <host> -c 4` (for Mac/Linux) or `ping <host>` (for Windows) with a specific number of packets (4).使用特定数量的数据包 (4) 运行命令`ping <host> -c 4` （对于 Mac/Linux）或`ping <host>` （对于 Windows）。
     - Capture and save the traffic.捕获并保存流量。
     - Analyze the captured packets to understand each step of the ping request and response.分析捕获的数据包以了解 ping 请求和响应的每个步骤。
     - Look for ICMP request and response packets in the capture and explain their working (ping sends an echo request, and the server replies with an echo response).在捕获中查找 ICMP 请求和响应数据包并解释其工作原理（ping 发送回显请求，服务器使用回显响应进行回复）。
     - Create a flow graph in Wireshark to show the ping packet flow.在 Wireshark 中创建流程图以显示 ping 数据包流。
   - **Explain the filter**: Make sure you explain why the filter captures only the ping packets (ICMP protocol) and excludes other traffic like DNS or mDNS.**解释过滤器**：确保解释为什么过滤器仅捕获 ping 数据包（ICMP 协议）并排除 DNS 或 mDNS 等其他流量。

#### **3.2 Delay and Jitter Measurements3.2 延迟和抖动测量**

1. Measure the round-trip delay for all the hosts in **Table 1** by running the `ping` command three times for each host.通过对每台主机运行 3 次`ping`命令来测量**表 1**中所有主机的往返延迟。

2. Calculate the average round-trip delay and jitter for each host. You can do this either manually or by using the standard deviation from the command output.

   计算每个主机的平均往返延迟和抖动。您可以手动或使用命令输出的标准差来执行此操作。

   - For example, if you ping a host and get round-trip times of `30ms`, `32ms`, and `35ms`, you can calculate the standard deviation to find jitter.例如，如果您 ping 主机并获得往返时间`30ms` 、 `32ms`和`35ms` ，则可以计算标准偏差来查找抖动。

3. Plot the 

   scatter charts

   :

   绘制**散点图**：

   - One for **average round-trip delay vs geographical distance**.一是**平均往返延迟与地理距离的关系**。
   - Another for **jitter vs geographical distance**.另一个是**抖动与地理距离的**关系。

4. Provide a table of results showing the calculated values and the plots.提供显示计算值和绘图的结果表。

5. Explain if there's any correlation between **delay and distance** or **jitter and distance** based on the network environment (e.g., network load, shared network, ISP speed). Consider the potential factors that may cause variation, like users sharing the network or network congestion.根据网络环境（例如网络负载、共享网络、ISP 速度）解释**延迟和距离**或**抖动和距离**之间是否存在相关性。考虑可能导致变化的潜在因素，例如用户共享网络或网络拥塞。

### **Question 4: Measuring the bandwidth-delay product (8 marks)问题4：测量带宽延迟积（8分）**

#### **4.1 Bandwidth-Delay Product**

1. **What it tells us**: The bandwidth-delay product gives the maximum amount of data that can be in transit in the network at any given time. It helps you understand the data transmission capability of a network. The larger the bandwidth-delay product, the more data the network can handle before an acknowledgment is received.**它告诉我们什么**：带宽延迟乘积给出了在任何给定时间可以在网络中传输的最大数据量。它可以帮助您了解网络的数据传输能力。带宽延迟乘积越大，网络在收到确认之前可以处理的数据就越多。
2. Run the `iperf` command three times for each host from **Table 1** to measure bandwidth and calculate the average bandwidth.对**表1**中的每台主机运行`iperf`命令3次，测量带宽并计算平均带宽。

#### **4.2 Time Slot Measurements**

1. Choose one host that is the furthest away from your location (e.g., **speedtest.masnet.ec** in Ecuador) and another that is closest.选择距离您所在位置最远的一台主机（例如厄瓜多尔的**speedtest.masnet.ec** ）和另一台最近的主机。

2. Run 

   ```
   iperf
   ```

    tests at four different time slots (morning, afternoon, evening, and night). Collect the results and analyze any variations in bandwidth.

   在四个不同的时间段（早上、下午、晚上和晚上）运行`iperf`测试。收集结果并分析带宽的任何变化。

   - Explain why changes occur or don’t occur, considering factors like time of day (e.g., network congestion in the evening).考虑一天中的时间（例如晚上的网络拥塞）等因素，解释为什么发生或不发生变化。

#### **4.3 Bandwidth-Delay Product Calculation4.3 带宽-延迟乘积计算**

1. For each host, calculate the bandwidth-delay product using the formula:对于每个主机，使用以下公式计算带宽延迟乘积： Bandwidth-Delay Product=Bandwidth×Round-trip Time (from ping tests)\text{Bandwidth-Delay Product} = \text{Bandwidth} \times \text{Round-trip Time (from ping tests)}Bandwidth-Delay Product=Bandwidth×Round-trip Time (from ping tests) Convert the result into kilobits.将结果转换为千位。
2. Plot a **bar chart** for each host showing the bandwidth-delay product.为每个主机绘制一个**条形图**，显示带宽延迟乘积。

#### **4.4 Challenges**

- List two major challenges encountered during your experiments, such as:

  列出您在实验过程中遇到的两个主要挑战，例如：

  - **Network congestion**: Multiple users sharing the same network can affect your results.**网络拥塞**：多个用户共享同一网络可能会影响您的结果。
  - **Dynamic set of users**: Fluctuations in network usage may introduce outliers in your data.**动态用户集**：网络使用情况的波动可能会在数据中引入异常值。

- Suggest solutions like running tests during times of low network usage or isolating the device running the tests from other network traffic.建议解决方案，例如在网络使用率较低时运行测试或将运行测试的设备与其他网络流量隔离。

Make sure to include **screenshots** of your results in the appendix as evidence, as required by the project description.请确保按照项目描述的要求在附录中包含结果的**屏幕截图**作为证据。