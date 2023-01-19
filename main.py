import configparser
import time
import requests
import argparse
import base64
import xlsxwriter

def get_config():
    global your_email
    global your_key
    config = configparser.ConfigParser()
    # 读取配置文件
    config.read('config.ini', encoding="utf-8")
    # 读取section的所有键值，返回结果为列表
    # 每个键值为tuple类型
    for x in config.items("fofa"):
        if "your_key" in x:
            your_key = x[1]
        if "your_email" in x:
            your_email = x[1]


def check_apikey():
    try:
        url = f"https://fofa.info/api/v1/info/my?email={your_email}&key={your_key}"
        data = requests.get(url)
        result = data.json()
        if result['error'] == True:
            print("Account Invalid!")
            return False
        else:
            return True
    except Exception as e:
        print(e)

def query(key):
    qbase64 = str(base64.b64encode(key.encode("utf-8")), "utf-8")
    base_url = f"https://fofa.info/api/v1/search/all?email={your_email}&key={your_key}&qbase64={qbase64}"
    url = f"{base_url}&size=1"
    data = requests.get(url).json()
    if not data['error']:
        if data["size"] > 10000:
            size = 10000
        else:
            size = data["size"]
        fields = "ip,port,protocol,domain,title"
        url = f"{base_url}&size={size}&fields={fields}"
        data = requests.get(url).json()
        write_xml(data["results"])
    else:
        print("查询语法错误")

def write_xml(data):
    x = time.strftime("%Y%m%d%H%M", time.localtime())
    file_name = x+".xlsx"
    workbook = xlsxwriter.Workbook(file_name)
    worksheet = workbook.add_worksheet()
    column  = ['IP', 'Port', 'Protocol', 'Domain', 'Title']
    worksheet.write_row('A1', column)
    line = 2
    for x in data:
        worksheet.write_row('A'+str(line), x)
        line = line+1
    workbook.close()
    print(f'查询结束,结果保存到{file_name}中')



if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-k', '--key', type=str,required=True, help='指定查询参数')
    args = parser.parse_args()
    if args.key:
        get_config()
        if check_apikey():
            print("apikey检测通过")
            query(args.key)

