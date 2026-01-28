


'''
用python编写一个爬虫程序
访问下面的页面
https://mp.weixin.qq.com/s/GlXsn5sthTRl3w57cVGn2g

该页面中, 有很多链接, 每个链接的地址, 都以https://mp.weixin.qq.com/ 开头

这每个链接中的页面上, 都有一个夸克网盘资源的链接, 地址是以 https://pan.quark.cn/ 开头的.  比如 https://pan.quark.cn/s/1897479db916  ,  https://pan.quark.cn/s/221f9aada350  这样的地址.

请把所有链接中的这个夸克网盘资源地址, 提取出来.

注意: 为了防止爬虫被封杀, 请每爬一次, 就随机暂停500-1000毫秒之间的时间.

'''


import requests
from bs4 import BeautifulSoup
import time
import random
import re
from urllib.parse import urljoin


def get_quark_links():
    # 设置请求头
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36',
        'Referer': 'https://mp.weixin.qq.com/'
    }

    # 第一步：获取主页面内容
    main_url = 'https://mp.weixin.qq.com/s/GlXsn5sthTRl3w57cVGn2g'

    try:
        response = requests.get(main_url, headers=headers, timeout=10)
        response.raise_for_status()
    except Exception as e:
        print(f"主页面请求失败: {e}")
        return []

    # 解析主页面获取所有微信文章链接
    soup = BeautifulSoup(response.text, 'html.parser')
    wechat_links = set()

    # 查找所有包含微信链接的a标签
    for a in soup.find_all('a', href=True):
        full_url = urljoin(main_url, a['href'])
        if full_url.startswith('https://mp.weixin.qq.com/'):
            wechat_links.add(full_url)

    print(f"共发现 {len(wechat_links)} 篇微信文章")

    # 第二步：遍历所有微信文章获取夸克链接
    quark_pattern = re.compile(r'https://pan\.quark\.cn/[^\s>"\'\)]+')
    all_quark_links = set()

    for idx, article_url in enumerate(wechat_links, 1):
        print(f"正在处理第 {idx}/{len(wechat_links)} 篇文章")

        try:
            # 随机延迟（500-1000毫秒）
            time.sleep(random.uniform(0.5, 1))

            # 请求微信文章页面
            article_response = requests.get(article_url, headers=headers, timeout=10)
            article_response.raise_for_status()

            # 两种方式查找夸克链接：
            # 方式1：通过正则表达式全文搜索
            matches = quark_pattern.findall(article_response.text)
            # 方式2：通过解析HTML标签
            soup = BeautifulSoup(article_response.text, 'html.parser')
            for a in soup.find_all('a', href=True):
                if a['href'].startswith('https://pan.quark.cn/'):
                    matches.append(a['href'])

            # 去重处理
            for link in matches:
                clean_link = re.sub(r'[&?]from=[^&]+', '', link)  # 清理跟踪参数
                all_quark_links.add(clean_link.split('#')[0])  # 去除锚点

        except Exception as e:
            print(f"处理文章失败 [{article_url}]: {e}")

    return sorted(all_quark_links)


if __name__ == "__main__":
    start_time = time.time()
    print("程序启动，开始爬取...")

    result = get_quark_links()

    print("\n最终发现的夸克网盘链接：")
    for i, link in enumerate(result, 1):
        print(f"{i}. {link}")

    print(f"\n总计发现 {len(result)} 个有效链接")
    print(f"程序运行耗时：{time.time() - start_time:.2f}秒")