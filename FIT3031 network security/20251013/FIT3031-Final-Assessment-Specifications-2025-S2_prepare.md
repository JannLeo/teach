


> ❌ 程序在第 1 页因异常停止：InvalidSessionIdException()


---

## 第 1 页

![第 1 页](FIT3031-Final-Assessment-Specifications-2025-S2_assets/page-001.png)

这张截图展示的是 **Monash University（莫纳什大学）课程 FIT3031《Network Security（网络安全）》的期末考核要求**，是一份作业说明文档。下面我会为你详细逐段解释内容含义、注意事项，以及如何在课堂上讲解这一类教学任务。

---

## 一、文档总体介绍

标题部分写明：

> **FIT3031 Network Security Final Assessment**
> **Total Marks 100**
> **Due on Nov 7th, Friday, 11:55 PM**

这意味着这是网络安全课程的**期末作业（Final Assessment）**，满分为 100 分，截止提交时间是 **11 月 7 日晚上 11:55**。
这个文件是学生提交最终作业的重要指南，包含评分、提交要求以及违规处理方式。

---

## 二、第一部分：Overview（概述）

这一部分说明了作业的**学习目标**与**独立性要求**：

> The learning objective of this assignment is for you to gain a first-hand experience on designing, implementing, testing and ethically using an enterprise network.

意思是：这项作业的目标是让学生获得**设计、实现、测试和伦理地使用企业网络的实践经验**。
也就是说，这不是纯理论性任务，而是偏向实践操作（可能涉及虚拟机、GNS3 模拟器等网络工具）。

接着强调：

> This is an individual assignment and you are not allowed to discuss any aspect of it with others (excluding teaching team members).

表示这是**个人作业**，学生**不得与其他同学讨论或分享任何作业内容**（但可以向老师或助教咨询）。

文中还提到学术诚信：

> Failing this requirement ... will result in penalties in accordance with the University’s Academic Integrity guidelines

这里警告学生，违反独立完成的规定会按照莫纳什大学的学术诚信政策受到处罚（提供了学校相关链接）。

**课堂讲解提示**：

* 可以强调学术诚信的重要性。
* 举例说明什么算违规（如私下共享配置文件、互相抄袭网络拓扑等）。
* 说明老师如何验证独立完成（比如通过 hash 验证项目文件）。

---

## 三、第二部分：Submission Policy（提交政策）

这一部分是最关键的作业操作说明，讲述提交文件格式、文件内容、命名规范和视频演示要求。

### (1) 文件命名规范

> Name your files in the format: \[Your Name]-\[Student ID]-FIT3031-FA

例如：
`JohnSmith-31234567-FIT3031-FA.pdf`
`JohnSmith-31234567-FIT3031-FA.mp4`

统一命名便于助教批改和识别。

---

### (2) 主提交内容（Main submission）

学生需要提交两个主要文件：

1. **一份 PDF 报告**（描述自己完成的内容、过程、截图和观察结果）；
2. **一段视频文件**（演示关键任务的实现过程）。

---

### (3) Project Hash（项目哈希验证）

这部分是网络安全作业的一个**防作弊机制**。

要求学生：

* 将 GNS3（网络模拟软件）的项目文件目录打包压缩；
* 生成一个 **SHA1 哈希值**；
* 并将该哈希输出包含在报告第一页。

命令如下：

```bash
cd /opt/gns3/projects/
tar -czvf <ProjectName>.tar.gz <ProjectName>
sha1sum <ProjectName>.tar.gz
```

解释：

* `tar -czvf`：将项目压缩为 tar.gz 文件；
* `sha1sum`：生成哈希值（验证文件唯一性）；
* 报告第一页要写出生成的哈希字符串；
* **不要删除该 tar.gz 文件**，老师可能会要求核验。

**教学建议**：

* 在课堂中可现场演示这三条命令的作用；
* 讲解“哈希”的安全意义（文件验证、防止伪造等）。

---

### (4) 视频提交要求

所有演示视频要合成为**一个单独的视频文件**，并且：

* 在视频中要**清楚显示正在解决的问题编号**；
* 可通过插入文字或语音说明，如“Q1 - Firewall Configuration”。

**目的**：让批改老师能清楚看到视频对应哪道题。

---

## 四、重要说明与扣分规则（Important notes and penalties）

这一部分讲的是常见失分点：

1. **视频文件必须能在普通 Windows 电脑上播放**（不能用需要专门软件的格式，如 `.mov`、`.mkv` 等）。
2. **视频与报告总大小不能超过 500 MB**。
3. **图像、文字、语音必须清晰可辨，且使用英语**。
4. **如视频无法播放，则直接零分**。
5. **可以先上传草稿版（draft submission）**，检查能否正常打开再正式提交。
6. **一旦最终提交，就不能修改。**

**课堂讲解要点**：

* 强调检查视频格式（推荐 `.mp4`），以及分辨率、声音质量；
* 教学生如何在 Moodle 上做 “draft submission”；
* 演示如何合并多个视频任务；
* 提醒学生文件大小控制技巧（如使用 HandBrake 压缩）。

---

## 五、总结与教学重点提示

| 教学重点 | 内容                      |
| ---- | ----------------------- |
| 作业目标 | 学生独立设计并验证一个企业网络环境       |
| 工具   | GNS3 模拟器、Linux 命令行      |
| 提交内容 | PDF 报告 + 演示视频 + 哈希输出    |
| 技术重点 | 网络拓扑搭建、防火墙配置、哈希验证、安全测试  |
| 纪律要求 | 严禁抄袭、讨论，确保学术独立性         |
| 常见问题 | 视频打不开、文件命名错误、哈希忘写、大小超限等 |

---

是否希望我帮你把这份说明转写成一份可直接用于**课堂讲解PPT讲稿（含分段提纲与讲解要点）**？这样你上课时可以直接使用或投影讲解。


---

## 第 2 页

![第 2 页](FIT3031-Final-Assessment-Specifications-2025-S2_assets/page-002.png)

非常好，这张截图是 **Monash University FIT3031《Network Security（网络安全）》期末考核说明文档的第 2 页**，主要讲述了学生在**录制演示视频**和**提交作业**时的详细要求、评分标准、迟交惩罚、视频技术规格等。
下面我会为你系统地拆解每个部分的内容和教学重点，你可以直接据此讲课或制作讲义 / PPT。

---

## 一、关于提交状态（Submission Status）

> **Note that draft files are NOT accepted and will not be marked.**

意思是：“草稿文件不会被评分”。
学生必须在 Moodle 上\*\*点击“Submit for grading”（提交评分）\*\*才能算正式提交。
如果文件只是“草稿状态（draft）”，系统不会算作提交。

另外：

> Otherwise, standard late submission penalty will apply.

如果学生没及时完成正式提交，则会被算作迟交。

**课堂讲解要点：**

* Moodle 平台有 “Save draft” 和 “Submit for grading” 两种状态；
* 老师评分只会看正式提交状态；
* 迟交惩罚会自动计算（系统不会因为学生“误操作”而豁免）。

---

## 二、录制开头要求（Identity Verification）

> At the beginning of your recording, you must clearly show your face and have your photo ID...

学生必须在视频开头：

1. **出示带照片的学生证（Monash ID Card）**；
2. **露出本人面部**；
3. 确保信息清晰可辨。

文档给出了一个示例幻灯片（Figure 1）：

```
FIT3031 - Assignment 1
202X Semester 2
Firstname Lastname – Student ID
Your Monash ID Card
```

学生在期末提交时应改为：

> “Final Assessment” instead of “Assignment 1”

**课堂讲解要点：**

* 演示视频要包含身份验证；
* 可以解释学校为什么要求这样：防止代做、学术不端；
* 要确保视频分辨率足够高，身份证清晰；
* 提醒学生不要遮挡脸部或模糊不清。

---

## 三、视频中需持续露脸（Continuous Face Visibility）

> A part of the submitted video (at a corner) must clearly show your face at all times.

这要求学生在录制时：

* 屏幕上必须**有一个角落显示自己的人脸画面**（如通过 OBS 或 Zoom 小窗）；
* 如果整段视频都没有露脸，会被直接判定为**无效提交，零分处理**。

**课堂讲解要点：**

* 演示如何用 OBS、Zoom、或 GNS3 自带摄像叠加功能来实现；
* 强调这是学校验证“你确实是本人操作”的关键环节。

---

## 四、迟交规则（Late Submission Penalty）

> Late submissions will incur a 5-point deduction per day.

即每天迟交扣 5 分，例如：

* 迟交 2 天 1 小时 → 扣 15 分；
* 超过 7 天未交 → **零分**。

**课堂讲解要点：**

* 可举例计算：满分 100 分，迟交 3 天变成 85 分；
* 明确：系统自动扣分，教师无法人工豁免；
* 鼓励学生提前导出和上传视频（避免传输超时）。

---

## 五、上传时间与技术考虑（Export & Upload）

> Long export or upload times cannot be accepted as a reason for waiving a late submission penalty.

意思是：学生如果因为视频导出太久或上传太慢导致迟交，不算有效理由。
这是在提醒学生提前预留上传时间。

**教学建议：**

* 告诉学生导出视频需预留 1–2 小时；
* Moodle 上传较慢，最好提前在非高峰时段（如白天）上传；
* 演示如何在导出时压缩视频（如使用 ffmpeg）。

---

## 六、申请延期（Extension / Special Consideration）

> If you require extension or special consideration, refer to this link. No teaching team member is allowed to give you extension.

意思是：

* 任何延期必须通过学校的**官方系统申请**；
* 教师本人不能批准延期；
* 不要私信助教请求“通融”。

**教学提示：**

* 可以现场展示 Monash 的“special consideration”申请流程；
* 强调学生需提供医疗证明或其他合理理由。

---

## 七、视频时长要求（Duration Limit）

> The maximum allowed duration for the recorded video is **20 minutes**.

* 只有**前 20:00 分钟的内容**会被评分；
* 超出部分将被忽略；
* 加速播放视频会被判为无效；
* 使用软件加速（如 1.5x）属于违规，**零分处理**。

**教学要点：**

* 讲解如何控制视频时长；
* 建议提前脚本规划、分段录制；
* 可以示范如何通过剪辑软件查看时长。

---

## 八、设备与替代方案（Devices and Recording）

> If your device does not have a camera ... you can borrow a device from Monash Connect or Library.

学生可以借设备录制视频；但借不到设备不是有效借口。
意思是：**技术问题不能作为延迟或免罚的理由**。

**课堂建议：**

* 提醒学生提前检查摄像头、麦克风；
* 提供录制工具示例（OBS、Zoom、QuickTime、Windows Camera 等）。

---

## 九、视频可分段录制与合并（Video Editing Rules）

> You can create multiple video parts ... combine and submit a single video at the end.

学生可以分多次录制、后期合并成一个视频。
重点是最终视频**必须连贯、清晰、易懂**。

---

## 十、视频质量要求（Quality and Size Limit）

> Blurry, unreadable, or inaudible videos will receive zero marks.
> The maximum video file size allowed for upload on Moodle is **500 MB**.

要求：

* 视频必须清晰、可听；
* 上传文件大小 ≤ 500 MB；
* 如果超过，可以用压缩工具（如 ffmpeg）压缩；
* 压缩后必须保留完整时长与清晰度。

**课堂讲解建议：**

* 实机演示视频压缩命令：

```bash
ffmpeg -i input.mp4 -vcodec libx264 -crf 28 output.mp4
```
* 展示清晰 vs 模糊视频的对比；
* 提醒学生：清晰度比特率要适中（480p 或 720p 即可）。

---

## 十一、课堂讲解总结表

| 主题   | 关键要求                  | 教学建议                             |
| ---- | --------------------- | -------------------------------- |
| 提交状态 | 必须正式提交（非 draft）       | 展示 Moodle 界面“Submit for grading” |
| 身份验证 | 视频开头出示 Monash ID + 露脸 | 可现场示范如何录制                        |
| 持续露脸 | 屏幕角落要有人脸              | 教 OBS 分屏技巧                       |
| 迟交惩罚 | 每天 -5 分，7 天后零分        | 举例说明计算规则                         |
| 视频长度 | 最长 20 分钟，不能加速         | 讲解时间规划                           |
| 视频质量 | 清晰、可听、≤500MB          | 教 ffmpeg 压缩方法                    |
| 延期申请 | 仅能通过官方系统              | 说明不能私下请求                         |
| 技术准备 | 提前录制、导出、上传            | 教学生提前测试                          |

---

是否希望我帮你把这两页（page 1 + page 2）整理成一份**教学用 PPT 提纲（含讲解语句、案例说明和演示建议）**？
那样你可以直接用来讲授“作业规范与学术诚信”专题课。


---

## 第 3 页

![第 3 页](FIT3031-Final-Assessment-Specifications-2025-S2_assets/page-003.png)

非常好，这张截图是 **Monash University（莫纳什大学）FIT3031《Network Security（网络安全）》期末考核说明文档的第 3 页**，内容主要包括两大部分：
👉 **第 3 节：作业场景说明（Scenario for the Assignment）**
👉 **第 4 节：安全网络设计与实现任务（Secure Network Design and Implementation）**

下面我会分部分进行详细讲解，帮助你理解教学要点、作业设计思路和课堂讲授重点。

---

## 一、前导部分：视频演示任务要求（上页延续）

这一页开头部分补充了对**视频录制与演示方式**的要求，强调“必须实时演示任务”而非事后讲述。

### 1️⃣ 现场演示（Live Demonstration）

> All tasks must be live demonstrated instead of explaining an already completed task.

意思是：
学生必须**在视频中亲自操作、实时演示任务过程**，而不是展示事先做好的结果。
例如：要展示网络配置，就应当在视频里执行命令并讲解，而不是只展示配置文件截图。

进一步说明：

* **不能后期配音（no voice-over later on）**；
* **不能照着写好的稿子念（no reading from prepared scripts）**；
* **必须在每个任务开始时明确说明该任务是什么（state the task being carried out）**。

**课堂讲解要点：**

* 强调“过程可见性”与“讲解同步”；
* 可以演示一个对比视频：一个仅展示结果，一个边操作边讲解，让学生理解差别；
* 说明评分重点是“能否清晰展示思路与操作”。

---

### 2️⃣ 软件安装说明

> You are allowed to do that in advance of recording your video.
> You do not need to demonstrate software installation in the video.

意思是：
如果需要安装软件（如 GNS3、Wireshark、MikroTik RouterOS），可以提前完成安装；
**视频里不需要展示安装过程**，只需展示使用与配置操作。

---

### 3️⃣ 可以提前准备但不能照搬（Preparation & Academic Integrity）

> You can do online research in advance, take notes, prepare code, etc.
> But you cannot copy-paste commands without explanation.

允许学生：

* 提前查资料、记笔记；
* 准备命令脚本；
但不允许：
* 直接复制粘贴命令而不解释；
* 演示中不说明命令功能。

**课堂讲解要点：**

* 鼓励学生边演示边解释命令作用；
* 举例对比 “正确讲解方式” vs “错误照搬方式”；
* 强调技术表达能力与理解力。

---

### 4️⃣ 学术诚信警告

> Zero tolerance on plagiarism and academic integrity violations.

一旦发现抄袭或作弊（包括视频伪造），将直接记为零分甚至课程挂科。
大学会通过视频对比与哈希校验检测作弊。

---

## 二、Scenario for the Assignment（作业场景说明）

这一部分是作业的背景设置（仿真任务的“现实场景”）。

> Assume you are a network security engineer ... hired to design and implement a secure network for Monash University.

**情境**：
你是一名网络安全工程师，为 Monash University 设计并实现一个安全网络系统，网络覆盖三个校区：

* Caulfield
* Clayton
* Peninsula

网络包含：

* 服务器（servers）
* 防火墙（firewalls）
* 路由器（routers）
* 客户端（clients）

学生需要用 GNS3（网络模拟软件）完成这一系统的搭建、配置与演示。

---

### 📊 学生分配机制（Primary DC）

> The location of the primary data-center (Primary DC) depends on your student ID.

每个学生被分配到不同的“主数据中心（Primary DC）”，分配方法：

| StudentID mod 3 | Primary DC |
| --------------- | ---------- |
| 0               | Caulfield  |
| 1               | Clayton    |
| 2               | Peninsula  |

算法说明：
学生用自己的学号（Student ID）除以 3，取余数（mod 3）：

* 如果余数是 0 → Caulfield；
* 如果余数是 1 → Clayton；
* 如果余数是 2 → Peninsula。

**示例**：
Student ID = 31234567
31234567 ÷ 3 = 10411522 余 **1** → **Primary DC = Clayton**

---

### 🚨 严格警告：错误分配零分

> If you solve a question based on an incorrect Primary DC value ... you will receive a zero mark.

也就是说：

* 如果学生没有按自己学号正确计算 Primary DC；
* 或者故意选错数据中心完成作业；
则**整个题目即使技术上正确，也记零分**。

**课堂讲解要点：**

* 在课堂上可以示范“取模计算”；
* 让学生练习算自己的 Primary DC；
* 强调评分系统是严格匹配学生身份的。

---

## 三、Secure Network Design and Implementation（网络设计与实现任务）

这是作业的 **第一个技术性任务（占 18 分）**。
学生需使用 GNS3 构建一个跨越三校区的安全网络架构。

---

### 1️⃣ 任务目标（Task Objective）

> This task entails designing and executing a network that spans across the three Monash campuses, utilizing GNS3.

学生需：

* 设计并实现一个虚拟网络；
* 网络必须具备安全架构；
* 校区之间要能安全互联；
* 强调防火墙配置、网络分区（segmentation）、路由策略（routing policies）等安全设计。

---

### 2️⃣ 网络设计原则（Design Guidelines）

> The network’s architecture should prioritize security considerations.

也就是说：

* 网络拓扑应包含安全边界（如防火墙节点）；
* 需防止未经授权访问；
* 校区间通信需使用安全路由；
* 可以使用提供的示例拓扑或自行设计。

---

### 3️⃣ 示例文件下载命令

文档提供了下载“示例配置文件”的命令：

```bash
gdown 1b3obWbVLl9kcOztDuAe-CjG_Csmt1Sx7 ; sudo bash ./install_Monash.sh
```

或备用下载方式（如校园 Wi-Fi 无法使用时）：

```bash
wget https://sniffrun.com/install_Monash.sh --no-check-certificate ; \
sudo bash ./install_Monash.sh
```

> 用户名：admin
> 密码：留空（不需要密码）

**教学重点**：

* 演示 Linux 命令执行；
* 说明命令分为：下载脚本 + 运行脚本；
* 可讲述为什么 Wi-Fi 可能屏蔽 `gdown` 下载（安全防火墙或网络过滤）。

---

### 4️⃣ 可选拓扑设计与资料参考

> You can use your own network topology if you would like.
> Mikrotik documentation can be found here: [https://help.mikrotik.com/docs/](https://help.mikrotik.com/docs/)

说明：

* 示例拓扑只是参考；
* 学生可以自由设计自己的网络结构；
* 推荐阅读 **Mikrotik 官方文档**，理解路由、防火墙配置方法。

---

### 5️⃣ 额外网络前置要求

文末提到：

> Additionally, there are supplementary network prerequisites that must be addressed.

意味着后续页面可能列出额外条件（如 VLAN、VPN、防火墙策略等）。

---

## 四、课堂教学建议总结

| 教学主题   | 内容                   | 教学重点                   |
| ------ | -------------------- | ---------------------- |
| 作业模式   | 实时演示 + 讲解            | 演示如何边讲边操作              |
| 学术诚信   | 零容忍作弊                | 强调哈希验证与视频核验            |
| 作业背景   | 模拟网络工程师任务            | 讲解三校区架构背景              |
| 数据中心分配 | 取模计算 studentID mod 3 | 举例练习，确保正确              |
| 技术内容   | 使用 GNS3 设计安全网络       | 介绍 GNS3、Mikrotik、防火墙基础 |
| 下载配置   | Linux 命令实践           | 教学生命令行执行步骤             |
| 安全重点   | 路由安全、防火墙策略           | 强调安全优先原则               |

---

是否希望我帮你把前三页（你已上传的三张图）整理成一份 **完整授课讲稿提纲 + 讲解语句草稿（适合配 PPT 使用）**？
我可以帮你写出每页讲解时间分配、提问环节建议和教学板书重点。


---

## 第 4 页

![第 4 页](FIT3031-Final-Assessment-Specifications-2025-S2_assets/page-004.png)

非常好，这张截图是 **Monash University（莫纳什大学）FIT3031《Network Security（网络安全）》期末考核说明文档的第 4 页**，内容主要讲述两个部分：

* **第 4 节后半部分：网络设计的详细技术要求（Secure Network Design Details）**
* **第 5 节：BGP（边界网关协议）任务 \[10 分]**

我会为你详细解释这一页每一条要求的意义、背后的教学重点、评分逻辑，以及课堂上可以如何讲解或演示。

---

## 一、Secure Network Design – 技术配置要求（延续第 4 节）

这一部分是对学生如何在 GNS3 中构建安全网络的**详细规范**，是整份作业的技术核心内容，占 18 分中的主要部分。

### 1️⃣ 网络总体结构要求

> • All campuses must have at least one perimeter firewall/router.
> • All campuses must have a Client LAN, each LAN should contain at least one client container.

解释如下：

* 每个校区（Campus）都要有**一个边界防火墙/路由器（Perimeter Firewall/Router）**，负责流量控制与安全策略。

  > * 太好了，这正是期末项目里最核心的一块。我给你一套**可直接用来授课 + 带实验的做法**，同时分别给出 **pfSense/VyOS（GNS3 友好）** 和 **Cisco IOS 路由器（Zone-Based Firewall）** 的实现步骤。你可以任选其一做课堂演示。
  >
  >   ------
  >
  >   # 一、定位：什么是“校区边界防火墙/路由器”
  >
  >   - **位置**：每个 Campus 的互联网出口 / 广域网（WAN）入口处。
  >   - **职责**：
  >     1. **分区（Zones）**：WAN / LAN / DMZ / VPN / Guest / MGMT；
  >     2. **策略**：最小权限、默认拒绝（尤其是 WAN→内部）；
  >     3. **NAT**：内网出网的 PAT、对外发布服务的静态 NAT/端口映射；
  >     4. **VPN**：各校区之间的站点到站点 IPsec、或远程接入；
  >     5. **路由**：与核心交换/上级路由的静态或 OSPF/BGP；
  >     6. **高可用**：双机热备/双链路；
  >     7. **可观测**：日志/Syslog、NetFlow/IPFIX、告警；
  >     8. **反欺骗**：uRPF/反向路由检查、Bogon/RFC1918 过滤。
  >
  >   ------
  >
  >   # 二、基线架构与策略（课上先讲这一张图/表）
  >
  >   **参考拓扑（文字版）**
  >    Internet ⇄ [Perimeter FW/Router] ⇄ Core
  >                   ├─ DMZ
  >                   ├─ LAN
  >                   ├─ Guest/IoT
  >                   └─ VPN (to other campuses)
  >
  >   **默认策略表（讲解“为什么”）：**
  >
  >   - WAN → 任何：**拒绝**（仅放行 VPN 终端口与对外发布的 DMZ 服务端口）
  >   - LAN → WAN：**允许必要**（80/443、NTP、DNS 到内网 DNS、软件更新等），**阻断**直连 SMTP:25、P2P 等
  >   - DMZ ↔ LAN：**默认互拒**；仅允许来自管理网段的 SSH/RDP/备份
  >   - Guest → 仅 Internet（80/443/DNS），**拒绝**访问 LAN/DMZ
  >   - VPN（对端校区子网）↔ LAN：按业务白名单放通
  >   - 反欺骗：在 WAN 阻断 RFC1918/保留地址、启用 uRPF
  >
  >   ------
  >
  >   # 三、GNS3 方案（推荐课堂演示）：pfSense 或 VyOS
  >
  >   ## A) 用 pfSense（图形界面快、学生易跟）
  >
  >   **1. 接口与分区**
  >
  >   - 给 pfSense 增加网卡：`WAN / LAN / DMZ / GUEST / MGMT（可选）`
  >   - 在 *Interfaces* 中为每个接口命名、设 IP；WAN 设默认网关（上联运营商/互联网云）
  >
  >   **2. NAT**
  >
  >   - *Firewall → NAT → Outbound*：改为 **Hybrid/Manual**
  >     - 规则1（PAT）：`LAN/GUEST → WAN` 源 NAT 到 WAN 地址
  >     - 规则2（VPN 豁免）：**Do not NAT** `LAN ↔ 对端校区子网`（避免 VPN 里被 PAT）
  >
  >   **3. 防火墙规则（Firewall → Rules）**
  >
  >   - **WAN**：
  >     - 默认拒绝；
  >     - 允许 `IPsec`（500/4500/ESP）或 `OpenVPN` 端口；
  >     - 若发布 DMZ Web：仅放 `TCP/443` 到 DMZ Web 的 **端口转发**（NAT→Port Forward）
  >   - **LAN**：
  >     - 允许 `已建立/相关`（默认有）；
  >     - 允许出网 `80/443/NTP/内网DNS`，**阻断** `TCP/25`（除非内部邮件网关）；
  >     - 可加“只允许到内网 DNS”，并**阻断**直出 53/853（DNS over TLS）
  >   - **DMZ**：
  >     - 拒绝到 LAN；
  >     - 允许到 WAN 仅必要的更新或上报；
  >     - 允许从管理网段（MGMT）到 DMZ 的 SSH/RDP
  >   - **GUEST**：
  >     - 仅到 WAN 的 80/443/DNS；阻断到 LAN/DMZ
  >
  >   **4. 站点到站点 VPN（两校区示例）**
  >
  >   - *VPN → IPsec*：
  >     - Phase1：对端公网 IP，AES-GCM/PSK 或证书；DPD 打开
  >     - Phase2：`本端 LAN 子网 ↔ 对端 LAN 子网`，勾选 `Install policy`
  >   - 两端对称配置，建立后在 *Status → IPsec* 验证 SA
  >
  >   **5. 动态路由（可选，高阶）**
  >
  >   - *System → Package Manager* 安装 **FRR**；
  >   - FRR 里启 **OSPF** 或 **BGP**，把 `LAN/DMZ` 网段宣告给对端（可走 IPsec 虚拟-Tunnel 口）；
  >
  >   **6. 高可用（可选）**
  >
  >   - 两台 pfSense：启 **CARP VIP**（虚 IP），打开 **pfsync** 同步状态、**XML-RPC** 同步配置；
  >   - 双 WAN 可做故障切换/负载分担（Gateway Group）
  >
  >   **7. 日志与可观测**
  >
  >   - *Status → System Logs → Settings*：配置 **Remote Syslog** 到 SIEM；
  >   - 安装 **softflowd** 输出 NetFlow/IPFIX；
  >   - 用 *Aliases* 维护地址/端口组，便于规则复用
  >
  >   **课堂演示验证点**
  >
  >   - LAN 主机能上网，Guest 不能访问 LAN
  >   - DMZ Web 可从外部访问 443，不能访问 22/3306 等
  >   - 两校区间：仅能互访白名单端口（如 22/443），`ping` 通，`traceroute` 走 IPsec
  >   - 日志里能看到被拒绝与放行记录（抓两条给学生看）
  >
  >   ------
  >
  >   ## B) 用 VyOS（纯命令，开源，和企业路由器思路接近）
  >
  >   > 适合想让学生练命令行的班级；同理也能替换成 RouterOS/FRR。
  >
  >   **基本配置示例（节选，按需改网段/接口名）：**
  >
  >   ```bash
  >   configure
  >   set interfaces ethernet eth0 address '203.0.113.2/30'   # WAN
  >   set interfaces ethernet eth1 address '10.10.0.1/24'     # LAN
  >   set interfaces ethernet eth2 address '10.20.0.1/24'     # DMZ
  >   set protocols static route 0.0.0.0/0 next-hop '203.0.113.1'
  >     
  >   # NAT：LAN/DMZ 出网 PAT
  >   set nat source rule 10 outbound-interface 'eth0'
  >   set nat source rule 10 source address '10.10.0.0/24'
  >   set nat source rule 10 translation address 'masquerade'
  >   set nat source rule 20 outbound-interface 'eth0'
  >   set nat source rule 20 source address '10.20.0.0/24'
  >   set nat source rule 20 translation address 'masquerade'
  >     
  >   # 防火墙：分区+默认拒绝
  >   set firewall name WAN-IN default-action drop
  >   set firewall name WAN-IN rule 10 action accept
  >   set firewall name WAN-IN rule 10 state established enable
  >   set firewall name WAN-IN rule 20 action accept
  >   set firewall name WAN-IN rule 20 protocol udp
  >   set firewall name WAN-IN rule 20 destination port '500,4500'   # IPsec
  >   set firewall name WAN-IN rule 30 action accept
  >   set firewall name WAN-IN rule 30 protocol 50                    # ESP
  >   # 可选：发布 DMZ Web
  >   set firewall name WAN-IN rule 100 action accept
  >   set firewall name WAN-IN rule 100 protocol tcp
  >   set firewall name WAN-IN rule 100 destination address '203.0.113.2'
  >   set firewall name WAN-IN rule 100 destination port '443'
  >     
  >   set firewall name LAN-OUT default-action drop
  >   set firewall name LAN-OUT rule 10 action accept
  >   set firewall name LAN-OUT rule 10 state established enable
  >   set firewall name LAN-OUT rule 20 action accept
  >   set firewall name LAN-OUT rule 20 protocol tcp
  >   set firewall name LAN-OUT rule 20 destination port '80,443'
  >   set firewall name LAN-OUT rule 30 action accept
  >   set firewall name LAN-OUT rule 30 protocol udp
  >   set firewall name LAN-OUT rule 30 destination port '53,123'
  >   set firewall name LAN-OUT rule 40 action drop
  >   set firewall name LAN-OUT rule 40 protocol tcp
  >   set firewall name LAN-OUT rule 40 destination port '25'        # 禁止直连SMTP
  >     
  >   # 绑定方向
  >   set interfaces ethernet eth0 firewall in name 'WAN-IN'
  >   set interfaces ethernet eth1 firewall out name 'LAN-OUT'
  >   set interfaces ethernet eth2 firewall out name 'LAN-OUT'
  >     
  >   # 站点到站点 IPsec（概要）
  >   set vpn ipsec ike-group IKEv2 proposal 1 encryption 'aes256'
  >   set vpn ipsec ike-group IKEv2 proposal 1 hash 'sha256'
  >   set vpn ipsec esp-group ESP proposal 1 encryption 'aes256gcm128'
  >   set vpn ipsec esp-group ESP pfs 'dh14'
  >   set vpn ipsec site-to-site peer 198.51.100.2 authentication mode 'pre-shared-secret'
  >   set vpn ipsec site-to-site peer 198.51.100.2 authentication pre-shared-secret 'YourPSK'
  >   set vpn ipsec site-to-site peer 198.51.100.2 ike-group 'IKEv2'
  >   set vpn ipsec site-to-site peer 198.51.100.2 default-esp-group 'ESP'
  >   set vpn ipsec site-to-site peer 198.51.100.2 local-address '203.0.113.2'
  >   set vpn ipsec site-to-site peer 198.51.100.2 tunnel 1 local prefix '10.10.0.0/24'
  >   set vpn ipsec site-to-site peer 198.51.100.2 tunnel 1 remote prefix '10.30.0.0/24'
  >     
  >   commit; save
  >   ```
  >
  >   ------
  >
  >   ## C) Cisco IOS 路由器（Zone-Based Firewall）示例（节选）
  >
  >   ```cisco
  >   ! 接口与 NAT
  >   int g0/0 description OUTSIDE
  >    ip address 203.0.113.2 255.255.255.252
  >    ip nat outside
  >    ip verify unicast source reachable-via rx  ! uRPF
  >   !
  >   int g0/1 description INSIDE
  >    ip address 10.10.0.1 255.255.255.0
  >    ip nat inside
  >   !
  >   int g0/2 description DMZ
  >    ip address 10.20.0.1 255.255.255.0
  >    ip nat inside
  >   !
  >   access-list NAT permit 10.10.0.0 0.0.0.255
  >   access-list NAT permit 10.20.0.0 0.0.0.255
  >   ip nat inside source list NAT interface g0/0 overload
  >     
  >   ! ZBF：定义 class/policy（放行已建立、常用出网）
  >   class-map type inspect CM-INET
  >    match protocol http https dns ntp
  >   policy-map type inspect PM-IN2OUT
  >    class CM-INET
  >     inspect
  >    class class-default
  >     drop log
  >   !
  >   zone security OUTSIDE
  >   zone security INSIDE
  >   zone security DMZ
  >   !
  >   zone-pair security ZP-IN-OUT source INSIDE destination OUTSIDE
  >    service-policy type inspect PM-IN2OUT
  >   !
  >   ! WAN 入站：默认拒绝，仅放 VPN/发布端口（ACL+自定义 policy）
  >   ip access-list extended WAN-IN
  >    deny   ip 10.0.0.0 0.255.255.255 any      ! RFC1918 反欺骗
  >    permit udp any host 203.0.113.2 eq 500
  >    permit udp any host 203.0.113.2 eq 4500
  >    permit esp any host 203.0.113.2
  >    permit tcp any host 203.0.113.2 eq 443    ! 如需发布DMZ Web
  >    deny   ip any any log
  >   int g0/0
  >    ip access-group WAN-IN in
  >   ```
  >
  >   > IPsec、BGP/OSPF、静态 NAT/端口映射可按需要补充；课堂重点放在 **ZBF 思路** 与 **策略落地**。
  >
  >   ------
  >
  >   # 四、课堂实验设计（与期末录屏强绑定）
  >
  >   **任务清单（学生演示脚本）**
  >
  >   1. 画拓扑（标出 Zones）→ 讲思路
  >   2. 出网 PAT：LAN 主机访问 Internet 成功，Guest 仅 80/443
  >   3. DMZ 发布 Web：外网可访问 443，其它端口拒绝（演示被拒绝日志）
  >   4. 校区 A ↔ 校区 B 建 IPsec：仅白名单端口能通
  >   5. Egress 控制：阻断直连 SMTP（telnet smtp.gmail.com 25 失败）
  >   6. 反欺骗与 Bogon：从 WAN 发 RFC1918 源地址包被挡（抓日志）
  >   7. 日志与监控：把拒绝/放行发到 Syslog，并展示查询
  >   8. （加分）HA：CARP/HSRP/VRRP 切换演示
  >
  >   **评分要点**
  >
  >   - 分区清晰、默认拒绝；
  >   - NAT 与 NAT 豁免正确；
  >   - 规则按“最小权限”编写，并能**解释理由**；
  >   - 能提供**验证证据**（抓包/日志/连通性）。
  >
  >   ------
  >
  >   # 五、易错点与口訣
  >
  >   - **规则顺序很重要**（pfSense 从上到下；Cisco 按匹配顺序）。
  >   - **VPN 要做 NAT 豁免**，否则两端私网被 PAT。
  >   - **不要“允许任何到任何”**，先放 **已建立/相关** 再加白名单。
  >   - **先策略、后配置**：先写“谁到谁、为什么、什么端口、日志怎么打”。
  >
  >   ------
  >
  >   需要我把上面内容做成你可以直接发给学生的 **实验手册（PDF 模板）** 或 **课堂用的 1 页策略图** 吗？我可以把策略表与核对清单整理成讲义版。



> 非常好！你发的这张图是你在 GNS3 里搭的 **多校区网络拓扑图**（Clayton、Peninsula、Caulfield 三个校区），这是你期末项目或教学示范的核心。
>  接下来我教你——**怎么在这张图上正确“加上边界防火墙/路由器（Perimeter Firewall/Router）”**，以及为什么要这么做。
>
> ------
>
> ## 🧭 一、为什么每个校区都要加一个边界防火墙
>
> 1. **每个校区都是一个独立的安全域（Campus Network Segment）**，需要自己控制对外/对内流量。
> 2. **Perimeter Firewall / Router** 负责：
>    - 执行访问控制策略（ACL 或防火墙规则）；
>    - 处理 NAT（校区内部上网、对外发布服务）；
>    - 承担 VPN 终端（各校区之间的安全通道）；
>    - 日志与告警收集（检测攻击或异常流量）。
>
> 所以——每个校区必须有自己的**边界防火墙节点**，位于校区内部网络和“外部网络（通常是 Internet 或校区互联骨干）”之间。
>
> ------
>
> ## 🧩 二、从你的图上看现在的情况
>
> 你现在有三个校区：
>
> - **CLAYTON**
> - **PENINSULA**
> - **CAULFIELD**
>
> 中心节点是 “PENINSULA”，上连 Internet。
>  目前这三个校区都是直接通过路由器互连，没有明确的防火墙设备（也没有 DMZ、NAT 层）。
>
> ------
>
> ## 🛠 三、该怎么加：结构与命名（最标准做法）
>
> ### 1. 每个校区都放一个 “Perimeter Firewall / Router” 节点
>
> 在每个校区内（CLAYTON / PENINSULA / CAULFIELD）添加一个节点，建议命名：
>
> ```
> CLAYTON_FW
> PENINSULA_FW
> CAULFIELD_FW
> ```
>
> 👉 如果你用 pfSense 或 VyOS 镜像，可以直接拖一个出来；
>  若你用 Cisco Router，可以当作防火墙路由器使用。
>
> ------
>
> ### 2. 连接位置
>
> 每个校区的 **FW** 设备要放在 “外部 Internet / 校区骨干” 和 “内部局域网” 之间：
>
> 例如：
>
> ```
> [Internet] ─── [PENINSULA_FW] ─── [PENINSULA LAN Switch / Servers]
>                  │
>                  ├── VPN 到 CLAYTON_FW
>                  └── VPN 到 CAULFIELD_FW
> ```
>
> 再例如 Clayton 校区：
>
> ```
> [PENINSULA_FW] ─── [CLAYTON_FW] ─── [CLAYTON LAN / DNS / SMTP / Clients]
> ```
>
> ------
>
> ### 3. 接口划分建议
>
> 以 **CLAYTON_FW** 为例（pfSense/VyOS 都通用）：
>
> | 接口名      | 作用                       | 示例地址      | 备注                   |
> | ----------- | -------------------------- | ------------- | ---------------------- |
> | WAN         | 外联到 Peninsula/Internet  | 192.168.12.2  | 默认路由指向外部       |
> | LAN         | 内部局域网                 | 10.10.0.1/24  | DHCP、DNS、Client 使用 |
> | DMZ（可选） | 放服务器（DNS、SMTP、Web） | 10.10.10.1/24 | 提供对外服务的安全区域 |
> | VPN         | IPsec 隧道接口（可选）     | N/A           | 与其他校区互联         |
>
> ------
>
> ### 4. 基本安全策略
>
> 你讲课时可以展示或让学生总结：
>
> - WAN → LAN：默认拒绝（仅允许 VPN / 已建立连接）
> - LAN → WAN：允许 HTTP/HTTPS、DNS、NTP，阻断 SMTP
> - DMZ → LAN：拒绝，仅允许管理流量
> - LAN → DMZ：允许访问服务器的业务端口
> - Guest → WAN 仅 80/443
> - Logging & NAT：出网 PAT，日志送 Syslog
>
> ------
>
> ### 5. GNS3 具体操作步骤
>
> 1️⃣ **添加防火墙设备**
>  在左侧设备栏：
>
> - 拖一个 **pfSense**、**VyOS** 或 **Cisco Router** 节点，命名为 `CLAYTON_FW`。
> - 添加两块网卡：WAN、LAN（必要时 DMZ）。
>
> 2️⃣ **连接拓扑**
>
> - WAN 接口连接到校区之间的“骨干路由（PENINSULA / INTERNET 节点）”。
> - LAN 接口连接到校区的交换机或内部服务器。
>
> 3️⃣ **分配 IP 地址**
>  例如（示例）：
>
> ```
> CLAYTON_FW (WAN) = 192.168.12.2/30 → Gateway: 192.168.12.1 (PENINSULA_FW)
> CLAYTON_FW (LAN) = 10.10.0.1/24
> ```
>
> 4️⃣ **设置默认路由**
>
> ```
> 默认路由 → PENINSULA_FW (192.168.12.1)
> ```
>
> 5️⃣ **配置 NAT 和规则**
>  在 pfSense / VyOS / Cisco 中设置：
>
> - LAN → WAN NAT (masquerade / PAT)
> - WAN 默认拒绝
> - 添加允许规则（80/443/DNS）
>
> 6️⃣ **测试连通性**
>
> - 内部客户端 ping 外网 IP（验证 NAT）
> - 从外部 ping 校区服务器（验证拒绝）
> - 建立 VPN 后测试两校区互通
>
> ------
>
> ### 6. 建议你加上的小图标与标注
>
> 你可以在图上：
>
> - 每个校区旁边放一个红色框或防火墙图标 🔥；
>
> - 标上 “Perimeter FW”；
>
> - 标出接口名称（WAN / LAN / DMZ）；
>
> - 用虚线画出 VPN 隧道（Site-to-Site IPsec）；
>
> - 在右上角添加一个图例（Legend）：
>
>   ```
>   🔥 = Perimeter Firewall
>   —— = Internal LAN
>   - - - = VPN Tunnel
>   🌐 = Internet
>   ```
>
> ------
>
> ### ✅ 最后示范（逻辑结构）
>
> ```
>          🌐 INTERNET
>               │
>        ┌──────┴──────┐
>        │             │
>    PENINSULA_FW   (其他VPN或ISP)
>       /      \
>  🔥CLAYTON_FW 🔥CAULFIELD_FW
>   │            │
> LAN/DMZ     LAN/DMZ
> (Clients)   (Servers)
> ```
>
> ------
>
> 要不要我帮你在你这张图的基础上画出一个**加了防火墙的参考拓扑图（带颜色和标注）**？
>  我可以直接生成带图标的示意图，让你上课投屏讲解。你只要告诉我：
>
> - 想用哪种风格（教学简图 / 真实网络拓扑风格）
> - 是否用 pfSense 作为防火墙（或 Cisco 路由器）

* 每个校区内部都要有一个**客户端局域网（Client LAN）**，至少包含一个虚拟客户端容器（如 Ubuntu）。

  > 非常棒 👏！你这张图已经完成了**“每个校区都有独立 Client LAN 并包含客户端主机”** 这一步，只差一点优化就完全符合要求。
  >  我帮你仔细看过了，下面是详细评估和改进建议（你可以直接照着讲给学生听）👇
  >
  > ------
  >
  > ## ✅ 一、你已经完成的部分（做得很对）
  >
  > | 项目                              | 状态 | 说明                                                         |
  > | --------------------------------- | ---- | ------------------------------------------------------------ |
  > | **每个校区都有独立 LAN 交换机**   | ✅    | CLAYTON_CLIENT_LAN、PENINSULA_CLIENT_LAN、CAULFIELD_CLIENT_LAN 已存在。 |
  > | **每个校区都有客户端设备**        | ✅    | CLAYTON_CLIENT-1、PENINSULA-CLIENT-1、CAULFIELD-CLIENT-1 均已连接。 |
  > | **LAN 网段独立**                  | ✅    | 分别是：• CLAYTON: 10.200.10.0/24• PENINSULA: 10.201.10.0/24• CAULFIELD: 10.202.10.0/24 |
  > | **客户端与防火墙/路由器连接正确** | ✅    | 都通过 `_CLIENT_LAN` 交换机接入对应校区主路由。              |
  > | **每个客户端有唯一 IP**           | ✅    | 例如 CLAYTON_CLIENT-1 = 10.200.10.101。                      |
  > | **拓扑清晰，结构符合三校区模型**  | ✅    | 结构分明、逻辑正确，适合用于防火墙与 VPN 测试。              |
  >
  > ------
  >
  > ## ⚙️ 二、你还可以微调的地方（为了更标准化）
  >
  > ### 1️⃣ 增加每个校区的“边界防火墙”节点
  >
  > 目前每个校区（CLAYTON、CAULFIELD、PENINSULA）只有一个**核心路由器**，它既连外部又连内部。
  >  👉 你需要再加一个“Perimeter Firewall / Router”节点（可以用 pfSense、VyOS、Cisco Router），放在每个校区出口处：
  >
  > **示例结构（以 CLAYTON 为例）：**
  >
  > ```
  > INTERNET/ISP ──> CLAYTON_FW ──> CLAYTON 路由器 ──> CLAYTON_CLIENT_LAN
  > ```
  >
  > 这样每个校区的“出入口”才独立、安全策略可控。
  >
  > ### 2️⃣ 内部命名建议
  >
  > - 把校区内部路由器命名为 **Core Router** 或 **Internal Gateway**，防止和边界混淆。
  >    例：`CLAYTON_CORE`、`PENINSULA_CORE`、`CAULFIELD_CORE`
  > - 边界设备命名为 `CLAYTON_FW`、`PENINSULA_FW`、`CAULFIELD_FW`。
  >
  > ### 3️⃣ VPN / 互联拓扑
  >
  > PENINSULA 是中心（Hub），CLAYTON 与 CAULFIELD 为分支（Spokes）。
  >  建议：
  >
  > - 建立三台防火墙间的 **IPsec Site-to-Site VPN**；
  > - PENINSULA_FW 作为中心 Hub，负责 NAT 出网 + VPN 聚合；
  > - CLAYTON_FW、CAULFIELD_FW 各自 NAT 内网并连到 Hub。
  >
  > ### 4️⃣ 客户端优化建议
  >
  > - 若学生机器性能允许，可以换 Ubuntu 容器代替 VPCS，这样能跑 ping、curl、dig 等完整命令。
  > - 若要演示 DHCP，可在每个防火墙 LAN 上开启 DHCP Server，客户端自动获取地址。
  >
  > ------
  >
  > ## 🧪 三、验证你完成 Client LAN 的方法（课堂演示建议）
  >
  > 1️⃣ **验证本地连通性**
  >
  > ```bash
  > ping 10.200.10.1      # ping 本校区防火墙的 LAN 口
  > ```
  >
  > 2️⃣ **跨校区验证（VPN 建好后）**
  >
  > ```bash
  > ping 10.201.10.101    # Clayton → Peninsula
  > ping 10.202.10.101    # Clayton → Caulfield
  > ```
  >
  > 3️⃣ **出网测试**
  >
  > ```bash
  > ping 8.8.8.8
  > curl http://example.com
  > ```
  >
  > 4️⃣ **安全策略验证**
  >
  > - 允许 LAN→WAN HTTP/HTTPS；
  > - 阻止 LAN→WAN SMTP；
  > - DMZ 仅能从 MGMT 网段访问。
  >
  > ------
  >
  > ## 🧱 四、课堂讲解逻辑建议
  >
  > 1. 讲解每个校区的结构：
  >     “这是 CLAYTON 校区，它有防火墙、内部路由器和 Client LAN。”
  >
  > 2. 解释为什么每个校区要分段：
  >     “为了隔离广播域、做访问控制、配置 NAT、分配 DHCP。”
  >
  > 3. 展示 IP 地址规划表：
  >
  >    | 校区      | 防火墙 LAN  | Client IP     | 子网 |
  >    | --------- | ----------- | ------------- | ---- |
  >    | CLAYTON   | 10.200.10.1 | 10.200.10.101 | /24  |
  >    | PENINSULA | 10.201.10.1 | 10.201.10.101 | /24  |
  >    | CAULFIELD | 10.202.10.1 | 10.202.10.101 | /24  |
  >
  > 4. 实时在 GNS3 里 ping 演示。
  >
  > ------
  >
  > ## ✅ 总结
  >
  > 你的拓扑已经完成了 **“每个校区都有 Client LAN 和客户端主机”** 的核心要求，
  >  接下来只要：
  >
  > - 在每个校区入口加一台防火墙设备；
  > - 调整命名结构（Core vs Firewall）；
  > - 建立三校区 VPN；
  > - 完善 NAT 与访问策略，
  >
  > 你就能完成整个 **FIT3031 网络安全期末大作业的核心设计图**。
  >
  > ------
  >
  > 是否需要我帮你在这张拓扑的基础上，画出**加了防火墙节点后的完整标准结构图（教学版）**？
  >  我可以标出每个校区的连接、VPN 隧道、IP 地址规划和流量方向，让你上课直接展示。

**课堂讲解要点**：

* 讲解“perimeter firewall”的作用（保护内部网络免受外部攻击）；
* 在 GNS3 中演示如何为每个 campus 建立防火墙节点与客户端 LAN。

---

### 2️⃣ 网络服务要求

> • The network must have the following servers: DNS, CA (Certificate Authority), SSH, Web and SMTP.

必须具备以下服务器：

* **DNS**：域名解析
* **CA**：证书颁发机构
* **SSH**：远程访问
* **Web**：网页服务
* **SMTP**：邮件服务
* > 非常好的问题！👏
  >  你现在的 GNS3 拓扑已经非常接近完整的“企业级网络架构”，而且你提到的这些服务（DNS、CA、SSH、Web、SMTP）正是 **FIT3031 网络安全大作业** 要求的“核心服务器组件”。
  >  我帮你对照逐一检查——你现在**哪些已经有、哪些还缺、哪些可以优化**。
  >
  > ------
  >
  > ## 🧾 一、任务要求回顾
  >
  > 每个完整校区（或集中式数据中心）必须具备以下五类服务器：
  >
  > | 服务                            | 功能                               | 必须部署在哪里                     | 示例主机名 |
  > | ------------------------------- | ---------------------------------- | ---------------------------------- | ---------- |
  > | **DNS**                         | 内部域名解析、可缓存外部查询       | 建议集中部署在主校区（如 CLAYTON） | `DNS`      |
  > | **CA（Certificate Authority）** | 签发内部 HTTPS/VPN 证书            | 可与 DNS 同区或单独节点            | `CA`       |
  > | **SSH**                         | 提供远程运维访问（跳板机/Bastion） | 一般放在内网安全区                 | `SSH`      |
  > | **Web**                         | 提供 HTTP/HTTPS 网站服务           | 放在 DMZ 区                        | `WEB`      |
  > | **SMTP**                        | 提供邮件收发服务                   | 放在 DMZ 区                        | `SMTP`     |
  >
  > ------
  >
  > ## 🔍 二、你当前拓扑的实际情况（从截图分析）
  >
  > ### ✅ 已存在的服务器
  >
  > | 服务器   | 状态             | 位置                                            | 说明                                         |
  > | -------- | ---------------- | ----------------------------------------------- | -------------------------------------------- |
  > | **DNS**  | ✅ 有             | CLAYTON 校区，连在 DMZ_Switch（10.200.40.0/24） | 命名为 `DNS`，功能正确，连到防火墙 DMZ。     |
  > | **SMTP** | ✅ 有             | CLAYTON 校区 DMZ 区                             | 命名为 `SMTP`，是邮件服务节点。              |
  > | **Web**  | ✅ 有             | CLAYTON 校区 DMZ 区                             | 命名为 `WEB`，提供网站服务。                 |
  > | **SSH**  | ✅ 有             | CLAYTON 校区 Internal_Server_Switch 区          | 命名为 `SSH`，对应远程登录服务。             |
  > | **CA**   | ⚠️ 缺失（未看到） | —                                               | 在拓扑右侧 Node 列中没有 `CA` 节点。应新增。 |
  >
  > ------
  >
  > ## ⚙️ 三、你应该补充的部分
  >
  > ### 🔹 1️⃣ 添加 **CA 服务器（Certificate Authority）**
  >
  > - 作用：为 VPN、防火墙管理、Web/SMTP HTTPS 签发证书。
  > - 建议放置位置：CLAYTON 校区，与 DNS 同级（可共用 DMZ_Switch 或放内部网段）。
  > - 命名：`CA`
  > - IP 示例：`10.200.40.6`（若放 DMZ）或 `10.200.20.6`（若放内部网段）
  > - 系统：可以用轻量 Ubuntu Server + `openssl` 或 `easy-rsa` 搭建。
  >
  > **命令简例（课堂演示可用）：**
  >
  > ```bash
  > sudo apt update
  > sudo apt install easy-rsa -y
  > make-cadir ~/ca
  > cd ~/ca
  > ./easyrsa init-pki
  > ./easyrsa build-ca
  > ```
  >
  > 生成的 `ca.crt`、`ca.key` 可用于：
  >
  > - 签发防火墙 VPN 证书；
  > - 签发内部 HTTPS 服务证书；
  > - 分发到客户端以建立信任。
  >
  > ------
  >
  > ### 🔹 2️⃣ 确认各服务器连接区段正确
  >
  > | 服务             | 所在网段       | 防火墙区域    | 备注                       |
  > | ---------------- | -------------- | ------------- | -------------------------- |
  > | Web / SMTP / DNS | 10.200.40.0/24 | DMZ           | 外部可访问的公开服务       |
  > | SSH / CA         | 10.200.20.0/24 | 内部网（LAN） | 仅管理员或防火墙访问       |
  > | Clients          | 10.200.10.0/24 | Client LAN    | 普通用户上网或访问内部资源 |
  >
  > ------
  >
  > ### 🔹 3️⃣ 确保防火墙策略支持这些服务
  >
  > 在 CLAYTON_FW（或 Internal-Firewall）中添加规则：
  >
  > | 方向      | 源区           | 目标区         | 协议/端口          | 动作 |
  > | --------- | -------------- | -------------- | ------------------ | ---- |
  > | WAN → DMZ | Any → WEB      | TCP 80,443     | 允许               |      |
  > | WAN → DMZ | Any → SMTP     | TCP 25,465,587 | 允许（邮件入站）   |      |
  > | LAN → DMZ | Any → DNS      | UDP/TCP 53     | 允许               |      |
  > | LAN → DMZ | Admin-PC → SSH | TCP 22         | 允许（管理用）     |      |
  > | DMZ → LAN | DMZ → CA       | TCP 443        | 允许（请求签证书） |      |
  > | Default   | All → All      |                | 拒绝（log）        |      |
  >
  > ------
  >
  > ## 🧠 四、课堂讲解建议
  >
  > 讲课时，你可以用这个逻辑带学生理解：
  >
  > 1. **为什么要这些服务器？**
  >    - DNS：让网络能通过域名访问。
  >    - CA：让 VPN/HTTPS 有信任关系。
  >    - SSH：让管理员安全远程维护。
  >    - Web：提供对外服务。
  >    - SMTP：提供内部邮件通信。
  > 2. **为什么这些服务器要分区？**
  >    - DMZ 是“半公开区”，允许外部访问部分服务。
  >    - 内部区（LAN）只允许管理员或认证访问。
  >    - 防火墙负责策略分离。
  > 3. **展示 DMZ 流量控制：**
  >    - 从外网访问 Web（能通）
  >    - 从外网访问 SSH（被拒）
  >    - 从 DMZ Web 访问内部数据库（被拒）
  >
  > ------
  >
  > ## ✅ 五、总结核对清单
  >
  > | 服务 | 是否存在 | 位置         | 建议                 |
  > | ---- | -------- | ------------ | -------------------- |
  > | DNS  | ✅        | CLAYTON DMZ  | 保留                 |
  > | CA   | ❌        | —            | 新建一台 `CA` 服务器 |
  > | SSH  | ✅        | CLAYTON 内部 | 保留                 |
  > | Web  | ✅        | CLAYTON DMZ  | 保留                 |
  > | SMTP | ✅        | CLAYTON DMZ  | 保留                 |
  >
  > ------
  >
  > ## 🔧 下一步建议
  >
  > 1. 新增 **CA** 服务器；
  > 2. 在防火墙上配置规则让内部设备能访问 CA（例如 VPN、防火墙、Web）；
  > 3. 在报告中描述 **“服务器分布与安全区域设计”**，附上表格和示意图。
  >
  > ------
  >
  > 是否希望我帮你画一张图，显示这些服务器分别位于哪个安全区域（LAN / DMZ / WAN）？
  >  那张图可以直接放进你的报告或教学 PPT，用来解释“安全分区设计”。

这些服务共同构成一个完整的企业级安全网络结构。

---

### 3️⃣ 服务器部署位置说明

> • DNS and CA are internal servers; WEB and SMTP are external servers.
> SSH is only accessible for Remote Access VPN users.
> All external servers must be placed in your Primary DC.

意思是：

* DNS、CA：**内部网络使用**（internal servers）；
* WEB、SMTP：**外部可访问服务器**（external servers）；
* SSH：只对**VPN 用户**开放；
* 所有外部服务器（WEB 和 SMTP）都必须部署在学生自己分配的 **Primary DC**。

**教学重点**：

* 解释“内部服务器”和“外部服务器”的安全分层概念；
* 讲述 DMZ（非军事区）结构；
* 强调 SSH 只限 VPN 用户访问，体现访问控制策略。
* > 非常棒，你现在已经理解了这部分核心设计逻辑，这个问题问得**非常关键**，因为它是整个 **FIT3031 网络安全期末实验架构** 的灵魂之一。
  >
  > 我仔细分析了你当前的 GNS3 拓扑（截图），结合“服务器部署位置说明”的要求，下面是**逐项核对 + 教学讲解 + 实现建议**👇
  >
  > ------
  >
  > ## ✅ 一、任务原文核心含义再解释
  >
  > | 类型                               | 定义                             | 示例服务       | 所在安全区域              | 访问策略                               |
  > | ---------------------------------- | -------------------------------- | -------------- | ------------------------- | -------------------------------------- |
  > | **内部服务器（Internal Servers）** | 仅内部网络可访问                 | DNS、CA        | LAN 或内部 Server 网络    | 仅内网主机 / 防火墙可访问              |
  > | **外部服务器（External Servers）** | 提供对外公开服务                 | WEB、SMTP      | DMZ（Demilitarized Zone） | 允许来自 WAN 的访问（80/443、25、465） |
  > | **SSH**                            | 远程管理服务                     | SSH/Bastion    | LAN 或专用 VPN 子网       | 仅允许 VPN 用户访问 TCP/22             |
  > | **Primary DC（主数据中心）**       | 你自己选定的“主校区”，放外部服务 | 通常是 CLAYTON | 托管 DMZ 区的 Web、SMTP   |                                        |
  >
  > ------
  >
  > ## 🧩 二、结合你的拓扑逐项核对
  >
  > ### ✅ 1️⃣ DNS —— 内部服务器 ✔️
  >
  > - 你有一个节点命名为 `DNS`，位于 `CLAYTON` 校区，通过 `DMZ_Switch` 与内部互连。
  > - 按要求，DNS 应该属于 “Internal Server”，而不是对外暴露。
  > - **你的图中 DNS 与 DMZ_Switch 相连 → 可调整。**
  >
  > **建议：**
  >
  > - 把 DNS 改连到 `Internal_Server_Switch`（和 SSH 同区）。
  > - 防火墙上仅允许：
  >   - 内部客户端访问 UDP/TCP 53；
  >   - DMZ/外网禁止访问该 DNS。
  >
  > ✅ 实现后：**满足 “DNS internal only”**。
  >
  > ------
  >
  > ### ⚠️ 2️⃣ CA —— 内部服务器 
  >
  > - 要求中指出 CA 必须为内部服务器，用于签发 VPN、防火墙、Web 证书。
  >
  > **建议：**
  >
  > - 新建一台 `CA` 主机（例如 Ubuntu Server），放置在：
  >
  >   ```
  >   Internal_Server_Switch (10.200.20.0/24)
  >   ```
  >
  > - 典型 IP：`10.200.20.6`
  >
  > - 防火墙规则：仅允许内部防火墙/VPN 网段访问 443（取证书）。
  >
  > ✅ 加上后即可满足 **“CA internal server”**。
  >
  > ------
  >
  > ### ✅ 3️⃣ WEB —— 外部服务器 ✔️
  >
  > - 你已有 `WEB` 节点，放在 `DMZ_Switch (10.200.40.0/24)`。
  > - DMZ 正是“外部服务器区”，位置正确。
  > - 必须通过防火墙规则，允许：
  >   - WAN → WEB: TCP 80,443
  >   - LAN → WEB: TCP 443（内部测试）
  > - 禁止：
  >   - WEB → LAN（防止被攻陷后横向移动）
  >
  > ✅ 完全符合 “external server in DMZ”。
  >
  > ------
  >
  > ### ✅ 4️⃣ SMTP —— 外部服务器 ✔️
  >
  > - 你有一个 `SMTP` 节点，也在 `DMZ_Switch`。
  > - 这正是标准设计（邮件网关 / 外部收发服务）。
  >
  > **建议防火墙规则：**
  >
  > - WAN → SMTP: TCP 25,465,587 允许（对外收信）
  > - LAN → SMTP: TCP 25,465 允许（内网发信）
  > - SMTP → LAN 禁止（除非内部邮件转发）。
  >
  > ✅ 符合 “external server in Primary DC (DMZ)”。
  >
  > ------
  >
  > ### ⚠️ 5️⃣ SSH —— 仅 VPN 用户可访问 ⚙️
  >
  > - 你有一个名为 `SSH` 的节点，位于 `Internal_Server_Switch`，很好；
  > - 但你目前拓扑中 **还没有建立 VPN 子网 / VPN 用户段**。
  >
  > **要实现要求，需要：**
  >
  > 1. 在你的防火墙（建议在 CLAYTON_FW 或 PENINSULA_FW）上配置一个 **Remote Access VPN**：
  >    - 例如 OpenVPN 或 IPsec L2TP；
  >    - 分配 VPN 地址段：`10.250.0.0/24`；
  > 2. 在防火墙上写访问控制策略：
  >    - 仅允许 `10.250.0.0/24 → SSH server (10.200.20.x)` 端口 22；
  >    - 禁止其他源访问 SSH。
  >
  > ✅ 这样 SSH 才能“只对 VPN 用户开放”。
  >
  > **VPN 地址段（10.250.0.0/24）要与内部网络（10.200.x.x）分开，**
  >  是为了：
  >
  > - 避免地址冲突；
  > - 让防火墙能区分 VPN 用户；
  > - 做精确访问控制（只允许 VPN → SSH）。
  >
  > ------
  >
  > ## 🧱 三、Primary DC 检查
  >
  > > “All external servers must be placed in your Primary DC.”
  >
  > - 你当前拓扑的外部服务器（WEB、SMTP）都在 **CLAYTON 校区**；
  > - CLAYTON 显然是你设计的 **主数据中心（Primary DC）**；
  >    ✅ 已满足要求。
  >
  > ------
  >
  > ## 🧠 四、教学讲解重点（你可以这样讲给学生）
  >
  > ### 🔹 概念讲解逻辑
  >
  > 1. **安全分层（Security Zones）**
  >
  >    - Internal Zone：受信任区（DNS、CA、SSH）
  >    - DMZ Zone：半公开区（WEB、SMTP）
  >    - External Zone：不受信任（Internet）
  >
  > 2. **访问控制示意**
  >
  >    ```
  >    Internet → [Firewall] → DMZ (WEB, SMTP)
  >                           ↓
  >                         Internal (DNS, CA)
  >    VPN Users → SSH (only via VPN tunnel)
  >    ```
  >
  > 3. **Primary DC 概念**
  >
  >    - 每个学生选一个校区作为主数据中心；
  >    - 所有对外服务集中部署，方便统一防护与审计。
  >
  > 4. **防火墙规则思路**
  >
  >    - 默认拒绝；
  >    - 允许必要通信；
  >    - 明确方向（source/destination zone）。
  >
  > ------
  >
  > ## ✅ 五、总结核对表
  >
  > | 服务 | 应在区域                | 你现在的状态            | 是否达标   | 改进建议                    |
  > | ---- | ----------------------- | ----------------------- | ---------- | --------------------------- |
  > | DNS  | Internal                | 在 DMZ（应调整）        | ⚠️ 部分达标 | 移至 Internal_Server_Switch |
  > | CA   | Internal                | 无                      | ❌          | 新增 CA 节点                |
  > | WEB  | External (DMZ)          | ✅ 在 DMZ                | ✅          | 保持                        |
  > | SMTP | External (DMZ)          | ✅ 在 DMZ                | ✅          | 保持                        |
  > | SSH  | Internal，仅 VPN 可访问 | ✅ 在 Internal，但缺 VPN | ⚠️ 部分达标 | 配置 Remote Access VPN      |
  >
  > ------
  >
  > ## 🚀 六、下一步建议
  >
  > 1. **调整 DNS 位置 + 新建 CA 节点；**
  > 2. **在防火墙添加 VPN（OpenVPN/IPsec Remote Access）；**
  > 3. **配置访问控制：**
  >    - 仅 VPN 用户能访问 SSH；
  >    - 内网主机能访问 DNS/CA；
  >    - 外网主机只能访问 Web/SMTP；
  > 4. **验证：**
  >    - 通过 VPN 登录 SSH ✅；
  >    - 直接从 Internet 登录 SSH ❌；
  >    - Web/SMTP 外部可达 ✅；
  >    - 内部主机可正常解析域名 ✅。
  >
  > ------
  >
  > 要不要我帮你画一张 **安全分区示意图（Internal / DMZ / VPN / External）**？
  >  这张图可以直接放进你的报告或课堂 PPT，一眼看出各服务器的安全分层和访问路径。

---

### 4️⃣ 额外的外部节点

> • Add two Ubuntu containers named External-Attacker and External-Client.

这两台容器代表：

* **External-Attacker**：外部攻击者节点（用于后面 BGP 攻击任务演示）；
* **External-Client**：外部普通用户节点。

---

### 5️⃣ 子网划分与防火墙分配

> • Assign different subnets to campuses and configure perimeter firewalls/routers.

每个校区必须使用不同的子网（Subnet），并在防火墙中配置路由策略。

课堂中可以讲解：

* 为什么不同区域要用不同子网（隔离风险、简化管理）；
* 在 GNS3 中如何设置防火墙的 IP 路由规则。

---

### 6️⃣ 各服务器配置要求

#### SSH 服务器

> • Open OpenSSH on a regular Ubuntu container.
> 说明：使用 Ubuntu 的 OpenSSH 服务即可，不需要专门镜像。

#### DNS / WEB / SMTP / CA 服务器

> • Use any open-source server, e.g., OpenSSL for CA.
> • Web server should host a web page showing your Student ID.
> • DNS can forward to Google DNS.

* DNS 可以是转发服务器（Forwarding Server）；
* CA 可使用 OpenSSL 工具生成证书；
* Web 页面要显示学生学号（用于防抄袭识别）。

#### Web 与 SMTP 加密

> • WEB server should use TLS with certificates issued by the CA.
> • SMTP server must enforce encryption with STARTTLS or SMTPS.

意味着：

* Web 必须使用 HTTPS；
* 邮件服务器必须启用加密通信；
* 证书由自己搭建的 CA 签发；
* 域名需包含学生 ID，例如：
`111222333.com`。

> 非常好，Chloe 👏
>  这部分正是你同学（甚至助教）最容易迷糊的地方 ——
>  **“怎么在 GNS3 里让这些服务器真正跑起来”**。
>  你现在拓扑已经很标准了（每台服务器都放在正确的子网），
>  接下来只要在这些服务器容器里**安装配置对应的服务**即可。
>
> 下面我给你一个 **完整可上课讲解 + 可操作的步骤表**，
>  你可以直接带学生一步步做，所有命令都是在 Ubuntu Server 容器里执行的。
>
> ------
>
> ## 🧱 一、准备：确认你用的是 Ubuntu 容器（不是 VPCS）
>
> - 打开 GNS3 → 从左侧拖 **Ubuntu Container** 到拓扑（例如 `WEB`, `DNS`, `CA`, `SSH`, `SMTP`）。
>
> - 确认能进入终端（命令行），显示类似：
>
>   ```
>   root@WEB:~#
>   ```
>
> - 如果不能联网更新包，请在 GNS3 的“Cloud”节点桥接到宿主机网络（或用本地镜像离线安装）。
>
> ------
>
> ## 🧩 二、SSH 服务器配置（SSH）
>
> ### 🔹 目的
>
> 让远程 VPN 用户或管理员通过 SSH 登录校区内部。
>
> ### 🔹 操作步骤
>
> ```bash
> # 更新软件库
> sudo apt update
> 
> # 安装 OpenSSH 服务
> sudo apt install openssh-server -y
> 
> # 启动服务
> sudo systemctl enable ssh
> sudo systemctl start ssh
> 
> # 查看状态
> sudo systemctl status ssh
> ```
>
> ### 🔹 验证
>
> 在另一台容器（或笔记本）上：
>
> ```bash
> ssh user@10.200.20.4
> ```
>
> > 其中 `10.200.20.4` 是你的 SSH 容器 IP。
> >  如果显示 “login as:” 就成功了。
>
> ------
>
> ## 🌐 三、DNS 服务器配置（DNS）
>
> ### 🔹 目标
>
> 让内部主机（Client / Server）通过本地 DNS 解析域名。
>  DNS 服务器转发请求到 Google DNS (8.8.8.8)。
>
> ### 🔹 操作步骤
>
> ```bash
> sudo apt update
> sudo apt install bind9 -y
> ```
>
> 编辑主配置文件：
>
> ```bash
> sudo nano /etc/bind/named.conf.options
> ```
>
> 修改为以下内容：
>
> ```bash
> options {
>     directory "/var/cache/bind";
> 
>     forwarders {
>         8.8.8.8;
>         8.8.4.4;
>     };
> 
>     allow-query { any; };
>     recursion yes;
> };
> ```
>
> 保存并重启服务：
>
> ```bash
> sudo systemctl restart bind9
> sudo systemctl enable bind9
> ```
>
> ### 🔹 验证
>
> 在 Client 容器执行：
>
> ```bash
> nslookup www.google.com 10.200.20.2
> ```
>
> 若能返回解析结果，则 DNS Forwarder 正常。
>
> ------
>
> ## 💻 四、Web 服务器配置（WEB）
>
> ### 🔹 目标
>
> 提供网页，网页上显示学生学号，用于防抄袭验证。
>
> ### 🔹 操作步骤
>
> ```bash
> sudo apt update
> sudo apt install apache2 -y
> ```
>
> 创建自定义主页：
>
> ```bash
> echo "<h1>FIT3031 - Student ID: 31234567</h1>" | sudo tee /var/www/html/index.html
> ```
>
> 启动服务：
>
> ```bash
> sudo systemctl enable apache2
> sudo systemctl start apache2
> ```
>
> ### 🔹 验证
>
> 从任何内网主机访问：
>
> ```
> curl http://10.200.40.2
> ```
>
> 应输出你的学号网页。
>
> 或在浏览器输入：
>
> ```
> http://10.200.40.2
> ```
>
> ------
>
> ## 📧 五、SMTP 邮件服务器（SMTP）
>
> ### 🔹 目标
>
> 让 DMZ 区有一个能接收邮件的开放端口（用于演示）。
>
> 你可以使用轻量 **Postfix** 服务。
>
> ### 🔹 操作步骤
>
> ```bash
> sudo apt update
> sudo apt install postfix -y
> ```
>
> 安装时选择：
>
> - “Internet Site”
> - System mail name: `mail.clayton.local`
>
> 修改配置文件：
>
> ```bash
> sudo nano /etc/postfix/main.cf
> ```
>
> 确认以下内容：
>
> ```bash
> myhostname = mail.clayton.local
> myorigin = /etc/mailname
> mydestination = $myhostname, localhost.localdomain, localhost
> inet_interfaces = all
> inet_protocols = ipv4
> ```
>
> 重启服务：
>
> ```bash
> sudo systemctl restart postfix
> sudo systemctl enable postfix
> ```
>
> ### 🔹 验证
>
> 在任意客户端执行：
>
> ```bash
> telnet 10.200.40.3 25
> ```
>
> 出现：
>
> ```
> 220 mail.clayton.local ESMTP Postfix
> ```
>
> 即表示 SMTP 工作正常。
>
> ------
>
> ## 🔐 六、CA 证书颁发机构（CA）
>
> ### 🔹 目标
>
> 创建一个简单的内部 CA，用来签发 HTTPS / VPN 证书。
>
> ### 🔹 安装与初始化
>
> ```bash
> sudo apt update
> sudo apt install openssl -y
> mkdir ~/CA
> cd ~/CA
> mkdir certs newcerts private
> chmod 700 private
> touch index.txt
> echo 1000 > serial
> ```
>
> ### 🔹 生成根 CA 密钥与证书
>
> ```bash
> openssl genrsa -aes256 -out private/ca.key.pem 4096
> openssl req -x509 -new -nodes -key private/ca.key.pem -sha256 -days 3650 -out certs/ca.cert.pem
> ```
>
> 填写信息时：
>
> - Common Name: `CLAYTON-CA`
> - Country, Org 随意
>
> CA 文件：
>
> - 私钥：`private/ca.key.pem`
> - 证书：`certs/ca.cert.pem`
>
> 这两个文件可以发给 Web / VPN / SMTP 用来签发服务端证书。
>
> ### 🔹 验证
>
> ```bash
> openssl x509 -in certs/ca.cert.pem -text -noout
> ```
>
> 输出 CA 详情即成功。
>
> ------
>
> ## 🧠 七、课堂讲解重点建议
>
> | 服务 | 学生要理解的重点 | 教师讲解关键词                              |
> | ---- | ---------------- | ------------------------------------------- |
> | SSH  | 远程管理入口     | “VPN 登录后才可访问”                        |
> | DNS  | 内部域名解析     | “内部服务器查本地名，外部转发到 Google DNS” |
> | Web  | 对外服务         | “页面显示学号验证身份”                      |
> | SMTP | 对外通信         | “演示邮件协议与 DMZ 设计”                   |
> | CA   | 安全信任根       | “签发 VPN 与 HTTPS 证书”                    |
>
> > 🎯 强调教学逻辑：
> >
> > - 这些服务器都在 **CLAYTON 校区**；
> > - 分区部署：
> >   - DMZ → Web、SMTP（外部）
> >   - Internal → DNS、CA、SSH（内部）
> > - 体现安全域隔离思想。
>
> ------
>
> ## ✅ 八、总结核对表（你课堂可发给学生）
>
> | 服务 | 软件包           | 关键配置文件                   | 验证命令                                   |
> | ---- | ---------------- | ------------------------------ | ------------------------------------------ |
> | SSH  | `openssh-server` | `/etc/ssh/sshd_config`         | `ssh localhost`                            |
> | DNS  | `bind9`          | `/etc/bind/named.conf.options` | `nslookup www.google.com`                  |
> | Web  | `apache2`        | `/var/www/html/index.html`     | `curl localhost`                           |
> | SMTP | `postfix`        | `/etc/postfix/main.cf`         | `telnet localhost 25`                      |
> | CA   | `openssl`        | `~/CA` 目录                    | `openssl x509 -in certs/ca.cert.pem -text` |
>
> ------
>
> ## 💡 九、额外加分点（想拿高分可讲）
>
> - Web 页面使用 HTTPS（用你 CA 签发的证书）；
> - DNS 增加内部域名（如 web.clayton.local）；
> - SMTP 配合防火墙规则，只允许出站 TCP 25；
> - SSH 只允许来自 VPN 子网登录（通过防火墙规则控制）。
>
> ------
>
> 是否希望我帮你生成一份配套的 **教学讲义模板（Markdown / Word 格式）**，
>  里面直接列出每台服务器的安装命令、截图占位和验证命令？
>  这样你可以直接发给学生作为“实验指导书”。

---

### 7️⃣ 网络连通性与验证

> • At this stage all devices should be able to reach each other and all services should be active.

学生完成此部分时：

* 所有节点间应能互通；
* 所有服务（DNS、Web、SMTP、SSH）必须正常运行。

---

## 二、4.1 Submission Requirement（提交要求）

分为两个部分：**Video** 与 **Report**。

### 🎥 Video（演示视频要求）

> Video should demonstrate access to DNS, WEB, SMTP and SSH services from a different campus.

学生需录制视频展示：

* 从另一个校区访问这些服务；
* 展示 HTTPS、SMTP、SSH 的加密通信；
* 可以使用工具如：

* `Lynx`（命令行浏览器）
* `OpenSSL s_client`
* `dig`
* `Wireshark`（验证加密流量）

**课堂讲解要点：**

* 演示 Wireshark 抓包查看加密数据；
* 解释 HTTPS 与 STARTTLS 的握手过程；
* 指导学生如何在视频中说明每个实验步骤。

---

### 🧾 Report（书面报告要求）

> Report should include a screenshot of the network topology (GNS3), IP subnets, IP addresses of all nodes, and name of your Primary DC.

报告应包含：

* GNS3 拓扑截图；
* 子网与 IP 地址；
* 各节点配置表；
* 明确标明学生的 Primary DC 名称；
* 所有截图需清晰且完整。

---

## 三、第五节：BGP（边界网关协议）\[10 分]

* 这是期末作业里 **BGP 专题（10 分）** 的任务说明。它要求你用 BGP 把三个校区的“边界防火墙/路由器”互联、做一次**前缀劫持（prefix-hijacking）攻击演示**，再从受害方做一个**临时反制**并用抓包/trace 证明流量方向发生了变化。下面给你能直接上课讲、也能照做的流程（我用你拓扑举例：CLAYTON=主数据中心 Primary DC，另两个是分校区）：

  ------

  # 任务在说什么（白话版）

  1. **每个校区=一个 BGP AS**
      例如：CLAYTON/Primary-DC=AS **65020**，PENINSULA=AS **65010**，CAULFIELD=AS **65030**。
      各校区防火墙把“直连的内部网段”（LAN/DMZ 等）**通过 BGP network 宣告**出去。

  2. **做一次前缀劫持（5 分）**
      从**非 Primary DC** 的任意防火墙（如 CAULFIELD 或 PENINSULA）发动攻击：

     - 伪装/宣告 **更具体的前缀**（Longest-Prefix-Match 会获胜），把原本发往 Primary-DC 的流量**吸走**。
     - 在视频里用 `traceroute`/Wireshark 证明路径改变（流量没走到 Primary-DC，而被你“劫持”的校区收走）。

  3. **临时反制（5 分）**
      只在**受害的 Primary-DC** 防火墙上做**临时**措施把流量拉回：最简单可行的是**再宣告更更具体的子网**（把自己的 /24 拆成两个 **/25**），立刻赢回最优路径，并用抓包证明路径回正。

     > 注：真正工程上会做**前缀过滤/ROA/RPKI/邻居入站 prefix-list**等，但这些通常涉及对端配置；题目强调“temporally fight back from the victim firewall”，所以课堂上采用“更具体前缀”是最直观的现场反制。

  4. **注意**
      题目建议**先做 BGP 任务**，以免被 VPN/复杂防火墙规则干扰。做完**记得还原**配置再做后续题。

  ------

  # 教学与实操：一步步做

  下面给 **VyOS/FRR（pfSense 装 FRR 也同理）** 的示例。把 IP/网段换成你图里的：

  - Primary-DC（CLAYTON）对外公布：`10.200.20.0/24`（Internal-Servers），`10.200.40.0/24`（DMZ）。
  - 邻接关系：各校区之间通过 ISP/中心交换建立 eBGP 邻居。

  ## 1) 基础 BGP（每个校区都要完成）

  ### 以 **Primary-DC（CLAYTON_FW，AS65020）** 为例

  ```bash
  configure
  set protocols bgp 65020 neighbor 192.168.122.201 remote-as 65010   # PENINSULA
  set protocols bgp 65020 neighbor 192.168.122.202 remote-as 65030   # CAULFIELD
  set protocols bgp 65020 network 10.200.20.0/24    # Internal servers
  set protocols bgp 65020 network 10.200.40.0/24    # DMZ
  commit; save
  ```

  ### 以 **PENINSULA_FW（AS65010）**

  ```bash
  configure
  set protocols bgp 65010 neighbor 192.168.122.200 remote-as 65020
  set protocols bgp 65010 neighbor 192.168.122.202 remote-as 65030
  # 宣告本校区网段，例如：
  set protocols bgp 65010 network 10.201.10.0/24
  commit; save
  ```

  ### 以 **CAULFIELD_FW（AS65030）**

  ```bash
  configure
  set protocols bgp 65030 neighbor 192.168.122.200 remote-as 65020
  set protocols bgp 65030 neighbor 192.168.122.201 remote-as 65010
  set protocols bgp 65030 network 10.202.10.0/24
  commit; save
  ```

  **验证：**

  ```
  show ip bgp summary
  show ip bgp
  ```

  确保每台都学到对方的前缀（能看到 10.200.20.0/24、10.200.40.0/24 等）。

  ------

  ## 2) 演示“前缀劫持”（5 分）

  选择**非 Primary-DC** 的一台（例如 **CAULFIELD_FW / AS65030**）执行：

  **思路：** 劫持 **10.200.20.0/24**（真实属于 Primary-DC）的方法有两种：
   A. **宣告更具体前缀**（推荐，最直观）：例如 `10.200.20.0/25` 和 `10.200.20.128/25`；
   B. 宣告同等前缀但让**AS_PATH 更短**（不稳定且受其他策略影响）。

  课堂上用 **A 方案**：

  ```bash
  configure
  # 恶意（或误配）地宣告受害者网段的两个更具体子网
  set protocols bgp 65030 network 10.200.20.0/25
  set protocols bgp 65030 network 10.200.20.128/25
  commit; save
  ```

  **效果：** 其他校区路由器会因为“最长前缀匹配”而更倾向去往 **CAULFIELD**，
   此时从 PENINSULA/外部访问 `10.200.20.x` 的流量会被**重定向到 CAULFIELD**（即被你“劫持”）。

  **在视频里证明：**

  - 攻击前后分别 `traceroute 10.200.20.5`（例如 DNS/CA/SSH 任一主机）
  - 或在边界抓包（Wireshark/tcpdump）展示下一跳变化。

  ------

  ## 3) 受害方临时反制（5 分）

  只改 **Primary-DC（CLAYTON_FW / AS65020）**，不触碰对端：

  ```bash
  configure
  # 受害者也宣告两个 /25（比被劫持者“同级”，但因为你是正主，邻居可能优选直连/更短AS_PATH）
  set protocols bgp 65020 network 10.200.20.0/25
  set protocols bgp 65020 network 10.200.20.128/25
  commit; save
  ```

  很多情况下，邻居将**首选来自真正源头**的 /25（AS_PATH 更短/更可信，且你的邻接关系直连）。
   如果仍未收回，可在**被劫持者**那里撤销其 /25；你的视频可先演示“正主发布 /25 后路径回正”，再演示“撤销攻击 /25 后完全恢复”。

  **撤销（还原环境）：**

  ```bash
  # 攻击端（CAULFIELD）撤销劫持
  delete protocols bgp 65030 network 10.200.20.0/25
  delete protocols bgp 65030 network 10.200.20.128/25
  commit; save
  
  # 受害端（CLAYTON）按需保留或也撤销 /25
  ```

  **视频里证明回正：**

  - 再次 `traceroute`，路径回到 Primary-DC；
  - Wireshark 看到流量下一跳恢复。

  ------

  ## 4) 课堂可补充的“工程级”防御（说概念即可）

  - **入站前缀过滤（prefix-list/route-map）**：只接受对端应当宣告的前缀；
  - **RPKI/ROA 验证**：带 `valid/invalid` 的路由验证；
  - **max-prefix** 限制；**BGP community** 约束传播；
  - **AS-PATH 过滤**、uRPF、监控告警。

  ------

  # 评分点怎么卡住就怎么演

  1. **BGP 成功互联**（每个 AS 宣告自身网段，邻居能学到）。
  2. **从“非 Primary-DC”发动劫持**（宣告更具体前缀，证明路径改变）。
  3. **受害方临时反制**（宣告更更具体或收回对端劫持，证明路径恢复）。
  4. **全程有抓包/trace 佐证 + 口头解释“为什么变了”**。
  5. **演示后恢复现场**（删除临时 network，回到干净拓扑）。

  ------

  如果你要，我可以把上述命令按你实际 IP/AS 直接替换成**一键脚本清单**（分三台防火墙），上课照抄就能跑；也能给你一页**BGP 攻防流程图**放 PPT。


---

## 第 5 页

![第 5 页](FIT3031-Final-Assessment-Specifications-2025-S2_assets/page-005.png)

非常好，这张截图是 **Monash University FIT3031《Network Security（网络安全）》期末考核说明文档的第 5 页**，这一页的内容非常关键，主要涵盖了网络安全设计中的**VPN配置、BGP路由攻击防御演示要求、以及防火墙配置任务**，是学生实践操作与安全机制理解的核心部分。
下面我将为你逐段详细解释其含义，并提供课堂讲解思路。

---

## 一、延续上页内容：5.1 Submission Requirement（第5章报告与提交要求）

### 🔹 视频要求（Video）

> Recording of the demonstration of the attack and the fight back.

意思是：学生需要录制视频，演示：

1. BGP攻击的发生过程（prefix hijacking）；
2. 防御措施的实施与效果（fight back）。

### 🔹 报告要求（Report）

> N/A
> 即：这部分任务（第5章）**不需要提交文字报告**，只要视频演示即可。

---

## 二、6. VPN（22分）

这是本次作业中分值较高的部分，目的是让学生通过**IPSec VPN**建立三校区间的安全通信网络。

---

### 6.1 Site-to-Site VPNs（校区间VPN连接）

> Your objective is to establish VPN tunnels using IPSec with ESP between the three campuses...

**目标：**

* 在三个校区之间建立 **IPSec 隧道（tunnel）**；
* 使用 **ESP（Encapsulating Security Payload）** 进行数据加密；
* 构建一个“**全互联的网状VPN拓扑（mesh topology）**”。

**核心思想：**

* 每个校区之间的通信（如文件传输、路由信息）必须加密；
* 目的是确保**跨校区通信安全**，防止数据被窃听或篡改。

**课堂讲解建议：**

* 展示 IPSec VPN 的逻辑结构图（三节点互连）；
* 讲解 ESP 协议在加密数据包时如何保护机密性与完整性；
* 可让学生用 Wireshark 抓包展示加密效果（ESP 无法直接读取明文）。

---

### 6.2 Remote Access VPNs（远程访问VPN）

> Create a Remote Access IPSec VPN on the Primary DC...

**任务要求：**

* 在主数据中心（Primary DC）上创建远程访问VPN；
* 让远程用户（如外部员工或学生）通过VPN访问内部网络；
* 只允许访问主数据中心内部子网；
* 其他流量走普通网络（即**split tunneling 分离隧道模式**）。

**示例场景：**

* 学生在家（External Client）连接VPN；
* 只能访问 Primary DC 的服务器（如 SSH、DNS）；
* 访问其他网站仍通过正常互联网出口。

**课堂讲解重点：**

* 对比 Full Tunnel 与 Split Tunnel；
* 演示 VPN 路由配置方式；
* 指导学生用命令行验证路由变化（`ip route`）。
* > 好——下面给你一份**课堂可直接照讲 & 演示**的教学脚本，涵盖：
  >
  > 1. Full-Tunnel vs Split-Tunnel 的概念对比与直观验证，
  > 2. 常见 VPN（OpenVPN / IPsec）下如何配置路由（演示命令/配置片段），
  > 3. 学生在客户端与防火墙上应运行的验证命令（`ip route` 等）与如何用抓包/外网 IP 验证流量路径变化。
  >
  > 你可以把这当成一页 PPT + 一段实验手册：讲完概念后带学生现场做，演示每一步并让学生自己复现。
  >
  > ------
  >
  > # 1) 概念（上课讲解要点，30–60 秒）
  >
  > - **Full Tunnel（全通道）**：VPN 建立后，**所有流量（包括访问 Internet）都走 VPN 隧道**。优点：客户端受企业防护、统一策略、可以访问内部资源；缺点：带宽与隐私（外网看起来走公司出口）。
  > - **Split Tunnel（分割通道）**：只有**访问企业内部网段**的流量走 VPN，其他 Internet 流量走本地 ISP。优点：减轻公司出口流量、保留本地网速；缺点：可能安全风险（客户端直连 Internet 时受本地环境影响）。
  > - 课堂示例图（讲义上画出）：Client →（Full）→ VPN → Company Internet；Client →（Split）→ Local Internet + VPN→ Internal
  >
  > ------
  >
  > # 2) 在 OpenVPN 中如何配置（演示最常见）
  >
  > ## A. Full Tunnel（把默认路由推到客户端）
  >
  > **Server 配置（server.conf 或 via pfSense GUI）**
  >
  > ```text
  > # server.conf (OpenVPN)
  > server 10.250.0.0 255.255.255.0
  > push "redirect-gateway def1 bypass-dhcp"    # 将默认路由推送到客户端（全通道）
  > push "dhcp-option DNS 10.200.20.2"           # 推送企业 DNS
  > ```
  >
  > - `redirect-gateway def1` 会在客户端加两条 /1 路由，覆盖默认路由，使所有流量走隧道。
  >
  > **客户端验证（连接后）**
  >
  > ```bash
  > ip route           # 查看路由表，注意有 /1 or 0.0.0.0 改变
  > curl ifconfig.me   # 检查公网 IP 是否变为公司出口 IP（Full Tunnel）
  > ```
  >
  > ## B. Split Tunnel（只推特定内网路由）
  >
  > **Server 配置**（只推内部网段）
  >
  > ```text
  > push "route 10.200.0.0 255.255.0.0"   # 推送走隧道的内网网段
  > push "dhcp-option DNS 10.200.20.2"
  > # 不推送 default route
  > ```
  >
  > - 客户端会增加具体的 10.200.x.x 路由到 tun0，但默认网关仍然指向本地 ISP。
  >
  > **客户端验证**
  >
  > ```bash
  > ip route
  > # 你会看到一条像：10.200.0.0/16 via 10.250.0.1 dev tun0
  > curl ifconfig.me   # 公网 IP 应仍为本地 ISP（Split Tunnel）
  > ```
  >
  > ------
  >
  > # 3) 在 IPsec（StrongSwan / Libreswan）中如何体现
  >
  > - **Policy-based IPsec**：在 IKE 配置里定义 `leftsubnet` / `rightsubnet`。
  >   - 若 `leftsubnet = 0.0.0.0/0`，就是把所有流量（全通道）发到对端（较少用于 Remote Access）。
  >   - 常见是 `leftsubnet = 10.250.0.0/24`（VPN pool）+ `rightsubnet = 10.200.0.0/16`（内部）。
  > - **Route-based IPsec (vti/gre)**：创建一个虚拟接口（vti/tunnel0），在本地路由表上为目标网段指向 vti；是否把默认路由指向 vti 决定全/分割。
  >
  > 示例（strongSwan style, remote access 通常是 virtual IP pool + policies）：
  >
  > ```conf
  > conn ra
  >   left=%defaultroute
  >   leftid=@vpn.example.com
  >   leftcert=server-cert.pem
  >   right=%any
  >   rightsourceip=10.250.0.0/24      # VPN 客户端地址池
  >   rightsubnet=10.200.0.0/16       # 分割：允许访问的内网段
  >   auto=add
  > ```
  >
  > - 上例是 **split-tunnel**（只允许访问 10.200.0.0/16）。
  >
  > ------
  >
  > # 4) 在 pfSense（GUI）中快速演示点
  >
  > - OpenVPN Server 页面：
  >   - `Redirect Gateway` 勾选 → 全通道（Full Tunnel）。
  >   - 不勾选并在 `Client Specific` 或 `Advanced` 里 `push "route 10.200.0.0 255.255.0.0"` → 分割（Split Tunnel）。
  > - StrongSwan / IPsec 在 pfSense：配置 Phase1/Phase2 时设置 `Local Networks` / `Remote Networks` 来控制被隧道化的流量。
  >
  > ------
  >
  > # 5) 验证步骤（课堂实操脚本：让每个学生亲测）
  >
  > ## A. 先做基线（VPN 未连接）
  >
  > 1. 在客户端运行：
  >
  > ```bash
  > ip route show
  > curl -s ifconfig.me       # 记录公网 IP (A)
  > ```
  >
  > ## B. 连接 VPN（先演示 Full Tunnel）
  >
  > 1. 连接 VPN（OpenVPN client）
  > 2. 运行：
  >
  > ```bash
  > ip route show             # 应看到 default route 被 TUN 接口替换（或 /1 路由）
  > ip route get 8.8.8.8      # 查看下一跳是否走 tun0
  > curl -s ifconfig.me       # 公网 IP 应变为公司出口 IP (B != A)
  > traceroute -n 10.200.20.2 # 内网目标走隧道
  > ```
  >
  > ## C. 断开，改为 Split Tunnel，再演示
  >
  > 1. 修改 server push 为 `push "route 10.200.0.0 255.255.0.0"`（或 server-side config），重连 client。
  > 2. 运行：
  >
  > ```bash
  > ip route show             # 看到 10.200.0.0/16 via tun0，但 default 仍指向本地网关
  > curl -s ifconfig.me       # 公网 IP 应恢复为本地 ISP (A)
  > traceroute -n 10.200.20.2 # 内网走隧道
  > traceroute -n 8.8.8.8     # Internet 仍由本地出口
  > ```
  >
  > ## D. 在防火墙/网关抓包对比
  >
  > 在 CLAYTON_FW（或公司边界）上：
  >
  > ```bash
  > tcpdump -i wan0 host <client_public_ip> and port 443
  > # 或 tcpdump -i tun0 host 10.250.0.10
  > ```
  >
  > - **Full Tunnel**：你会在公司出口（WAN）上看到来自 client 的流量（VPN 加密包）；若是 HTTPS 访问，会看到加密隧道流量经公司出口。
  > - **Split Tunnel**：仅看到去往公司内网目的地的隧道包，本地 Internet 流量不会出现在公司出口。
  >
  > ------
  >
  > # 6) 用 `ip route` 教学生快速判断（课堂示例输出）
  >
  > **Full Tunnel（示例）**
  >
  > ```text
  > $ ip route
  > default via 10.250.0.1 dev tun0 proto static metric 50
  > 10.250.0.0/24 dev tun0 proto kernel scope link src 10.250.0.10
  > ```
  >
  > → default 指向 `tun0`（全通道）
  >
  > **Split Tunnel（示例）**
  >
  > ```text
  > $ ip route
  > default via 192.168.1.1 dev eth0 proto dhcp metric 100
  > 10.200.0.0/16 via 10.250.0.1 dev tun0
  > 10.250.0.0/24 dev tun0 scope link src 10.250.0.10
  > ```
  >
  > → default 仍为本地网关；只有 10.200.0.0/16 走 tun0（分割）
  >
  > **其他命令**
  >
  > ```bash
  > ip route get 8.8.8.8      # 查看到 8.8.8.8 的下一跳（判断 Internet 是本地还是隧道）
  > ip rule show              # 若做了策略路由（policy routing）
  > ss -tunap                 # 查看活跃连接和使用的接口
  > ```
  >
  > ------
  >
  > # 7) 课堂演示任务（practice）—— 20 分钟练习脚本
  >
  > 1. 让学生在自己的 Ubuntu 容器上：`ip route` & `curl ifconfig.me`（记录 baseline）；
  > 2. 教师切换 Server 到 **Full Tunnel**，学生连接，执行 `ip route`、`curl`、`traceroute` 并截图；
  > 3. 切换到 **Split Tunnel**，学生重连，重复验证并截图；
  > 4. 要求提交小报告：`截图（路由表、ifconfig.me、traceroute） + 简短结论（Full vs Split）`。
  >
  > ------
  >
  > # 8) 常见问题 & 课堂答疑要点
  >
  > - Q：为什么 push route 后客户端没收到路由？
  >    A：检查是否 client config 允许 server-pushed routes（OpenVPN 的 `pull` 必须启用），或客户端权限受限（Windows 有时需管理员权限）。
  > - Q：为什么 Full Tunnel 下 DNS 解析仍走本地？
  >    A：需要在 server 推送 DNS（`push "dhcp-option DNS x.x.x.x"`）或配置客户端使用隧道 DNS。
  > - Q：如何在 Windows 客户端看路由表？
  >    A：`route print`；OpenVPN GUI 也会显示 `redirect-gateway` 的影响。
  >
  > ------
  >
  > 如果你需要，我可以继续帮你准备：
  >
  > - 一页 **课堂幻灯片**（含图示 + 关键命令），或
  > - 一个 **一步步练习脚本（可直接发给学生）**，包含步骤、预期截图和常见错误排查。
  >
  > 你想先要哪一个？

---

### 6.3 Submission Requirement（提交要求）

此处说明了视频与报告具体要求及评分标准。

#### 🔹 视频内容（Video）

1. **Site-to-Site 演示：**

* 要录制使用 **Wireshark** 抓取三条VPN隧道（共三组）上的 **ESP加密流量**；
* 需展示跨校区通信数据成功通过加密隧道；
* 每个隧道演示 4 分，共 12 分。

2. **Remote Access VPN 演示：**

* 展示远程用户通过VPN访问 Primary DC 的内部服务；
* 同时证明非Primary DC流量未走VPN；
* 录制Wireshark流量截图；
* 共 8 分。

#### 🔹 报告内容（Report）

1. 执行命令：

```bash
/ip ipsec installed-sa print
```

并将每个防火墙的输出截图放入报告（每个0.5分）。

2. 展示 External Client（远程客户端）的VPN配置（0.5分）。

**课堂讲解重点：**

* 强调Wireshark抓包的重要性；
* 讲解ESP流量识别；
* 让学生了解如何验证VPN是否生效。

---

## 三、7. Firewall Configuration（防火墙配置，18分）

### 任务目的

配置三校区防火墙，以确保网络访问控制和安全策略有效。

---

### 🔹 通用防火墙要求（12分）

| 要求      | 说明                         |
| ------- | -------------------------- |
| DNS 服务器 | 仅允许三校区内部和远程VPN访问           |
| WEB 服务器 | 可被所有内部与外部客户端访问（包括VPN用户）    |
| 客户端     | 各站点客户端应能 ping 通各自防火墙（默认网关） |
| SSH 服务器 | 仅允许 Remote VPN 用户访问        |

**课堂讲解建议：**

* 使用 Mikrotik 或 Linux iptables 演示 ACL 配置；
* 说明“白名单策略”：只允许明确访问的端口；
* 讲解如何测试规则（如 telnet、ping、nmap）。
* > 非常好 👏 你这部分是课堂重点之一：**“防火墙访问控制策略 + 实际 ACL 测试”**。
  >  学生在这里最容易混乱的就是「谁能访问谁」、「怎么写规则」和「如何验证」。
  >  下面我给你一份 **教学讲解 + 实操演示脚本（适合在 Mikrotik 或 Linux iptables 环境）**，让你可以直接讲、现场演示、学生跟做。
  >
  > ------
  >
  > ## 🎯 一、任务目标回顾
  >
  > > 配置三校区的防火墙，确保：
  > >
  > > - DNS 只允许内网 & VPN；
  > > - Web 所有人可访问；
  > > - SSH 只允许 VPN；
  > > - 各客户端能 ping 自己的防火墙（网关）。
  >
  > ------
  >
  > ## 🧩 二、实验逻辑结构（课堂讲解）
  >
  > | 网络区       | 示例子网       | 允许访问目标                    | 示例规则         |
  > | ------------ | -------------- | ------------------------------- | ---------------- |
  > | Client LAN   | 10.200.10.0/24 | Ping 本校防火墙                 | `ICMP allow`     |
  > | DMZ          | 10.200.40.0/24 | Web/SMTP 对外开放               | TCP 80,443,25    |
  > | Internal LAN | 10.200.20.0/24 | DNS/CA/SSH，仅内部或 VPN 可访问 | TCP 22,53        |
  > | VPN          | 10.250.0.0/24  | 可访问 DNS、SSH、Web            | TCP 22,53,80,443 |
  > | Internet     | —              | 仅可访问 Web, SMTP（DMZ）       | TCP 80,443,25    |
  >
  > 👉 教学重点：
  >  **“白名单原则” (Default Deny + Explicit Allow)**
  >
  > > 防火墙最后一条规则是 “Drop all”，只有明确放行的流量才允许通过。
  >
  > ------
  >
  > ## 🔹 三、使用 Linux iptables 演示（推荐 pfSense 或 VyOS CLI 一致）
  >
  > 假设这台是 CLAYTON 校区的防火墙。
  >
  > ### 1️⃣ 设置默认策略
  >
  > ```bash
  > iptables -P INPUT DROP
  > iptables -P FORWARD DROP
  > iptables -P OUTPUT ACCEPT
  > ```
  >
  > > 表示所有流量默认拒绝（白名单模式）。
  >
  > ------
  >
  > ### 2️⃣ 允许基础通信（回环 & 已建立连接）
  >
  > ```bash
  > iptables -A INPUT -i lo -j ACCEPT
  > iptables -A INPUT -m state --state ESTABLISHED,RELATED -j ACCEPT
  > ```
  >
  > ------
  >
  > ### 3️⃣ 各功能规则示例
  >
  > #### ✅ (1) 允许 Client ping 自己防火墙
  >
  > ```bash
  > iptables -A INPUT -s 10.200.10.0/24 -p icmp -j ACCEPT
  > ```
  >
  > ------
  >
  > #### ✅ (2) DNS 服务器规则（只允许内部+VPN访问）
  >
  > ```bash
  > # 允许内网访问 DNS (UDP/TCP 53)
  > iptables -A INPUT -s 10.200.0.0/16 -p udp --dport 53 -j ACCEPT
  > iptables -A INPUT -s 10.200.0.0/16 -p tcp --dport 53 -j ACCEPT
  > 
  > # 允许 VPN 用户访问 DNS
  > iptables -A INPUT -s 10.250.0.0/24 -p udp --dport 53 -j ACCEPT
  > iptables -A INPUT -s 10.250.0.0/24 -p tcp --dport 53 -j ACCEPT
  > ```
  >
  > ------
  >
  > #### ✅ (3) Web 服务器规则（可被任何人访问）
  >
  > ```bash
  > # 允许任何来源访问 Web (HTTP/HTTPS)
  > iptables -A INPUT -p tcp -m multiport --dports 80,443 -j ACCEPT
  > ```
  >
  > ------
  >
  > #### ✅ (4) SSH 服务器规则（仅 VPN 用户）
  >
  > ```bash
  > # 拒绝所有非 VPN 的 SSH
  > iptables -A INPUT -p tcp --dport 22 -j DROP
  > # 允许 VPN 用户 SSH
  > iptables -I INPUT -s 10.250.0.0/24 -p tcp --dport 22 -j ACCEPT
  > ```
  >
  > ------
  >
  > #### ✅ (5) 记录和丢弃其余流量
  >
  > ```bash
  > iptables -A INPUT -j LOG --log-prefix "Dropped: "
  > iptables -A INPUT -j DROP
  > ```
  >
  > ------
  >
  > ### 4️⃣ 保存规则
  >
  > ```bash
  > sudo iptables-save > /etc/iptables.rules
  > ```
  >
  > ------
  >
  > ## 🔹 四、使用 Mikrotik RouterOS 演示（等价配置）
  >
  > 在 **Firewall → Filter Rules** 里依次添加：
  >
  > | Chain | Src.Address    | Dst.Port | Protocol | Action | Comment      |
  > | ----- | -------------- | -------- | -------- | ------ | ------------ |
  > | input | 10.200.10.0/24 | -        | ICMP     | accept | 客户端 ping  |
  > | input | 10.200.0.0/16  | 53       | UDP/TCP  | accept | 内网 DNS     |
  > | input | 10.250.0.0/24  | 53       | UDP/TCP  | accept | VPN DNS      |
  > | input | any            | 80,443   | TCP      | accept | Web 服务     |
  > | input | 10.250.0.0/24  | 22       | TCP      | accept | SSH via VPN  |
  > | input | any            | 22       | TCP      | drop   | 拒绝外部 SSH |
  > | input | any            | any      | any      | drop   | 默认拒绝     |
  >
  > > 在 Mikrotik 中确保规则顺序正确（匹配从上到下）。
  >
  > ------
  >
  > ## 🧠 五、课堂演示思路（讲 + 演 + 验）
  >
  > ### 🧩 Step 1：讲解“白名单原则”
  >
  > - 默认所有流量被拒绝；
  > - 只放行业务需要的端口；
  > - 每个防火墙都独立判断“谁能访问谁”。
  >
  > ### 🧩 Step 2：用命令或 GUI 实际添加规则
  >
  > - 讲解每条规则目的；
  > - 提醒学生注意 IP 范围和方向（src/dst）。
  >
  > ### 🧩 Step 3：现场验证规则（学生实验）
  >
  > | 测试项            | 客户端命令                        | 预期结果   |
  > | ----------------- | --------------------------------- | ---------- |
  > | Ping 本校防火墙   | `ping 10.200.10.1`                | ✅ 通       |
  > | 访问 Web          | `curl http://10.200.40.2`         | ✅ 页面输出 |
  > | 外部访问 DNS      | `nslookup google.com 10.200.20.2` | ❌ 拒绝     |
  > | VPN 用户访问 DNS  | `nslookup google.com 10.200.20.2` | ✅ 正常     |
  > | VPN 用户 SSH 登录 | `ssh user@10.200.20.4`            | ✅ 可登录   |
  > | 外网 SSH          | `telnet 10.200.20.4 22`           | ❌ 被拒     |
  >
  > ------
  >
  > ## 🧪 六、工具验证演示（课堂互动）
  >
  > 1. **Ping 测试连通性**
  >
  >    ```bash
  >    ping -c 2 10.200.10.1
  >    ```
  >
  > 2. **Telnet 测端口**
  >
  >    ```bash
  >    telnet 10.200.40.2 80
  >    ```
  >
  > 3. **Nmap 探测服务**
  >
  >    ```bash
  >    nmap -sS 10.200.20.4
  >    ```
  >
  >    - 只有 VPN 用户能扫到 22（SSH）
  >    - 普通客户端或外部应显示端口过滤
  >
  > 4. **Wireshark 抓包演示**
  >
  >    - 在防火墙 WAN 接口抓包；
  >    - 显示 HTTP 流量能进，SSH 流量被拒；
  >    - 讲解包匹配顺序与默认丢弃。
  >
  > ------
  >
  > ## 🧱 七、教学总结语（你可以直接念 👇）
  >
  > > “防火墙配置的关键是**白名单思维**：
  > >  不问‘要拦谁’，而是只允许‘谁可以进’。
  > >  每条规则都是‘显式放行’，最后一条是‘全部拒绝’。
  > >  在验证时，我们不光要看通不通，更要理解为什么通或为什么被拦。”
  >
  > ------
  >
  > ## ✅ 八、扩展练习（提高题，可布置作业）
  >
  > 1. **将规则迁移到 pfSense 或 VyOS 上（图形化管理）**
  >    - 让学生对比 CLI 与 GUI 区别。
  > 2. **配置日志审计**
  >    - 使用 `iptables -j LOG` 或 Mikrotik “log=yes”。
  >    - 让学生观察日志中被拦截的包。
  > 3. **模拟攻击测试（DoS、端口扫描）**
  >    - 用 `nmap -p 1-1024` 扫 DMZ，观察防火墙丢包与日志行为。
  > 4. **加入 VPN 用户测试**
  >    - 连接 VPN 后访问 SSH / DNS。
  >    - 断开 VPN 再访问，验证访问受限。
  >
  > ------
  >
  > 是否希望我帮你做一份 **可直接发给学生的实验指导文档（Word 或 PDF）**？
  >  内容包括上述配置命令、验证命令表和结果截图占位。这样学生跟着操作就能完成防火墙 ACL 实验。

---

### 🔹 个性化配置要求（3分）

每个学生根据 **student ID mod 3** 结果，配置不同防火墙规则：

| studentID mod 3 | 配置要求                                   |
| --------------- | -------------------------------------- |
| 0               | SMTP服务器可供Clayton校区与外部用户访问，但VPN用户不可访问   |
| 1               | SMTP服务器可供Peninsula校区与外部用户访问，但VPN用户不可访问 |
| 2               | 规则会在下一页（第6页）继续说明                       |

**教学重点：**

* 教学生如何使用“取模计算”分配任务；
* 说明不同防火墙配置的逻辑意义（限制特定流量入口）；
* 强调不同学生的配置必须唯一，防止抄袭。

---

## 四、课堂教学总结

| 教学主题       | 内容与意义       | 教学建议                   |
| ---------- | ----------- | ---------------------- |
| BGP攻击与防御   | 演示路由劫持与恢复   | 实机演示prefix hijacking实验 |
| IPSec VPN  | 校区互联与数据加密   | 讲解ESP抓包分析              |
| Remote VPN | 远程访问安全      | 展示split tunnel配置       |
| 防火墙配置      | 访问控制与网络隔离   | 实操iptables规则测试         |
| 学术诚信       | 每人独立配置、唯一任务 | 检查studentID-based配置    |

---

是否希望我继续为你讲解下一页（第 6 页）的内容？那一页会补充剩下的防火墙配置（studentID mod 3 = 2）及后续评分细则，我可以连同前几页一起帮你整理成一份完整的“期末考核讲解课件脚本”，适合课堂逐页讲授。


---

## 第 6 页

![第 6 页](FIT3031-Final-Assessment-Specifications-2025-S2_assets/page-006.png)

非常好，这张截图是 **Monash University FIT3031《Network Security（网络安全）》期末考核说明文档的第 6 页**，是整份作业中非常关键的部分。它主要涵盖三个主题：

1. **防火墙配置任务的最后部分与提交要求（Firewall Configuration）**
2. **网络安全分析（Security Analysis）**
3. **入侵检测系统 IDS 配置（Intrusion Detection System）**

下面我会为你分段详细解释内容含义、设计目的以及课堂讲解思路，帮助你备课时能够系统讲解给学生听。

---

## 一、继续前一页：防火墙配置（Firewall Configuration）

这一页开头延续第 5 页内容，补充了 **Student ID mod 3 = 2** 的情况：

> **If student ID mod 3 = 2:**
> – The SMTP server must be accessible to users on the Caulfield campus and to external users.
> – SMTP should not be accessible via the remote access VPN.

也就是说：

* 学号除以 3 余数为 2 的学生，SMTP 服务器的访问规则如下：

* **允许**：Caulfield 校区和外部用户；
* **禁止**：通过远程 VPN 访问的用户。

---

### 🔹 防火墙规则的一般要求与注意事项

文档接着列出了一系列非常重要的注意点：

#### 1️⃣ 必须添加隐式拒绝规则（Implicit deny rules）

> All firewalls must have implicit deny rules at the bottom...

也就是说：

* 每个防火墙的 input、output、forward 链底部必须加上：

```bash
drop all
```
* 若没有该规则，系统默认放行所有流量，将视为安全漏洞；
* 该项遗漏会导致整个防火墙部分**直接记零分**。

**课堂讲解要点：**

* 可用图示展示“防火墙匹配顺序”；
* 解释隐式拒绝是网络安全的最后防线；
* 举例说明未加此规则导致的漏洞（如开放端口被攻击）。

---

#### 2️⃣ 确保网络基础功能正常（VPN、防火墙路由等）

> If additional firewall rules are needed... they should be added.

* 若为了保证 VPN 隧道、远程访问功能等能正常工作，可以额外添加例外规则；
* 否则系统可能通信中断；
* 若因为规则不当导致网络失效，可被扣分最高 8 分。

---

#### 3️⃣ 配置跨校区防火墙规则（Inter-site traffic）

> When enabling inter-site traffic, firewall rules must be configured on both sites...

* 例如：若 Caulfield 与 Clayton 校区互联，则双方防火墙都需设置允许规则；
* 仅单边允许是不够的；
* 必须对称配置。

---

#### 4️⃣ 限制端口与接口

> Only the respective service port(s) should be allowed...

* 只允许必要端口（如 TCP 443/80 for WEB、UDP 53 for DNS）；
* 同时需指定：

* 源 IP
* 目的 IP
* 源接口
* 目标接口
* 以防止“宽泛匹配”造成潜在漏洞。

**教学建议：**

* 演示 Mikrotik 或 iptables 规则写法；
* 举例“宽松 vs 精确匹配”差异。

---

### 🔹 7.1 提交要求（Submission Requirement）

#### 视频（Video）

> Record a video demonstrating that the firewall rules are functioning as expected...

视频需展示以下内容：

1. 从**允许访问的节点**连接服务成功；
2. 从**被禁止的节点**连接失败；
3. 展示所有防火墙规则；
4. 验证配置与截图一致。

#### 报告（Report）

> Provide a screenshot of the firewall rules of each firewall...

要求：

* 截图展示每个防火墙的规则列表；
* 可使用命令：

```bash
/ip firewall filter print
```
* 所有规则应记录在提供的模板中；
* 此部分报告占 3 分。

---

## 二、Security Analysis（安全性分析，12 分）

这一部分考查学生对自己网络安全方案的分析能力，属于**理论与反思型题目**。

---

### 🔹 任务说明

> Perform a security analysis of the network you configured...

要求学生写一篇**不超过 1000 字**的报告，回答以下两个问题：

---

### 1️⃣ Firewall Bypass Analysis（4分）

> Can the firewall configuration be bypassed?

学生需分析：

* 是否存在绕过防火墙的可能；
* 如果“能”，解释原理（如 ICMP 隧道、VPN伪装、端口转发等）；
* 并说明防御对策；
* 如果“不能”，则需说明规则如何防止绕过。

**教学重点：**

* 引导学生从“逻辑层安全漏洞”角度分析；
* 举例：NAT未配置、允许ANY端口规则、信任区域过宽等；
* 强调防火墙不是“万能盾牌”，还需结合IDS等机制。

---

### 2️⃣ Network Security Improvement（8分）

> Discuss how the security of the network... can be further improved.

要求学生提出：

* 网络安全提升方案；
* 包含**新设备或新技术**建议；

* 例：IDS/IPS、反病毒网关、SIEM系统；
* 说明如何集成到当前拓扑中；
* 解释该措施的具体强化作用。

**教学建议：**

* 让学生画出自己的拓扑结构；
* 讨论“纵深防御（defense in depth）”概念；
* 引导学生关注服务安全（WEB、SSH、SMTP等）。

---

### 注意：

> No video demonstration required.

这一部分**只提交报告，不需录视频**。

---

## 三、9. IDS（入侵检测系统，15分）

这一部分是本课程最具实战性的部分之一，考查学生能否部署并使用 **Snort IDS** 检测攻击行为。

---

### 🔹 任务要求

> You are required to exploit an internal server as an external attacker and configure IDS to detect and alert on these intrusion attempts.

**核心任务：**

1. 模拟一次攻击行为；
2. 让 IDS 能检测到并报警；
3. 分析检测到的流量。

---

### 具体步骤（第一个小任务）

> Configure a Snort IDS node to the same network where your public servers (WEB, SSH and SMTP) are connected...

也就是说：

* 在连接公有服务器的网络段上，部署 Snort；
* 配置交换机端口镜像（port mirroring），使 IDS 能看到所有进出流量；
* 使用实验室（IDS lab）中学过的方法；
* 这部分任务 4 分。

**教学重点：**

* 解释 IDS 的工作原理（被动监控 vs 主动防御）；
* 讲解“端口镜像”机制；
* 演示 Snort 如何实时捕获攻击日志；
* 让学生理解 IDS 与防火墙的区别：
防火墙阻止攻击，IDS 发现攻击。

---

## 四、课堂教学总结表

| 教学主题   | 内容                    | 教学要点          |
| ------ | --------------------- | ------------- |
| 防火墙规则  | 三种 ID 情况下不同 SMTP 访问策略 | 讲解防火墙链结构与隐式拒绝 |
| 防火墙演示  | 视频展示允许/拒绝连接           | 说明如何验证防火墙正确性  |
| 安全分析   | 理论反思报告                | 引导学生思考安全漏洞与改进 |
| IDS 实验 | Snort 配置与攻击检测         | 演示IDS日志捕获过程   |
| 实践与报告  | 视频+截图+报告结合            | 强调格式统一与可视化演示  |

---

是否希望我帮你把 **第1页到第6页的全部内容** 整理成一份系统的 **“期末考核教学讲稿+PPT提纲”**？
我可以为你编排每章讲解时间分配、教学目标、提问环节、和实验演示建议，让你上课直接使用。


---

## 第 7 页

![第 7 页](FIT3031-Final-Assessment-Specifications-2025-S2_assets/page-007.png)

非常好，这张截图是 **Monash University（莫纳什大学）FIT3031《Network Security（网络安全）》期末考核说明文档的第 7 页**，是整份作业的最后一页，内容包括三部分：

1. **入侵检测系统 IDS（Intrusion Detection System）部分的后半内容与提交要求**
2. **报告展示质量评分标准（Quality of Presentation）**
3. **附录：为校区添加额外局域网的步骤（Appendix A）**

这一页总结了整个课程设计的最后实验任务，学生在这里需要综合运用网络安全各模块（防火墙、VPN、BGP、IDS等）完成系统防护。下面我会为你详细逐条解释内容含义、教学目标，以及课堂讲解要点。

---

## 一、继续第9章：IDS（Intrusion Detection System，入侵检测系统）

这一部分接续前一页（第6页）的任务，是 **网络防御实战的核心环节**。
学生需要配置 Snort IDS，执行攻击模拟实验，并让 IDS 检测并报警。

---

### 🔹 实验目标

学生要模拟两种常见的网络攻击：

1. **TCP Port Scan 攻击**（端口扫描）
2. **DoS 攻击**（拒绝服务攻击）

---

### 1️⃣ TCP Port Scan（5分）

> Perform TCP port scan on the SSH server from an external attacker node...

说明：

* 学生需从外部攻击节点（External Attacker）扫描内部 SSH 服务器端口；
* 该节点应位于 **Monash 网络之外（outside Monash network）**；
* 可使用任意扫描方式（如 `nmap`、`hping3` 等）；
* IDS（Snort）必须能检测到该扫描，并生成报警。

**教学讲解建议：**

* 解释端口扫描的原理（探测服务端口开放情况）；
* 举例展示 Nmap 命令：

```bash
nmap -sS <target_IP>
```
* 让学生理解 IDS 如何基于流量模式识别扫描行为（如SYN探测频繁）。

---

### 2️⃣ DoS 攻击（5分）

> Perform a Denial of Service (DoS) attack on the Web server from an external attacker node...

说明：

* 学生从外部攻击节点对 Web 服务器发动拒绝服务攻击；
* 可以采用任何类型（如 SYN Flood、HTTP Flood 等）；
* IDS 需检测到攻击流量并生成警报；
* 可使用现有攻击工具或编写简单 Python 攻击脚本。

**课堂讲解建议：**

* 讲解 DoS 攻击原理（请求泛滥导致服务器资源耗尽）；
* 可用 `hping3` 或 `slowloris` 举例演示；
* 强调测试环境与安全规范（必须在封闭虚拟网络内进行）。

---

### 3️⃣ 注意事项（Notes）

> Configurations without demonstration are not sufficient to receive any marks.

👉 **仅配置 IDS 而不录制演示视频，将不得分。**
学生必须展示“攻击 + 检测”的全过程。

> IDS rules must be customized...

👉 IDS 规则必须针对本实验流量定制，
要能识别**恶意流量**，同时忽略**正常通信**。
（例如，只检测异常频率的SSH连接，而非普通登录。）

**教学重点：**

* 让学生理解“检测精确度”；
* IDS 误报（False Positive）与漏报（False Negative）的概念；
* 鼓励学生用 Snort 规则语句精确匹配攻击特征。

---

### 4️⃣ 9.1 Submission Requirement（提交要求）

**视频（Video）**

> Demonstrate ... a live exploitation of the scan and the attack and the IDS detection alerts.

学生的视频要展示：

1. 攻击发起过程；
2. IDS 的实时检测与报警；
3. 讲解 IDS 规则的逻辑与意义；
4. 强调 IDS 只对恶意流量报警，不对正常流量触发。

**报告（Report）**

> Provide the IDS rule configuration in the report. (1 Mark)

* 报告需附上 IDS 规则配置内容；
* 例如 Snort 规则样例：

```bash
alert tcp any any -> 10.200.0.2 22 (msg:"SSH Port Scan Detected"; flags:S; threshold:type both, track by_src, count 10, seconds 5;)
```

**课堂讲解重点：**

* 让学生理解 Snort 规则语法结构（action、protocol、source、destination、options）；
* 强调在真实网络中 IDS 的部署位置（应靠近防火墙外侧）；
* 可举例展示 Snort 日志中的检测记录（/var/log/snort/alert）。

---

## 二、10. Quality of Presentation（展示质量，5分）

> The remaining 5 marks are allocated to the quality and clarity of presentation...

即最后 5 分用于评分学生提交作品的**呈现质量**。包括：

* 报告的组织结构；
* 截图清晰度；
* 视频讲解流畅度；
* 英语表达和技术说明的逻辑性。

**课堂讲解建议：**

* 教学生如何制作良好的技术演示视频（如分镜脚本、配字幕、展示清晰）；
* 提供一个评分标准样例，如：

| 评分项   | 标准          |
| ----- | ----------- |
| 逻辑与结构 | 报告章节完整、有条理  |
| 图表与截图 | 清晰、标注正确     |
| 视频讲解  | 英语表达自然、操作清晰 |
| 技术细节  | 对每项任务解释到位   |

---

## 三、Appendix A：Steps to Add Additional LAN to a Campus（为校区添加额外局域网的步骤）

附录部分提供了**技术指导**，用于扩展 GNS3 网络拓扑。
学生在实验中如需增加新子网，可按以下步骤进行。

---

### 🔹 步骤 1：连接交换机

> Add a switch and connect it to a vacant port in the campus router/firewall.

* 在 GNS3 中添加一个虚拟交换机；
* 将其连接到校园路由器或防火墙的空闲接口。

---

### 🔹 步骤 2：规划 IP 子网

> Decide the IP subnet for the new network...

例如：

* Clayton 校区：
原有 10.200.10.0/24
新增可用 10.200.20.0/24、10.200.30.0/24
* Peninsula 校区：
可使用 10.201.20.0/24 等。

**课堂演示建议：**

* 展示如何计算新子网；
* 讲解子网掩码与地址分配（如 `/24` 表示 256 个地址）。

---

### 🔹 步骤 3：配置防火墙接口 IP

> Login to the firewall and assign an IP address...

示例命令：

```bash
/ip address add address=10.200.20.1/24 network=10.200.20.0 interface=ether3
```

* 该 IP 为该新局域网的默认网关；
* 学生需理解每个 LAN 必须有防火墙网关。

---

### 🔹 步骤 4：配置 DHCP（可选）

> Configure a DHCP server for the new subnet...

* 如果客户端使用静态 IP，此步可跳过；
* 否则，防火墙可配置 DHCP 自动分配地址。

---

## 四、课堂教学总结表

| 教学模块   | 内容            | 教学重点           |
| ------ | ------------- | -------------- |
| IDS 实验 | Snort 配置与攻击检测 | 实机演示端口扫描与DoS攻击 |
| IDS 视频 | 展示实时检测与报警     | 强调精准规则与误报控制    |
| 报告撰写   | IDS规则配置与逻辑解释  | 讲解Snort规则结构    |
| 演示评分   | 视频与报告质量       | 指导学生如何制作清晰技术展示 |
| 附录内容   | 新LAN添加方法      | 讲授子网划分与网关配置实践  |

---

## 五、总结：整份作业的总体教学逻辑

这份“期末网络安全综合实验”实际上是一个 **完整的企业级安全架构模拟项目**，教学重点如下：

| 模块   | 实践内容        | 核心技能      |
| ---- | ----------- | --------- |
| 网络设计 | GNS3搭建三校区网络 | 网络拓扑设计    |
| 安全路由 | BGP配置与防劫持   | 路由安全与前缀验证 |
| 加密通信 | IPSec VPN配置 | 数据加密与隧道通信 |
| 访问控制 | 防火墙策略       | 安全边界防护    |
| 攻击防御 | IDS检测与响应    | 安全事件监测    |
| 安全分析 | 撰写报告        | 安全评估与改进能力 |

---

是否希望我帮你把整份（第1页–第7页）的教学内容整合成一份 **期末考核课程讲稿 + PPT大纲**？
我可以按“教学目标→知识讲解→课堂演示→实验指导→评分标准”五个板块编排，方便你直接用作远程教学课件。
