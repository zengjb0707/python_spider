import requests
import json
import time
import csv


def create_csv():
    '''
    创建保存评论的 csv
    :return:
    '''
    with open('../data/comments.csv','w+',newline='',encoding='utf8') as f:
        writer = csv.writer(f)
        head = ['ID','评论时间','评论星级','评论内容']
        writer.writerow(head)


def get_comments(params):
    '''
    请求 html
    :param params: url 带的参数
    :return: json 解析后的评论数据的列表
    '''
    url = 'https://www.meituan.com/ptapi/poi/getcomment'
    headers = {
        'Cookie' : '_lxsdk_cuid=17200c47d4c8f-06e96f15fb99ad-d373666-e1000-17200c47d4dc8; iuuid=6FC309D7107BB6918F04158FCB10A4FB820878DEF00E064A289206656CCEDB58; _lxsdk=6FC309D7107BB6918F04158FCB10A4FB820878DEF00E064A289206656CCEDB58; __mta=154433415.1595297842208.1595297842208.1595297842208.1; ci=107; rvct=107; uuid=49599086a35d420ab752.1595297927.1.0.0; mtcdn=K; lsu=; _lx_utm=utm_source%3Dgoogle%26utm_medium%3Dorganic',
        'Host' : 'www.meituan.com',
        'Referer' : 'https://www.meituan.com/zhoubianyou/94502860/',
        'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36'
    }
    response = requests.get(url,headers=headers,params=params)
    comments = json.loads(response.text)['comments']
    return comments


def write_to_csv(comments):
    '''
    保存进 csv
    :param comments: 评论内容
    :return:
    '''
    with open('../data/comments.csv','a+',newline='',encoding='utf8') as f:
        writer = csv.writer(f)
        for c in comments:
            data = [c['reviewId'],c['commentTime'],c['star'],c['comment']]
            writer.writerow(data)


if __name__ == '__main__':
    create_csv()
    for i in range(0,1671,10):
        params = {
            'id': 94502860,
            'offset': i,
            'pageSize': 10,
            'mode': 0,
            'tarRange': '',
            'userId': '',
            'sortType': 1
        }
        comments = get_comments(params)
        write_to_csv(comments)
        time.sleep(1)
        page = i // 10 + 1
        print('已爬取 %s 页' % str(page))
