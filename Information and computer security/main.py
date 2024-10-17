# 模拟信用卡类
class ChipCard:
    def __init__(self, card_number, exp_date, card_holder, CVV):
        self.card_number = card_number  # 卡号
        self.exp_date = exp_date  # 有效期
        self.card_holder = card_holder  # 持卡人
        self.CVV = CVV

    def send_card_info(self):
        # 返回卡片信息（如卡号等）
        print(self.card_number)
        print(self.card_holder)
        print(self.exp_date)
        print(self.CVV)
        return {
            "card_number": self.card_number,
            "exp_date": self.exp_date,
            "card_holder": self.card_holder,
            "CVV": self.CVV
        }

# 模拟商家的读卡终端类
class CardTerminal:
    def __init__(self):
        self.card_info = None

    def read_card(self, card):
        # 从卡片中读取信息
        self.card_info = card.send_card_info()
        print(f"终端：读取到卡信息：{self.card_info}")
        return self.card_info

    def send_payment_request(self, bank):
        if self.card_info:
            # 向银行发送支付请求
            result = bank.verify_card(self.card_info)
            return result
        else:
            print("终端：未读取到卡信息，无法发起支付请求。")
            return None

# 模拟发卡银行类
class IssuerBank:
    def __init__(self, valid_card_number,valid_exp_date ,valid_card_holder, valid_CVV):
        self.valid_card_number = valid_card_number  # 假设银行持有的有效卡号
        self.valid_exp_date = valid_exp_date
        self.valid_card_holder = valid_card_holder
        self.valid_CVV = valid_CVV


    def verify_card(self, card_info):
        # 验证卡号是否有效
        if card_info == {
            "card_number": self.valid_card_number,
            "exp_date": self.valid_exp_date,
            "card_holder": self.valid_card_holder,
            "CVV": self.valid_CVV
        }:
            print("银行：卡号验证成功，交易授权通过。")
            return "授权通过"
        else:
            print("银行：卡号验证失败，交易被拒绝。")
            return "授权失败"

# 初始化三方
card = ChipCard("1234567890123456", "12/25", "张三","111")
terminal = CardTerminal()
bank = IssuerBank("1234567890123456", "12/25", "张三","111")  # 假设银行认为这个卡号是有效的

# 1. 终端读取卡信息
card_info = terminal.read_card(card)

# 2. 终端向银行发起支付请求
if card_info:
    result = terminal.send_payment_request(bank)
    print(f"支付结果：{result}")
