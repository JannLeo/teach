你现在面对的是两个任务的重叠点：

---

### ✅ **你已经完成了 Site-to-Site VPN**（根据 Lab5 的内容）
### 🎯 **现在你要做的是 Remote Access VPN**（Final Assessment 要求 + Lab5 指导）

---

## ✅ 目标：完成 Final Assessment 的 **Remote Access VPN 部分（Task 6.2）**

---

### 🔍 要求回顾（来自 Final Assessment PDF）：

> **Task 6.2: Remote Access VPN**
>
> - 在 **Primary DC** 上配置 Remote Access IPsec VPN
> - 外部客户端（External-Client）连接后：
>   - **只能访问 Primary DC 的内部子网**（split tunneling）
>   - **其他流量（如访问 Google）不走 VPN**
> - 视频要求：
>   - 用 Wireshark 抓到 **ESP 流量**
>   - 展示访问 Primary DC 内部服务（如 SSH/Web）
>   - 展示 **非 Primary DC 流量不走隧道**

---

## ✅ 步骤总结（结合 Lab5 和 Final Assessment）

---

### 🔧 第一步：确认你的 Primary DC 是哪一个

根据你的 **Student ID mod 3**：

| 余数 | Primary DC |
| ---- | ---------- |
| 0    | Caulfield  |
| 1    | Clayton    |
| 2    | Peninsula  |

➡️ 假设你是 **Clayton（Primary DC）**，那么你要在 **Clayton-FW** 上配置 Remote Access VPN。

---

### 🔧 第二步：在 Primary DC 防火墙上配置 Remote VPN

#### ✅ 1. 创建 IP 池（给 VPN 客户端分配地址）

```bash
/ip pool add name=remote-pool ranges=10.200.10.100-10.200.10.110
```

#### ✅ 2. 创建 IPSec Profile（IKE）

```bash
/ip ipsec profile add name=remote-profile hash-algorithm=sha256 enc-algorithm=aes-256 dh-group=modp2048
```

#### ✅ 3. 创建 Proposal（ESP）

```bash
/ip ipsec proposal add name=remote-proposal auth-algorithms=sha256 enc-algorithms=aes-256-cbc pfs-group=modp2048
```

#### ✅ 4. 创建 Mode-config（split tunneling）

```bash
/ip ipsec mode-config add name=remote-conf address-pool=remote-pool address-prefix-length=32 split-include=10.200.10.0/24
```

> 🔍 `split-include` 是关键，它告诉客户端：**只有访问 10.200.10.0/24 的流量走 VPN**

#### ✅ 5. 创建 Peer（接受任意地址）

```bash
/ip ipsec peer add name=remote-peer address=0.0.0.0/0 exchange-mode=ike2 profile=remote-profile
```

#### ✅ 6. 创建 Identity（PSK）

```bash
/ip ipsec identity add peer=remote-peer auth-method=pre-shared-key secret=fit3031vpn generate-policy=port-strict mode-config=remote-conf
```

#### ✅ 7. 创建 Policy Template

```bash
/ip ipsec policy add template=yes group=default proposal=remote-proposal
```

---

### 🔧 第三步：配置 External-Client（Ubuntu）

#### ✅ 1. 安装 strongSwan

```bash
sudo apt update
sudo apt install strongswan strongswan-pki
```

#### ✅ 2. 编辑 `/etc/ipsec.conf`

```bash
conn monash-remote
    keyexchange=ikev2
    ike=aes256-sha256-modp2048!
    esp=aes256-sha256-modp2048!
    left=%defaultroute
    leftsourceip=%config
    leftauth=psk
    right=<Primary-DC-Public-IP>
    rightauth=psk
    rightsubnet=10.200.10.0/24
    auto=start
```

#### ✅ 3. 编辑 `/etc/ipsec.secrets`

```bash
%any <Primary-DC-Public-IP> : PSK "fit3031vpn"
```

#### ✅ 4. 启动连接

```bash
sudo ipsec restart
sudo ipsec up monash-remote
```

---

### ✅ 第四步：验证 split tunneling

#### ✅ 1. 查看分配的 IP

```bash
ip address
```

你应该看到类似：

```
10.200.10.100/32 scope global
```

#### ✅ 2. 测试访问 Primary DC 的内部服务

```bash
ssh user@10.200.10.120
lynx http://10.200.10.120
```

✅ 应该能访问（走 VPN）

#### ✅ 3. 测试访问 Google（不应走 VPN）

```bash
ping 8.8.8.8
```

✅ 应该能通，但 **不走 VPN**（你可以用 Wireshark 确认没有 ESP 流量）

---

### ✅ 第五步：Wireshark 抓包（用于视频）

- 在 **Primary DC 防火墙** 或 **External-Client** 上抓包
- 过滤：`esp`
- 你应该看到：
  - 访问 **10.200.10.0/24** 时有 ESP 包
  - 访问 **8.8.8.8** 时没有 ESP 包

---

### ✅ 第六步：截图 & 报告

#### ✅ 视频要求（Final Assessment）：

- 显示你连接 VPN
- 显示访问 Primary DC 内部服务（SSH/Web）
- 显示 Wireshark 中 **ESP 流量**
- 显示访问 Google **无 ESP 流量**

#### ✅ 报告要求：

- 提供 `/ip ipsec installed-sa print` 输出（Primary DC）
- 提供 External-Client 的 VPN 配置（如 `ipsec.conf`）
- 提供 Wireshark 截图（ESP vs 非 ESP）

---

## ✅ 总结：你现在要做的

| 任务                | 状态                                      |
| ------------------- | ----------------------------------------- |
| ✅ Site-to-Site VPN  | 已完成                                    |
| 🎯 Remote Access VPN | 按上面步骤配置                            |
| 📸 Wireshark 抓包    | 视频用                                    |
| 🧾 报告截图          | `/ip ipsec installed-sa print` + VPN 配置 |

---

## ✅ 下一步

你可以现在就在 **Primary DC 防火墙** 上开始配置 Remote VPN，然后我在你配置完后帮你检查：

- `/ip ipsec installed-sa print`
- `/ip firewall nat print`
- Wireshark 是否能看到 ESP

---

要不要我帮你 **检查你当前的配置** 或者 **带你一步步在 GNS3 里配一遍**？你可以贴出你现在的配置，我来帮你验证。