#更新新词库到本地。
import asyncio
import time
from multiprocessing.pool import Pool
import aiohttp

def sync_local_new_words():
    """
    请求api获取新词库。
    :return: 无。
    """
    main_get_html()
    main_parse_html()

#收集请求的内容
new_words_text_list=[]

# 信号量，控制协程数，防止爬的过快
sem = asyncio.Semaphore(5)
async def get_text(url,num):
    async with(sem):
        # async with是异步上下文管理器
        async with aiohttp.ClientSession() as session:  # 获取session
            async with session.request('GET', url) as resp:  # 提出请求
                new_words_text= await resp.text()
                new_words_text_list.append([new_words_text,num])

#解析请求的内容
def multi_parse_html(new_words_text,num):
    category_chinese = ["互联网", "动物", "财经", "汽车", "成语","地名", "食物", "法律", "历史名人", "医学", "诗词"]
    pattern= compile("(.*?)[ ]*\t[ ]*\d+[\r\n]")
    new_words_list=pattern.findall(new_words_text)
    tmp_list = []
    for new_word in new_words_list:
        tmp_new_word="".join([new_word,"\n"])
        tmp_list.append(tmp_new_word)
    tmp_list[-1]=tmp_list[-1].strip("\n")
    new_words_dict_path="C:\\Users\\Administrator\PycharmProjects\\anki_cloze_maker\\anki_cloze_maker\\res\\new_words_dict"
    path="".join([new_words_dict_path,"\\",category_chinese[num], ".txt"])
    with open(path, "w",encoding="utf-8") as f:
        f.writelines(tmp_list)

#多进程处理内容
def main_parse_html():
    p = Pool(4)
    for  i in new_words_text_list:
        p.apply_async(multi_parse_html,args=(i[0],i[1]))
    p.close()
    p.join()

#协程请求
def main_get_html():
    category=["IT","animal","caijing","car","chengyu","diming","food","law","lishimingren","medical","poem"]

    # 获取事件循环
    loop = asyncio .get_event_loop()
    # 把所有任务放到一个列表中
    tasks = [get_text("".join(["https://raw.github.com/thunlp/THUOCL/master/data", "/THUOCL_", category[i], ".txt"]),i) for  i in range(len(category))]
    # 激活协程
    loop.run_until_complete(asyncio.wait(tasks))
    # 关闭事件循环
    loop.close()

if __name__=="__main__":
    time_start = time.time()
    sync_local_new_words()
    time_end = time.time()
    print(time_end-time_start)