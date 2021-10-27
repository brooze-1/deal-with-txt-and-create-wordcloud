# 开发时间：2021/9/18  9:15
# coding:utf-8
import jieba
from wordcloud import WordCloud
from scipy.misc import imread
from matplotlib import colors

class TKA(object):
    def __init__(self,filename,color_list,color_sizes="black",len_keywords=3,list_keywords=10,max_font_size=40,img_templates="cat.png",up_or_down=True,create_png=False):
        # 注意传入的文件类型参数要是txt类型
        self.filename=filename
        file = open("wait_to_analysis/"+self.filename,"r",encoding="utf-8")
        self.content = file.read()
        file.close()
        # len_keywords(int)参数是用于筛选关键字长度大于等于len_keywords的关键字,默认值为3
        self.len_keywords=len_keywords
        # list_keywords(int)参数是默认的展示条数以及存储条数，默认值为10
        self.list_keywords=list_keywords
        # up_or_down(bool)参数用来选择是升序排列还是降序排列(up_or_down的类型是bool类型)，传入True表示升序,传入False表示降序，默认是True
        self.up_or_down=up_or_down
        # img_templates(.png)参数用于接受生成词云的模板，声明img_template支持传入列表
        self.img_templates = img_templates
        # create_png(bool)参数用来选择是否要生成词云，默认是False
        self.create_png = create_png
        # self.d用于临时存储解析的文本
        self.d={}
        # 用于存放色号,声明color_sizes支持传入列表 self.color_size适用于存放背景板的颜色 背景板需求的颜色格式是(221,204,210)这样的rgb格式 传入的对象是列表对象(list)
        self.color_sizes = color_sizes
        # font_size用于确定形成的词云的字体大小 默认大小等于30
        self.max_font_size=max_font_size
        # 建立字体颜色数组 传入的是列表对象(list)
        self.color_list = color_list
        # self.color_temp用于存储self.color_list转换好的色号   (221,204,210) => '#DDCCD2' 将rgb色号转成16进制  转换成16进制是因为字体需求的颜色样式是16进制
        self.color_temp = []



    # 解析文本获取关键字及其出现次数
    def Parse_text(self):
        # 使用jieba库的lcut方法对文本内容进行分词，生成列表对象
        words = jieba.lcut(self.content)
        for word in words:
            # 若关键字长度小于len_keywords则跳过
            if len(word) < self.len_keywords:
                continue
            # 关键字长度大于等于len_keywords时，则存储至临时字典d中
            else:
                self.d[word] = self.d.get(word,0) + 1


    # 对关键字进行排序
    def sort_content(self):
        # 生成列表对象
        self.items = list(self.d.items()) # 形如[("jason",8),("egon",6)...]
        # print(self.items)
        # print(len(self.items))
        self.tmp_items = list(self.d)
        # print(self.tmp_items)
        # 按照关键字出现的次数进行关键字的排序
        self.items.sort(key=lambda x:x[1],reverse=self.up_or_down)

    # 输出分析结果
    def input(self):
        # list_keywords(int)参数是默认的展示条数以及存储条数当真实数据条数小于list_keywords，将数据的长度赋值给list_key_words
        if len(self.items) < self.list_keywords:
            self.list_keywords = len(self.items)
        for i in range(self.list_keywords):
            k,v = self.items[i]
            if i<self.list_keywords - 1:
                print("{}:{}".format(k,v),end=",")
            else:
                print("{}:{}".format(k,v))

    # 将分析结果存储至文件中
    def up_to_file(self):
        # 处理filename
        self.filename = ".".join(self.filename.split("."))
        f1=open("analysis_result/"+self.filename,"w",encoding="utf-8")
        if len(self.items) < self.list_keywords:
            self.list_keywords = len(self.items)
        for i in range(self.list_keywords):
            k,v = self.items[i]
            f1.write("{}:{}\n".format(k,v))
        f1.close()

    # 当self.img_templates传入的是列表时，判断传入的color_sizes是列表还是字符串
    def judge_color_sizes(self,img_template,lines):
        mask = imread("img_template/" + img_template)
        # 当传入的color_sizes是列表时
        if type(self.color_sizes)==list:
            # 遍历改变背景颜色
            for color in self.color_sizes:
                wc = WordCloud(background_color=color, font_path="词云字体/simhei.ttf", max_font_size=self.max_font_size,
                               mask=mask,colormap=self.colormap).generate(lines)
                # 文件命名方式：文件名+词云字体大小+使用的词云模板名+背景色号
                wc.to_file("img_result/{}({}{}{}).png".format(self.filename.split(".")[0],self.max_font_size,img_template.split(".")[0],color))
        else:
            # 当传入的color_sizes是字符串时
            wc = WordCloud(background_color=self.color_sizes, font_path="词云字体/simhei.ttf", max_font_size=self.max_font_size,
                           mask=mask,colormap=self.colormap).generate(lines)
            # 文件命名方式：文件名+词云字体大小+使用的词云模板名+背景色号
            wc.to_file("img_result/{}({}{}{}).png".format(self.filename.split(".")[0],self.max_font_size,img_template.split(".")[0],self.color_sizes))

    # 当self.img_templates传入的是字符串时判断传入的color_sizes是列表还是字符串
    def judge_color_sizes2(self,lines):
        mask = imread("img_template/" + self.img_templates)
        # 当传入的color_sizes是列表时
        if type(self.color_sizes)==list:
            # 遍历改变背景颜色
            for color in self.color_sizes:
                wc = WordCloud(background_color=color, font_path="词云字体/simhei.ttf", max_font_size=self.max_font_size,
                               mask=mask,colormap=self.colormap).generate(lines)
                # 文件命名方式：文件名+词云字体大小+使用的词云模板名+背景色号
                wc.to_file("img_result/{}({}{}{}).png".format(self.filename.split(".")[0],self.max_font_size,self.img_templates.split(".")[0],color))
        else:
            # 当传入的color_sizes是字符串时
            wc = WordCloud(background_color=self.color_sizes, font_path="词云字体/simhei.ttf", max_font_size=self.max_font_size,
                           mask=mask,colormap=self.colormap).generate(lines)
            # 文件命名方式：文件名+词云字体大小+使用的词云模板名+背景色号
            wc.to_file("img_result/{}({}{}{}).png".format(self.filename.split(".")[0],self.max_font_size,self.img_templates.split(".")[0],self.color_sizes))

    # 生成词云
    def WC(self):
        if self.create_png:
            # 转化为ListedColormap对象作为字体颜色的参数传入
            self.colormap = colors.ListedColormap(self.color_temp)
            # lines = " ".join(self.tmp_items)
            # print(lines)
            # lines = """朱宛君 雷子怡 黄旦 曾丽雯 陈慧琦 付春天 陈远豪 任步月 朱臣臣 林鹏飞 胡祖鹏 熊屹 熊正坤 陈威志 周世浩 邓泽威 黄伟成 刘梓为 戴庆旺 敖宇翔 雷强 简豪欣 张家豪 王浩然 王俊杰 余兆聪 王月聪 郝书乐 马旭 吴欣睿 杨家华 张万平 吴柏沙 张乐新 熊景琦 付新宇 张晨 龙晶晶 范茗艺 赵荷曦 李辰柱 杨子雄 朱震宇 刘昀鑫 王景阳 成泽申 刘志 桂进杰 汪文轩 胡成 彭勇辉 易球 聂广远 申豪 李品行 刘禹宏 涂英东 彭奕霖 郭开成 史启良 朱环宇 牟航 吴鸿南 刘叙 吴佳乐 汪骏 鞠云龙 梁树泉 黄冰"""
            lines = """陈慧琦 付春天 朱宛君 雷子怡 胡成 彭勇辉 刘昀鑫 王俊杰 余兆聪 王月聪 易球 聂广远 申豪 雷强 简豪欣 林鹏飞 刘叙 吴佳乐 汪骏 鞠云龙 梁树泉 黄冰 黄伟成 刘梓为 戴庆旺 敖宇翔 陈远豪 任步月 朱臣臣 张家豪 王浩然 张晨 龙晶晶 范茗艺 赵荷曦 李辰柱 杨子雄 朱震宇 郝书乐 马旭 吴欣睿 杨家华 张万平 吴柏沙 张乐新 熊景琦 付新宇 王景阳 成泽申 刘志 黄旦 曾丽雯 桂进杰 汪文轩 胡祖鹏 熊屹 熊正坤 陈威志 周世浩 邓泽威 李品行 刘禹宏 涂英东 彭奕霖 郭开成 史启良 朱环宇 牟航 吴鸿南"""
            # 当传入self.img_templates是个列表时进行判断(即传入了多个模板图片时)
            if type(self.img_templates)==list:
                # 对传入的图片进行循环
                for img_template in self.img_templates:
                    # mask = imread("img_template/"+img_template)
                    # # 莫兰迪配色 (104,84,85) (164,164,164)
                    # wc = WordCloud(background_color=(104,84,85),font_path="词云字体/simhei.ttf", max_font_size=50, mask=mask).generate(lines)
                    # # 文件命名方式：文件名+使用的词云模板名
                    # wc.to_file("img_result/{}({}).png".format(self.filename.split(".")[0],img_template.split(".")[0]))
                    self.judge_color_sizes(img_template,lines)
            # 当只传入了一个图片时
            else:
                # mask = imread("img_template/"+self.img_templates)
                # wc = WordCloud(background_color=(104,84,85),font_path="词云字体/simhei.ttf", max_font_size=50, mask=mask).generate(lines)
                # wc.to_file("img_result/{}({}).png".format(self.filename.split(".")[0],self.img_templates.split(".")[0]))
                self.judge_color_sizes2(lines)
        else:
            return

    # (221,204,210) => '#DDCCD2' 将rgb色号转成16进制
    def Color_to_color_value(self,value):
        digit = list(map(str, range(10))) + list("ABCDEF")
        if isinstance(value, tuple):
            string = '#'
            for i in value:
                a1 = i // 16
                a2 = i % 16
                string += digit[a1] + digit[a2]
            return string
        elif isinstance(value, str):
            a1 = digit.index(value[1]) * 16 + digit.index(value[2])
            a2 = digit.index(value[3]) * 16 + digit.index(value[4])
            a3 = digit.index(value[5]) * 16 + digit.index(value[6])
            return (a1, a2, a3)

    # 重复操作Color_to_color_value()函数直至列表中所有的色号都转成16进制
    def repeated_color_convert(self):
        # 遍历将color_list中的rgb色号都转换成16进制存储至color_temp中
        for col in self.color_list:
            self.color_temp.append(self.Color_to_color_value(col))


    # 主函数
    def main(self):
        self.Parse_text()
        self.sort_content()
        self.input()
        self.up_to_file()
        self.repeated_color_convert()
        self.WC()


if __name__=="__main__":
    # 莫兰迪配色色号列表
    # color_sizes = [
    #         (221,204,210),(213,208,204),(237,209,205),(166,126,126),(240,228,250),(201,192,213),
    #         (104,98,98),(222,216,216),(104,84,85),(148,86,87),(125,114,131),(164,164,164),
    #     (199,195,185),(240,235,231),(184,197,179),(225,227,226),(179,174,180),(193,201,214),
    #     (255,251,240),(242,236,238),(164,150,137),(180,176,164),(249,233,220),(219,213,213),
    #     (195,189,189),(148,148,146),(199,183,170),(215,201,175),(244,239,233),(254,251,236),
    #     (199,180,166),(251,234,216),(120,138,116),(152,161,142),(160,167,186),(135,151,164)
    #               ]

    # color_sizes存储用于背景板的颜色
    color_sizes = [
        (60,112,126),(79,96,112),(122,103,131),(116,114,93),
        (176,172,171),(82,68,68),(114,156,170),(80,84,111),
        (40,112,136),(117,169,183),(189,170,140),(121,136,143),
        (29,29,37),(208,66,52)
    ]
    # color_list存储用于词云字体的颜色
    color_list = [
        (221, 204, 210), (213, 208, 204), (237, 209, 205), (166, 126, 126), (240, 228, 250), (201, 192, 213),
        (104, 98, 98), (222, 216, 216), (104, 84, 85), (148, 86, 87), (125, 114, 131), (164, 164, 164),
        (199, 195, 185), (240, 235, 231), (184, 197, 179), (225, 227, 226), (179, 174, 180), (193, 201, 214),
        (255, 251, 240), (242, 236, 238), (164, 150, 137), (180, 176, 164), (249, 233, 220), (219, 213, 213),
        (195, 189, 189), (148, 148, 146), (199, 183, 170), (215, 201, 175), (244, 239, 233), (254, 251, 236),
        (199, 180, 166), (251, 234, 216), (120, 138, 116), (152, 161, 142), (160, 167, 186), (135, 151, 164)
    ]

    # color_sizes = [(104,98,98),(222,216,216),(104,84,85),(148,86,87),(125,114,131),(164,164,164)]
    # obj = TKA(filename="name.txt",color_list=color_list,color_sizes=color_sizes,len_keywords=2,list_keywords=10,create_png=True,img_templates=["ai.png"])
    # obj.main()
    print(TKA.__dict__)
    print(dir(TKA))

