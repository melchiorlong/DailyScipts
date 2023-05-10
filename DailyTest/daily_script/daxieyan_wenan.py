names = [
	'刀哥',
	'sk',
	'飞哥',
	'炸炸',
	'大哥',
	'甘甘',
	# '程哥',
]

template = 'xxx 哈喽啊，我跟静怡4.22不是婚礼来着嘛，因为家里父母工作的原因就没有叫朋友们参加，5.21中午我们准备整个答谢宴，邀请下咱们大学同学～大家正好一起聚聚，吃个饭～你看看时间ok不～'
template_back = '哈哈哈哈 谢谢xxx～～～等你来哦～带媳妇一起不 我提前订位置～'


final_str_list = []
for name in names:
	sentence = template_back.replace('xxx', name)
	final_str_list.append(sentence)

for final_str in final_str_list:
	print(final_str)



