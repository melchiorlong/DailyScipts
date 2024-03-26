template_id_instance_name_dict = {
    26427: ["导航栏", "cb-cube-header-new"],
    26428: ["首页头部背景图", "cb-cube-v10-home-banner"],
    26429: ["大金刚", "cb-cube-v10-home-banner-menu"],
    26431: ["战略位", "cb-cube-v10-home-submenu"],
    26478: ["小金刚.", "cb-cube-v10-home-smart-menu"],
    26656: ["待办事项", "cb-cube-standard-home-todo-reminder"],
    26657: ["轮播banner（中部）", "cb-cube-banner1-new"],
    27409: ["新客专享", "cb-cube-v10-home-feature-business"],
    27410: ["权益活动", "cb-cube-v10-home-feature-business3"],
    27411: ["有温度的资产负债表", "cb-cube-v10-home-feature-business"],
    27413: ["发薪专享", "cb-cube-v10-home-salary-card"],
    27414: ["借钱专区", "cb-cube-v10-home-feature-business3"],
    27415: ["幸福+养老账本", "cb-cube-v10-home-smart-annuity"],
    27416: ["“双卡人”专属", "cb-cube-v10-home-feature-business2"],
    27417: ["资讯", "cb-cube-news-hot"],
    27418: ["财富专享", "cb-cube-v10-home-wealth-exclusive"],
    27419: ["私行尊享", "cb-cube-v10-private-privilege"],
    27420: ["城市服务", "cb-cube-v10-home-feature-business"],
    27422: ["出国金融", "cb-cube-v10-home-fea"],
}

for page_id, page_info in template_id_instance_name_dict.items():
    # print('页面名称是: ' + page_info[0])
    # print('模板类型是: ' + page_info[1])
    # print("select * from show where page_id = " + str(page_id) + ';')
    # print()
    if 'feature-business' in page_info[1]:
        print(page_info[0])
