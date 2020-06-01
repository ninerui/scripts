# 导入所需包
import requests
import json
import pandas as pd
import time


def get_bili_comment_one(url):
	"""
	功能：获取一页的信息
	"""
	# 添加headers
	headers = {
		'Host': 'api.bilibili.com',
		'Referer': 'https://www.bilibili.com/video/BV1YZ4y1j7s5',
		'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36'
	}

	# 添加cookies
	cookies = {
		"cookie": "你的浏览器cookie信息"
	}

	# 发起请求
	try:
		r = requests.get(url, headers=headers, cookies=cookies, timeout=3)
	except Exception as e:
		print(e)
		r = requests.get(url, headers=headers, cookies=cookies, timeout=3)

	# 解析为字典
	r_json = json.loads(r.text)

	# 提取信息
	replies_data = r_json['data']['replies']

	# 用户名
	user_name = [i['member'].get('uname') for i in replies_data]
	# 性别
	sex = [i['member'].get('sex') for i in replies_data]
	# 签名
	sign = [i['member'].get('sign') for i in replies_data]
	# 用户等级
	current_level = [i['member']['level_info'].get('current_level') for i in replies_data]
	# 评论内容
	content = [i['content'].get('message') for i in replies_data]
	# 用户设备
	device = [i['content'].get('device') for i in replies_data]
	# 评论时间
	content_time = [i.get('ctime') for i in replies_data]
	# 回复数
	reply_count = [i['rcount'] for i in replies_data]

	# 存储数据
	df = pd.DataFrame({
		'user_name': user_name,
		'sex': sex,
		'sign': sign,
		'current_level': current_level,
		'content': content,
		'device': device,
		'content_time': content_time,
		'reply_count': reply_count
	})

	return df


def get_bili_comment_all(oid, num):
	"""
	获取B站视频指定页评论信息
	"""
	# 循环构建URL
	df_all = pd.DataFrame()

	for page_num in range(1, num):
		try:
			# 构建URL
			url = 'https://api.bilibili.com/x/v2/reply?&pn={}&type=1&oid={}&sort=2'.format(page_num, oid)
			# 调用函数
			df = get_bili_comment_one(url)
			# 判断
			if df.shape[0] == 0:
				break
			else:
				# 循环追加
				df_all = df_all.append(df, ignore_index=True)
				# 打印进度
				print('我正在获取第{}页的信息'.format(page_num))
		except:
			break

	# 休眠一秒
	time.sleep(0.5)

	return df_all


# 《入海》bilibili X 毛不易 | 跃入人海，各有风雨灿烂
df = get_bili_comment_all(oid='795637027', num=973)

# 读出数据
# df.to_excel('B站评论数据-入海5.23.xlsx', index=False)
