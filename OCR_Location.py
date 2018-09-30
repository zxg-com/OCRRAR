from aip import AipOcr
import OCR_Global as gl

# 新建一个AipOcr对象
client = AipOcr(**{
    'appId': '11840928',
    'apiKey': 'ur3lXiWX2kFYrvXamEpA3zXP',
    'secretKey': 'wnNomip2sTIFlpjcphGaegQ6bP82fnVy'
})

# 读取图片
def get_file_content(file_path):
    with open(file_path, 'rb') as fp:
        return fp.read()

# 识别图片里的文字
def img_to_str(image_path):
    image = get_file_content(image_path)
    options = {}
    options["language_type"] = "CHN_ENG"
    options["detect_direction"] = "true"
    options["detect_language"] = "true"
    options["probability"] = "true"
    # 调用通用文字识别, 图片参数为本地图片
    gl.gAllResult = client.general(image,options) #通用文字识别（含位置信息版）
    # result = client.accurate(image,options) #通用文字识别（含位置高精度版）

def get_all_str():
    # 结果拼接返回
    count = 0
    strResult =""
    if 'words_result' in gl.gAllResult:
        for w in gl.gAllResult['words_result']:
            if strResult == "":
                strResult = w['words']
            else:
                strResult = strResult + '\n' + w['words']
            count = count + 1
    strResult = strResult + '\n' + "总计：" + str(count)
    return strResult
    # if 'words_result' in gl.gAllResult:
    #     return '\n'.join([w['words'] for w in gl.gAllResult['words_result']])

def get_one_str(containsStr):
    key=[]
    gl.gOneResult = []
    count = 0
    strResult =""
    if 'words_result' in gl.gAllResult:
        for w in gl.gAllResult['words_result']:
            if containsStr in w['words']:
                key.append(w['words'])
                gl.gOneResult.append(w['location'])
                count = count + 1
    for i in range(0,len(key)):
        if strResult == "":
            strResult = key[i]
        else:
            strResult = strResult + '\n' +key[i]
    return strResult + '\n' + "总计：" + str(count)

if __name__ == '__main__':
    print(get_one_str('1.png',"认证"))
