import time
import requests
from urllib.parse import urlparse, parse_qs

def extract_params_from_url(url: str) -> dict:
    """从答题链接中提取参数"""
    parsed_url = urlparse(url)
    query_scheme = parsed_url.scheme,
    query_netloc = parsed_url.netloc,
    query_path = parsed_url.path,
    print(f"我是parsed_url为:{parsed_url.scheme}, {parsed_url.netloc}, {parsed_url.path}")
    query_params = parse_qs(parsed_url.query)

    # 提取需要的参数
    params = {
        "scheme": query_scheme,
        "netloc": query_netloc,
        "path": query_path,
        "rx_token": query_params.get("rx_token", [""])[0],  # 取第一个 rx_token
        "operationType": query_params.get("operationType", [""])[0],
        "activeTitle": query_params.get("activeTitle", [""])[0],
        "activeId": query_params.get("activeId", [""])[0],
        "schedule": query_params.get("schedule", [""])[0],
        "id": query_params.get("id", [""])[0],
        "bizType": query_params.get("bizType", [""])[0],
        "testNum": query_params.get("testNum", [""])[0],
        "examType": query_params.get("examType", [""])[0],
        "activeYear": query_params.get("activeYear", [""])[0],
        "activeMonths": query_params.get("activeMonths", [""])[0],
        "flag": query_params.get("flag", [""])[0],
    }

    return params


def submit_score(url: str):
    """根据用户提供的链接动态构造请求并提交答题成绩"""
    # 提取URL中的参数
    params = extract_params_from_url(url)

    # # 使用传入的URL解析出基础URL（协议+域名）
    # parsed_url = urlparse(url)
    # print(f"我是parsed_url为:{params["scheme"]}, {params["netloc"]}")
    # base_url = f"{params["scheme"][0]}://{params["netloc"][0]}{params["path"][0]}"
    # print(f"我是基础URL为:{base_url}")

    # # 基础URL（去掉查询部分）
    if params["netloc"][0] == "mobilenew.xianfengdangjian.com.cn":
        base_url = "https://mobilenew.xianfengdangjian.com.cn/party/activityExam/onlineExam/submitTestMobile"
    elif params["netloc"][0] == "m.dj.cnpc.com.cn":
        base_url = "https://m.dj.cnpc.com.cn/party/onlineExam/onlineExam/submitTestMobile"

    headers = {
        "Accept": "application/json",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Connection": "keep-alive",
        "Content-Type": "application/json;charset=UTF-8",
        "Host": params["netloc"][0],  # 从URL中提取的Host
        "Origin": f"{params['scheme'][0]}://{params['netloc'][0]}",  # 从URL中提取的Origin
        "Referer": url,  # 使用传入的完整URL作为 Referer
        "rxToken": params["rx_token"],  # 从URL中提取的rx_token
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "source": "2",
        "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.6261.95 Mobile Safari/537.36",
        "X-Requested-With": "XMLHttpRequest"
    }
    print(headers)
    # 获取当前时间戳（毫秒）
    current_time = int(time.time() * 1000)

    # 构造payload
    payload = {
        "testId": params["id"],
        "bizType": params["bizType"],
        "flag": params["flag"],
        "examType": params["examType"],
        "startTime": current_time - 62320,  # 开始时间（当前时间减去答题耗时）
        "endTime": current_time,  # 结束时间
        "resDuration": 62320,  # 答题耗时（毫秒）
        "resScore": 100,  # 得分
        "isExercise": 0,  # 是否练习（0为正式考试）
        "listExam": [],  # 考试列表（空）

        "questionIdList": [
            "1127973733163751361",
            "1127973733176334272",
            "1127973733209888712",
            "1127973733222471616",
            "1127973733239248832"
        ],
        "rightIdList": [
            "1127973733163751360",
            "1127973733176334272",
            "1127973733209888712",
            "1127973733222471616",
            "1127973733239248832"
        ],

    }

    try:
        response = requests.post(base_url, headers=headers, json=payload, verify=False)
        print(f"状态码: {response.status_code}")
        # print("响应内容:")
        # print(response.json())
        return response
    except Exception as e:
        print(f"请求失败: {str(e)}")
        return {str(e)}


def get_user_info(url: str):
    """获取用户信息"""
    # 提取URL中的参数
    params = extract_params_from_url(url)


    if params["netloc"][0] == "mobilenew.xianfengdangjian.com.cn":
        base_url = "https://mobilenew.xianfengdangjian.com.cn/party/activityExam/onlineExam/submitTestMobile"
    elif params["netloc"][0] == "m.dj.cnpc.com.cn":
        base_url = "https://m.dj.cnpc.com.cn/party/onlineExam/onlineExam/checkTestNum"


    headers = {
        "Accept": "application/json",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Connection": "keep-alive",
        "Content-Type": "application/json;charset=UTF-8",
        "Host": params["netloc"][0],  # 从URL中提取的Host
        "Origin": f"{params['scheme'][0]}://{params['netloc'][0]}",  # 从URL中提取的Origin
        "Referer": url,  # 使用传入的完整URL作为 Referer
        "rxToken": params["rx_token"],  # 从URL中提取的rx_token
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "source": "2",
        "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.6261.95 Mobile Safari/537.36",
        "X-Requested-With": "XMLHttpRequest"
    }

    # 获取当前时间戳（毫秒）
    current_time = int(time.time() * 1000)

    # 构造payload
    payload = {
        "id": params["id"],
        "testNum": params["testNum"],
        "bizType": params["bizType"],
    }

    try:
        response = requests.post(base_url, headers=headers, json=payload, verify=False)
        print(f"状态码: {response.status_code}")
        # print("响应内容:")
        # print(response.json())
        return response
    except Exception as e:
        print(f"请求失败: {str(e)}")
        return {str(e)}



def get_testname(url: str):
    """获取用户信息"""
    # 提取URL中的参数
    params = extract_params_from_url(url)


    if params["netloc"][0] == "mobilenew.xianfengdangjian.com.cn":
        base_url = "https://mobilenew.xianfengdangjian.com.cn/party/activityExam/onlineExam/submitTestMobile"
    elif params["netloc"][0] == "m.dj.cnpc.com.cn":
        base_url = "https://m.dj.cnpc.com.cn/party/onlineExam/onlineExam/joinTest"



    headers = {
        "Accept": "application/json",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Connection": "keep-alive",
        "Content-Type": "application/json;charset=UTF-8",
        "Host": params["netloc"][0],  # 从URL中提取的Host
        "Origin": f"{params["scheme"][0]}://{params["netloc"][0]}",  # 从URL中提取的Origin
        "Referer": url,  # 使用传入的完整URL作为 Referer
        "rxToken": params["rx_token"],  # 从URL中提取的rx_token
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "source": "2",
        "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.6261.95 Mobile Safari/537.36",
        "X-Requested-With": "XMLHttpRequest"
    }

    # 获取当前时间戳（毫秒）
    current_time = int(time.time() * 1000)

    # 构造payload
    payload = {
        "id": params["id"],
        "examType": params["examType"],
        "bizType": params["bizType"],
    }

    try:
        response = requests.post(base_url, headers=headers, json=payload, verify=False)
        print(f"状态码: {response.status_code}")
        # print("响应内容:")
        # print(response.json())
        return response
    except Exception as e:
        print(f"请求失败: {str(e)}")
        return {str(e)}