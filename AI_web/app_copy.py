# -*- coding: utf-8 -*-
from __future__ import unicode_literals  # 头部加上这句
from flask import render_template, make_response, request
from flask import Flask
from flask.helpers import send_file
from data_transform_ch import pre_process_main

import math
import jieba
import os
import zipfile
import json
import sys
import re
reload(sys)
sys.setdefaultencoding('utf-8')

app = Flask(__name__)


@app.route('/')
@app.route('/index')
def index():
    return render_template("index1.html")

@app.route('/sstm_run', methods=['GET', 'POST'])
def test():
    topic = request.values['topic']
    iter = request.values['iter']
    emotion_dict = request.values['emotion_dict']
    article = request.values['article']
    article = str(article)
    # article_list = article.split('\d')
    article_list = re.split(r'[0-9]+\s', article)
    if len(article_list) > 1:
        article_list = article_list[1:]
    article_list = [str(a) for a in article_list]
    article_num = len(article_list)
    pre_process_main(article_list)

    command = 'cd ./SSTM++/src && ./main -ntopics ' + topic + ' -niters ' + iter + ' -doc_dir ../dataset/preProcessedData -output_dir res'
    if emotion_dict != 'non-emotion':
        command = command + ' -lexicon_dir ../lexicon/' + emotion_dict
    print("run command", command)
    respond = os.system(command)
    print(command)
    print(respond)
    print('##################')
    print('{:.6f}'.format(float(50/float(topic))))
    alpha = '{:.6f}'.format(float(50/float(topic)))
    emotion_to_num = {'BingLiu':'2','HashtagSentimentAffLexNegLex':'2','NRC-emotion-lexicon-wordlevel':'2','NRC-Hashtag-Sentiment-Lexicon-v0.1':'2',\
                      'paradigm+':'2','SCL-NMA':'2','SCL-OPP':'2','SemEval2015-English-Twitter-Lexicon':'2','Sentiment140-Lexicon-v0.1':'2',\
                      'Sentiment140AffLexNegLex':'2','SentiWordNet3':'2','subjectivity_clues_hltemnlp05':'2','non-emotion':'0','ANTUSD':'2',\
                      'HowNet':'2','NRC':'2','tsinghua':'2'}

    path = './SSTM++/src/res/assignment_est_ntopics'+topic+'_nsentis2('+emotion_to_num[emotion_dict]+')_niters'+iter+'_alpha'+alpha+'_gamma1.000000_betas0.0010000.1000000.000000.txt'
    doc_path = './SSTM++/src/res/doc_senti_prob_est_ntopics'+topic+'_nsentis2('+ emotion_to_num[emotion_dict] +')_niters'+iter+'_alpha'+alpha+'_gamma1.000000_betas0.0010000.1000000.000000.txt'
    topic_path = './SSTM++/src/res/top30_words_est_ntopics'+topic+'_nsentis2('+emotion_to_num[emotion_dict]+')_niters'+iter+'_alpha'+alpha+'_gamma1.000000_betas0.0010000.1000000.000000.txt'
    fs = open(path)
    sstm_results = {}
    for x,line in enumerate(fs):
        if x >= article_num:
            break
        #print(line)
        sents = line.split('\t\t')
        sstm_result = {}
        sents_num = 0
        for y,s in enumerate(sents):
            s = s.strip()
            if s == '\n' or s == '' or s == '\t':
                continue
            print(s)
            sstm_result['句子'+str(y+1)] = s
            sents_num = y
        sstm_result['sents_num'] = str(sents_num+1)
        sstm_results['文章'+str(x+1)] = sstm_result
        print(sstm_result['sents_num'])
        print(sstm_results['文章'+str(x+1)])
        print('*****')
        #sstm_results[str(x+1)] = sstm_results
    sstm_results['article_num']=str(article_num)
    doc_fs = open(doc_path)
    for x,line in enumerate(doc_fs):
        if x >= article_num:
            break
        prob = line.split(' ')
        if prob[0] < prob[1]:
            sstm_results['文章情感'+str(x+1)] = '正面'
        elif prob[0] > prob[1]:
            sstm_results['文章情感'+str(x+1)] = '负面'
        elif prob[0] == prob[1]:
            sstm_results['文章情感'+str(x+1)] = '中立'

    topic_fs = open(topic_path)
    topic_num = 0
    sentiment_num = 0
    topic_word_num = 0

    for x,line in enumerate(topic_fs):

        if line[:5] == 'Topic':
            tmp_list = line.split('#')
            topic_num = tmp_list[1][0]
            sentiment_num = tmp_list[2][0]
            topic_word_num = 0
        else:
            topic_word_num += 1
            line = line.decode('utf-8')
            line = line.strip()
            tmp_list = line.split(' ')
            sstm_results['主题'+topic_num+'情感'+sentiment_num+'主题词'+str(topic_word_num)] = tmp_list[0]
            sstm_results['主题'+topic_num+'情感'+sentiment_num+'主题词'+str(topic_word_num)+'概率'] = tmp_list[1]
    sstm_results['topic_num'] = topic_num
    print('#######')
    print(sstm_results)
    sstm_results = json.dumps(sstm_results,ensure_ascii=False)
    #result = "success"
    rst = make_response(sstm_results)
    rst.headers['Access-Control-Allow-Origin'] = '*'
    return rst

@app.route('/sstm_dataset/<file_name>',  methods=['GET'])
def sstm_dataset(file_name = None):
    file_name = file_name+'.zip'
    #path = "./SSTM++/lexicon/"+file_name
    abs_path = os.getcwd()+"/SSTM++/lexicon/"+file_name
    # 判断文件是否存在
    if os.path.exists(abs_path):
        response = make_response(send_file(abs_path))
        download_name = "attachment; filename=" + file_name
        response.headers["Content-Disposition"] = download_name
        return response
    else:
        msg = "文件" + file_name + "不存在，请返回"
        return msg

#夏天穿情侣装情侣鞋红色荧光色蓝色点击情侣网鞋网页链接网页各式各样照片墙想拥有照片墙童鞋要收动手美美家地址
#早上懒床绝招够玩坏一集万美金坑子拍百把集中国长城请鳗鱼吃官方水管轉發浮云
#[1;1870;1383213600;0.0,1.0]苏宁易购精品陶瓷感恩季大力支持，希望好运垂怜我，让我中个吧。太期待了！地址网页：成都现代舞剧太极传奇，支持你们举行好活动，坚持抽奖，我肯定会中的，相信老天是公平的。
#地址网页：寻找密净准， 朋友不必很多，知心就好，牵挂不必很多，动情就好，地址网页：网上购机票，支付用建行参加活动的同时，让我们一同分享快乐生活期待好运气。
#[0;5004;1378767085;0.8888888888888888,0.1111111111111111]田亮，我可不是挑事儿的人，我要是你我就撒泼打滚，嚎啕大哭，明明就木有情感野史，处女座在此，快来黑一黑。
@app.route('/latot_run', methods=['GET', 'POST'])
def latot_run():
    topic = request.values['topic']
    iter = request.values['iter']
    article = request.values['article']
    article = str(article)
    article_list = article.split('#')

    test_dir = os.getcwd()+"/LATOT/result/less"
    article_num = latot_modify_file(article_list, test_dir)
    filename = "test1.test"
    command = "cd LATOT && java -jar LATOTE.jar -inf -alpha 0.5 -beta 0.1 -ntopics " + topic + " -niters " + iter+" -twords 100 -dir "+test_dir+" -dfile " + filename + " -model trainModel -inftrainfile train"
    print(command)
    os.system(command)

    latot_results = {}
    for i, line in enumerate(open(os.getcwd()+"/LATOT/result/result")):
        if i >= article_num:
            break
        emotion_index = line.find('predictEmotion: ')
        emotion = line[emotion_index+len('predictEmotion: ')]
        article_and_emotion = ""
        article = article_list[i + 1].strip()
        if emotion == '0':
            article_and_emotion = "文章"+str(i+1)+": "+article+'\n'+'情感类型： 负面 \n'
        else:
            article_and_emotion = "文章" + str(i+1) + ": " + article+'\n' + '情感类型： 正面 \n'
        #print(article_and_emotion)
        latot_results[str(i)] = article_and_emotion
    latot_results["article_num"] = str(article_num)
    latot_results = json.dumps(latot_results,ensure_ascii=False)
    rst = make_response(latot_results)
    rst.headers['Access-Control-Allow-Origin'] = '*'
    return rst

def latot_modify_file(article_list,path):

    texts = []
    for article in article_list:
        if len(article) <= 0:
            continue
        article = article.strip()
        seg = jieba.cut(article)
        text = " ".join(seg)
        text = "[1;1029;1367262000;0.0,1.0]"+text+"\n"
        texts.append(text)

    article_num = len(texts)
    for line in open(path+'/test'):
        texts.append(line)
    fs = open(path+'/test1.test','w')
    for text in texts:
        fs.writelines(text)
    return article_num

@app.route('/latot_dataset/<file_name>',  methods=['GET'])
def latot_dataset(file_name = None):
    file_name = file_name+'.zip'
    #path = "./SSTM++/lexicon/"+file_name
    abs_path = os.getcwd()+"/LATOT/"+file_name
    # 判断文件是否存在
    if os.path.exists(abs_path):
        response = make_response(send_file(abs_path))
        download_name = "attachment; filename=" + file_name
        response.headers["Content-Disposition"] = download_name
        return response
    else:
        msg = "文件" + file_name + "不存在，请返回"
        return msg




if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=8088)
