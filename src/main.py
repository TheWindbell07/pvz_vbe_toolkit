"""
main program to implement specific functions.
"""

import sys
import win32event
import win32api

from ui_functions import *

"""
如无特别声明，以下数字代表的含义：
scene: {0:day, 1:night, 2:pool, 3:fog, 4:roof, 5:midnight}  # midnight场景可能会出现问题
row: 0-4(scene=0,1,4,5), 0-5(scene=2,3)  # 从上往下依次增加
col(umn): 0-8  # 从左往右依次增加
plant_id: 0-47  # 见./imports/plants_set.csv
zombie_id: 0-32  # 见./imports/zombies_set.csv
"""

class Train:
    def __init__(self, target):
        self.target = target

    def plantern_memorize(self, level=0, wait_time=2.0):  # 灯笼速记练习
        """
        A quick-memorizing practice.
        A plantern which only exist for a few seconds will be planted around several vase, you must remember what is in the vases to finish the following tasks.
        :param wait_time:
        :param level: contributing to which colume the plantern is in.
        :return: None.
        """
        time.sleep(0.1)
        self.target.game.set_scene(1)
        self.target.game.put_vase(4, 8, 4, 1, 17, 0, 0)
        print("NIGHT scene set.")

        PLA_ROW = random.choice((1, 2, 3))
        PLA_COL = level + 1
        self.target.game.put_plant(
            plant_type=25,
            row=PLA_ROW,
            col=PLA_COL,
            imitator=0
        )
        print("PLANTERN plant put.")

        SOURCE = [100, 103, 104, 105, 105, 117, 117, 117, 117, 117, 118, 118, 152, 152, 152, 152, 152, 152,
                  204, 204, 204, 204, 204, 215, 200, 200, 200, 223, 223, 223, 223, 223, 223, 300]
        MAP = []
        SOURCE = random.sample(SOURCE, k=16)
        for VAS_ROW in (0, 1, 2, 3, 4):
            for VAS_COL in (2, 3, 4):
                if (VAS_ROW - PLA_ROW) ** 2 + (VAS_COL - PLA_COL) ** 2 in (1, 2):
                    VAS_POS = VAS_ROW * 3 + VAS_COL - 2
                    MAP.append([VAS_POS, SOURCE[VAS_POS]])
                    self.target.game.put_vase(
                        row=VAS_ROW,
                        col=VAS_COL,
                        vase_type=3,
                        vase_content_type=SOURCE[VAS_POS] // 100,
                        plant_type=SOURCE[VAS_POS] % 100,
                        zombie_type=SOURCE[VAS_POS] % 100,
                        sun_shine_count=random.choice((25, 50, 75))
                    )
        print("VASEs placed.")
        print("MAP: ", MAP)

        time.sleep(wait_time)
        self.target.game.put_zombie(
            zombie_type=1, row=PLA_ROW, col=PLA_COL
        )
        print("FLAG_ZOMBIE zombie placed.")

        self.target.game.put_plant(40, PLA_ROW, 0, 0)
        print("GATLING_PEA plant put.")

        time.sleep(3)
        QUE = random.choice(MAP)
        self.target.game.put_vase(
            row=2,
            col=7,
            vase_type=3,
            vase_content_type=QUE[1] // 100,
            plant_type=QUE[1] % 100,
            zombie_type=QUE[1] % 100,
            sun_shine_count=25
        )
        print("question vase put.")
        input("Press to continue...")

    def left_card_memorize(self):  # 罐子记忆练习
        pass

    def quick_calc(self):  # 算血处理练习
        pass

    def quick_calc_pro(self):  # 快速反应练习
        pass

    def classic_endless(self):  # 经典冲关
        pass

    def sl_endless(self):  # 存档冲关
        pass

    def tool_kit(self):  # 辅助功能
        pass


class Puzzle:  # 珍珑
    def __init__(self, target):
        # 规定操作该珍珑的游戏窗口
        self.target = target
        self.scene = None
        self.islocked = None  # 道具位置是否锁定
        self.items = []
        self.item_rules = [[[]]]  # [[['0'],[罐子样式规则],[项目罗列]], ...]
        self.item_info = [[[]]]

    def ask_import(self):
        while True:
            ans = input("Please import something. ArrayDesign(A) or CSVfiles(C)? ")
            if ans.strip().lower() == "a":
                self.wybzq_import()
                return
            elif ans.strip().lower() == "c":
                self.csv_import()
                return
            print("Invailid input. ", end="")

    def wybzq_import(self):  # 从网页布阵器导入
        self.islocked = True
        # 用户输入基础阵型代码
        code = (input("Please go to http://jspvz.com/ArrayDesign/ to create your lineup and paste the code here: \n")
                .strip().split(','))
        print("processing...")
        try:
            # 从基础阵型代码提取该珍珑的场景信息
            self.scene = [
                2,  # 0to2 pool
                3,  # 1to3 fog
                0,  # 2to0 day
                1,  # 3to1 night
                4,  # 4to4 roof
                # 5   # 5to5 midnight
            ][int(code[0])]
            # 从基础阵型代码提取该珍珑的罐子里内容信息
            self.items = []
            for item in code[1:]:
                item_so = item.strip().split(' ')
                item_num = int(item_so[0], 16)
                if item_num == 7:  # REPEATER plant
                    if len(item_so) > 6 and item_so[6] == '1':  # reversed
                        self.items.append([1, 52, item_so[1], item_so[2]])
                    else:
                        self.items.append([1, 7, item_so[1], item_so[2]])
                elif item_num <= 47:  # plants
                    self.items.append([
                        1,  # 1(plant) or 2(zombie)
                        item_num,  # plant id
                        int(item_so[1]) - 1,  # position row
                        int(item_so[2]) - 1  # position column
                    ])
                elif 80 <= item_num <= 108:  # zombies
                    self.items.append([
                        2,  # 1(plant) or 2(zombie)
                        item_num - 80,  # zombie id
                        int(item_so[1]) - 1,  # position row
                        int(item_so[2]) - 1  # position column
                    ])
                else:
                    print("WARNING: unvalid item %s" % item)
        except IndexError or TypeError:
            print("Bad Code, Please Check.")

    def csv_import(self):  # 从.csv文件中导入阵型设置
        import csv
        self.islocked = False
        with open(file='./imports/rules_set.csv', mode='r') as fr:
            frr = csv.reader(fr)  # file_rules_reader
            items_rules = []  # [[['0'],[罐子样式规则],[项目罗列]], ...]
            cnt = 0
            for row in frr:
                if cnt % 4 == 0:  # 读第一行
                    items_rules.append([[row[0]]])  # 即lineups_set.csv中的编号
                elif cnt % 4 == 1:  # 读第二行
                    items_rules[-1].append(row)  # 罐子样式规则，后期再处理
                else:  # 读第三、四行
                    if cnt % 4 == 2:  # 植物
                        items_rules[-1].append([])  # 初始化该分区所有植物、僵尸罗列列表
                        for item in row:
                            for i in range(int(item[item.find("*")+1:])):
                                items_rules[-1][-1].append(item[:item.find("*")])
                    else:  # 为区分，所有僵尸编号加上50
                        for item in row:
                            for i in range(int(item[item.find("*")+1:])):
                                items_rules[-1][-1].append(str(int(item[:item.find("*")]) + 50))
                cnt += 1
            self.item_rules = items_rules
            print("info: self.items_rules = ", self.item_rules)
        with open(file='./imports/lineups_set.csv', mode='r') as fl:
            flr = csv.reader(fl)  # file_lineups_reader
            source = self.item_rules[:]  # 复制下来规则
            for i in source:  # 打乱
                random.shuffle(i[2])
            items_info = []  # [[['0', 植物/僵尸编号, 花瓶样式], ...] * 5or6]
            cnt = -1
            num_of_lines = 0
            for row in flr:
                if cnt == -1:  # scene
                    if 0 <= int(row[1]) <= 4:
                        self.scene = int(row[1])  # 读第一行第二位
                        num_of_lines = (6 if self.scene == 2 or self.scene == 3 else 5)
                    else:
                        raise IndexError("No scene numbered " + row[1])
                elif cnt < num_of_lines:  # lineup 此时cnt恰好代表行数(0-4or0-5)
                    for sign in row:
                        # 前方高能：rules的翻译和map的绘制
                        info = [sign]
                        for num in range(len(source)):
                            if self.item_rules[num][0][0] == sign:
                                if source[num][2] == []:
                                    break
                                item_id = source[num][2].pop(0)  # 提出待选物品列表中第一项
                                info.append(item_id)
                                vase_style = source[num][1][0]  # e.g. [q,p17@2]
                                info.append({'q': 3, 'p': 4, 'z': 5}[vase_style])  # 先只管第一条规则，其他后面再改
                                break
                        items_info.append(info)
                else:  # error
                    print("WARNING: Invalid lines in lineups_set.csv. Lines after %d will be ignored." % cnt)
                    break
                cnt += 1
            self.item_info = items_info

    def show(self):  # 在self.target中展示该珍珑（需先手动打开场景）
        self.target.game.set_scene(self.scene)
        print("scene set successfully.")
        time.sleep(0.1)

        if self.islocked:
            for item in self.items:
                self.target.game.put_vase(
                    row=item[2],
                    col=item[3],
                    vase_type=3,
                    vase_content_type=item[0],
                    plant_type=item[1],
                    zombie_type=item[1],
                    sun_shine_count=25
                )
            print("items set successfully.")
        else:
            for y in range(6 if self.scene == 2 or self.scene == 3 else 5):
                for x in range(9):
                    pos = y * 9 + x
                    li = self.item_info[pos]
                    if len(li) == 3:
                        self.target.game.put_vase(
                            row=y,
                            col=x,
                            vase_type=li[2],
                            vase_content_type=(int(li[1]) >= 50)+1,
                            plant_type=int(li[1]),
                            zombie_type=int(li[1])-50,
                            sun_shine_count=25
                        )
                    elif len(li) == 1:
                        pass
                    else:
                        raise IndexError


if __name__ == '__main__':
    mutex = win32event.CreateMutex(None, True, "PvZ Toolkit Python")
    if win32api.GetLastError() == 0:
        QCoreApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
        app = QApplication(sys.argv)
        window = PvzToolkit()
        print("waiting for game window...")  # 仅限年度加强版！
        window.game.wait_for_game()
        # window.show()
        # training = Train(window)
        # for i in range(2):
        #     training.plantern_memorize(level=1, wait_time=1)
        puzzling = Puzzle(window)
        puzzling.ask_import()
        puzzling.show()
        # sys.exit(app.exec())
