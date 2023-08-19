import copy
import random
import tkinter                    # UI模块
import tkinter.messagebox         # UI弹窗
from PIL import ImageTk, Image    # 圖片處理

# PIL 为第三方模块，需手动安装
# pip install pillow


class Matrix2048():
    def __init__(self, column: int = 4):
        self.column = column
        self.matrix = [[0 for i in range(column)] for li in range(column)]
        self.history = []
        self.score = 0
        self.init()

    # 生成新的数字
    def generate_number(self):
        matrix = self.matrix
        column = self.column
        # 找出所有为0的位置
        zero = [(x, y) for x in range(column)
                for y in range(column) if matrix[x][y] == 0]
        # 随机选择一个为0的位置并填充为随机数字
        if zero != []:
            x, y = random.choice(zero)
            matrix[x][y] = random.choice([2, 2])

    # 判断游戏是否结束 结束则返回True， 否则返回False
    def gameover(self) -> bool:
        matrix = self.matrix
        column = self.column
        # 1. 矩阵(self.matrix)中有0则未结束
        if 0 in [i for li in matrix for i in li]:
            return False

        # 2. 水平方向上有相同的数字则未结束
        for row in range(column):
            for col in range(column-1):
                if matrix[row][col] == matrix[row][col+1]:
                    return False

        # 3. 垂直方向上有相同的数字则未结束
        for row in range(column-1):
            for col in range(column):
                if matrix[row][col] == matrix[row+1][col]:
                    return False
        return True

    # 游戏初始化 用于新建游戏或重置游戏
    def init(self):
        self.matrix = [[0 for x in range(self.column)]
                       for y in range(self.column)]
        self.generate_number()
        self.generate_number()

        self.history = []
        self.score = 0

    # 移动合并 并记录历史数据
    def matrix_move(self, direction):
        if direction in ['L', 'R', 'D', 'U']:

            # 记录历史
            prev_step = {
                'score': copy.deepcopy(self.score),
                'matrix': copy.deepcopy(self.matrix)
            }
            self.history.append(prev_step)
            # 只记录最近10次
            if len(self.history) > 10:
                self.history = self.history[-10:]
            if direction == 'U':
                self.move_up()
            if direction == 'D':
                self.move_down()
            if direction == 'L':
                self.move_left()
            if direction == 'R':
                self.move_right()

    # 向左移动合并
    def move_left(self):
        column = self.column
        matrix = self.matrix

        # 数字左移
        def move_left_(matrix):
            for row in range(column):
                while 0 in matrix[row]:
                    matrix[row].remove(0)
                while len(matrix[row]) != column:
                    matrix[row].append(0)
            return matrix

        # 数字向左合并
        def merge_left(matrix):
            for row in range(column):
                for col in range(column-1):
                    if matrix[row][col] == matrix[row][col+1] and matrix[row][col] != 0:
                        matrix[row][col] = 2 * matrix[row][col]
                        matrix[row][col+1] = 0
                        self.score = self.score + matrix[row][col]
            return matrix

        matrix = move_left_(matrix)
        matrix = merge_left(matrix)
        self.matrix = move_left_(matrix)

    # 向右移动合并
    def move_right(self):
        self.matrix = [li[::-1] for li in self.matrix]
        self.move_left()
        self.matrix = [li[::-1] for li in self.matrix]

    # 向上移动合并
    def move_up(self):
        column = self.column

        self.matrix = [[self.matrix[x][y]
                        for x in range(column)] for y in range(column)]
        self.move_left()
        self.matrix = [[self.matrix[x][y]
                        for x in range(column)] for y in range(column)]

    # 向下移动合并
    def move_down(self):
        self.matrix = self.matrix[::-1]
        self.move_up()
        self.matrix = self.matrix[::-1]

    # 返回上一步
    def prev_step(self):
        if self.history:
            prev_data = self.history[-1]
            self.score = prev_data['score']
            self.matrix = prev_data['matrix']
            self.history = self.history[0:-1]

    # 命令行显示
    def show(self):
        r = '+-----' * self.column + '+\n'
        for li in self.matrix:
            for i in li:
                s = '|' + ' '*5 if i == 0 else '|' + str(i).center(5, ' ')
                r = r + s
            r = r + '|\n' + '+-----' * self.column + '+\n'
        print(r)


class Window2048():

    def __init__(self, column: int = 4):
        self.init_setting(column)
        self.data = Matrix2048(column)
        self.root = self.init_root()
        self.t = 0  # 判断游戏结束时用
        self.main()

    # 配置初始化
    def init_setting(self, column):
        # 游戏的棋盘的大小，默认为4*4
        self.column = column

        # 棋盘中格子的间隔，单位为px
        self.space_size = 12

        # 棋盘中格子的大小，单位为px
        self.cell_size = 80

        # 用于存储tkinter.Lable对象
        self.emts = []  # 存储lable对象

        # 用于存储游戏的样式信息，如背景色，字体颜色，字体大小等
        self.style = {
            'page': {'bg': '#d6dee0', },
            # 0 ~ 4 灰色系  bg 背景颜色， fg字体颜色， fz字体大小
            0:    {'bg': '#EEEEEE', 'fg': '#EEEEEE', 'fz': 30},
            2**1: {'bg': '#E5E5E5', 'fg': '#707070', 'fz': 30},
            2**2: {'bg': '#D4D4D4', 'fg': '#707070', 'fz': 30},
            # 8 ～ 16 橙色系
            2**3: {'bg': '#FFCC80', 'fg': '#FAFAFA', 'fz': 30},
            2**4: {'bg': '#FFB74D', 'fg': '#FAFAFA', 'fz': 30},
            # 32 ～ 64 红色系
            2**5: {'bg': '#FF7043', 'fg': '#FAFAFA', 'fz': 30},
            2**6: {'bg': '#FF5722', 'fg': '#FAFAFA', 'fz': 30},
            # 128～2048 黄色系
            2**7: {'bg': '#FFEE58', 'fg': '#FAFAFA', 'fz': 30},
            2**8: {'bg': '#FFEB3B', 'fg': '#FAFAFA', 'fz': 30},
            2**9: {'bg': '#FDD835', 'fg': '#FAFAFA', 'fz': 30},
            # 1024~2048 橙色系
            2**10: {'bg': '#FF9800', 'fg': '#FAFAFA', 'fz': 30},
            2**11: {'bg': '#FB8C00', 'fg': '#FAFAFA', 'fz': 28},
            # 4096 +  红色系
            2**12: {'bg': '#fb3030', 'fg': '#FAFAFA', 'fz': 28},
            2**13: {'bg': '#e92e2e', 'fg': '#FAFAFA', 'fz': 28},
            2**14: {'bg': '#da1e1e', 'fg': '#FAFAFA', 'fz': 24},
            # 2**15 +  黑色 超过2**15颜色不再改变
            2**15: {'bg': '#3a3a3a', 'fg': '#E0E0E0', 'fz': 22},
            2**16: {'bg': '#3a3a3a', 'fg': '#E0E0E0', 'fz': 20},
            2**17: {'bg': '#3a3a3a', 'fg': '#E0E0E0', 'fz': 20},
            2**18: {'bg': '#3a3a3a', 'fg': '#E0E0E0', 'fz': 20},
            2**19: {'bg': '#3a3a3a', 'fg': '#E0E0E0', 'fz': 18},
            2**20: {'bg': '#3a3a3a', 'fg': '#E0E0E0', 'fz': 17},
            2**21: {'bg': '#3a3a3a', 'fg': '#E0E0E0', 'fz': 16},
            2**22: {'bg': '#3a3a3a', 'fg': '#E0E0E0', 'fz': 15},
            2**23: {'bg': '#3a3a3a', 'fg': '#E0E0E0', 'fz': 14},
            2**24: {'bg': '#3a3a3a', 'fg': '#E0E0E0', 'fz': 13},
            2**25: {'bg': '#3a3a3a', 'fg': '#E0E0E0', 'fz': 12},
        }

    # 窗口初始化
    def init_root(self):
        column = self.column
        space_size = self.space_size
        cell_size = self.cell_size

        # 创建根窗口
        root = tkinter.Tk()
        root.title('2048')

        # 根窗口尺寸设置
        window_w = column * (space_size + cell_size) + space_size
        window_h = window_w + cell_size + 2 * space_size
        root.geometry('{}x{}'.format(window_w, window_h))

        # 顶栏
        header_h = cell_size + space_size * 2
        header = tkinter.Frame(root, height=header_h, width=window_w)
        self.init_header(header)

        # 棋盘
        table = tkinter.Frame(root, height=window_w, width=window_w)
        self.init_table(table)

        return root

    # 顶栏初始化
    def init_header(self, master):
        master['bg'] = self.style['page']['bg']
        # 分数
        emt_score = tkinter.Label(master, bd=0)
        emt_score['fg'] = '#707070'
        emt_score['bg'] = self.style['page']['bg']
        emt_score['font'] = ("黑体", 30, "bold")
        img = Image.new('RGB', (self.cell_size, self.cell_size),
                        self.style['page']['bg'])
        img = ImageTk.PhotoImage(img)
        emt_score.configure(image=img)
        emt_score['image'] = img

        emt_score['text'] = 'score:' + str(self.data.score)
        emt_score['compound'] = 'center'
        self.emt_score = emt_score
        emt_score.place(x=15, y=15)
        master.pack()

    # 棋盘初始化
    def init_table(self, master):
        column = self.column
        cell_size = self.cell_size
        space_size = self.space_size

        master['bg'] = self.style['page']['bg']

        # 创建棋盘子元素
        emts = [[0 for x in range(column)] for y in range(column)]
        for row in range(column):
            for col in range(column):
                emt = tkinter.Label(master, bd=0)
                emt['width'] = self.cell_size
                emt['height'] = self.cell_size
                emt['text'] = ''
                emt['compound'] = 'center'

                y = space_size + (cell_size + space_size) * row
                x = space_size + (cell_size + space_size) * col

                emt.place(x=x, y=y)
                emts[row][col] = emt
        self.emts = emts
        master.pack()

    # 更新UI数据
    def update_ui(self):
        def update_score():
            img = Image.new(
                'RGB', (self.cell_size, self.cell_size), self.style['page']['bg'])
            img = ImageTk.PhotoImage(img)
            self.emt_score.configure(image=img)
            self.emt_score['image'] = img

            self.emt_score['text'] = 'score:' + str(self.data.score)
        update_score()
        matrix = self.data.matrix
        for row in range(self.column):
            for col in range(self.column):
                num = matrix[row][col]
                emt = self.emts[row][col]
                img = Image.new(
                    'RGB', (self.cell_size, self.cell_size), self.style[num]['bg'])
                img = ImageTk.PhotoImage(img)
                emt.configure(image=img)
                emt['fg'] = self.style[num]['fg']
                emt['bg'] = self.style[num]['bg']
                emt['image'] = img
                emt['font'] = ("黑体", self.style[num]['fz'], "bold")
                emt['text'] = str(num) if num != 0 else ''

    # 事件循环
    def key_event(self, event):
        # print(f"键盘输入:{ event.keysym }, ASCII码:{ event.keycode }")
        # 注意：在不同系统下的同一按键的keycode可能不同
        if event.keysym in ['Up', 'w', 'Down', 's', 'Left', 'a', 'Right', 'd']:
            if event.keysym in ['Up', 'w']:    # 向上
                self.data.matrix_move('U')
            elif event.keysym in ['Down', 's']:  # 向下
                self.data.matrix_move('D')
            elif event.keysym in ['Left', 'a']:  # 向左
                self.data.matrix_move('L')
            elif event.keysym in ['Right', 'd']:  # 向右
                self.data.matrix_move('R')
            self.data.generate_number()

        # 按z 返回上一步
        if event.keysym == 'z':
            if self.data.history != []:
                self.data.prev_step()
        self.update_ui()

        # 重置游戏
        def reset_game():
            self.t = 0
            self.data.init()
            self.update_ui()

        if self.data.gameover() is True:
            # 直接结束显式存在问题，显示的是上次的数据
            if self.t == 0:
                self.t = 1
            else:
                res = tkinter.messagebox.askyesno(
                    title="2048", message="Game Over!\n是否重新開始!")
                if res is True:
                    reset_game()
                else:
                    self.root.quit()

    # 重置游戏
    def reset_game(self):
        self.t = 0
        self.data.init()
        self.update_ui()

    # 主程序
    def main(self):
        self.update_ui()

        # 绑定键盘事件
        self.root.bind('<Key>', self.key_event)

        # 主循环
        self.root.mainloop()


g = Window2048(4)
