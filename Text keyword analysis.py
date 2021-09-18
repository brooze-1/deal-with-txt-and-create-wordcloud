# 开发时间：2021/9/18  9:15
import jieba
from wordcloud import WordCloud
from scipy.misc import imread
class TKA(object):
    def __init__(self,filename,len_keywords=3,list_keywords=10,img_template="词云模板2.png",up_or_down=True,create_png=False):
        # 注意传入的文件类型参数要是txt类型
        self.filename=filename
        file = open("wait_to_analysis/"+self.filename,"r",encoding="utf-8")
        self.content = file.read()
        # len_keywords(int)参数是用于筛选关键字长度大于等于len_keywords的关键字,默认值为3
        self.len_keywords=len_keywords
        # list_keywords(int)参数是默认的展示条数以及存储条数，默认值为10
        self.list_keywords=list_keywords
        # up_or_down(bool)参数用来选择是升序排列还是降序排列(up_or_down的类型是bool类型)，传入True表示升序,传入False表示降序，默认是True
        self.up_or_down=up_or_down
        # img_templates(.png)参数用于接受生成词云的模板
        self.img_templates = "img_wordcloud/"+img_template
        # create_png(bool)参数用来选择是否要生成词云，默认是False
        self.create_png = create_png
        # self.d用于临时存储解析的文本
        self.d={}

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
        self.tmp_items = list(self.d)
        # print(self.tmp_items)
        # 按照关键字出现的次数进行关键字的排序
        self.items.sort(key=lambda x:x[1],reverse=self.up_or_down)

    # 输出分析结果
    def input(self):
        for i in range(self.list_keywords):
            k,v = self.items[i]
            if i<self.list_keywords - 1:
                print("{}:{}".format(k,v),end=",")
            else:
                print("{}:{}".format(k,v))

    # 将分析结果存储至文件中
    def up_to_file(self):
        # 处理filename
        self.filename = "(Text keyword analysis).".join(self.filename.split("."))
        f1=open("analysis_result/"+self.filename,"w",encoding="utf-8")
        for i in range(self.list_keywords):
            k,v = self.items[i]
            f1.write("{}:{}\n".format(k,v))
        f1.close()

    # 生成词云
    def WC(self):
        if self.create_png:
            lines = " ".join(self.tmp_items)
            mask = imread(self.img_templates)
            wc = WordCloud(font_path="词云字体/simhei.ttf", max_font_size=80, mask=mask).generate(lines)
            wc.to_file("img_wordcloud/词云效果（{}）.png".format(self.filename.split(".")[0]))
        else:
            return

    # 主函数
    def main(self):
        self.Parse_text()
        self.sort_content()
        self.input()
        self.up_to_file()
        self.WC()


if __name__=="__main__":
    obj = TKA(filename="一种用于餐厅的机器人路径规划方法.txt",len_keywords=2,list_keywords=100,create_png=True)
    obj.main()