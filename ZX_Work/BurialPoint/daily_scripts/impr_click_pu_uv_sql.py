page_template_map = [
    {'2024':
         {'20427': '导航栏',
          '26428': '首页头部背景图',
          '26429': '大金刚',
          '26431': '战略位',
          '26478': '小金刚',
          '26656': '待办事项',
          '20657': '轮播banner（中部）',
          '27409': '新客专享',
          '27410': '权益活动',
          '27411': '有温度的资产负债表',
          '27413': '发薪专享',
          '27414': '借钱专区',
          '27415': '幸福+养老账本',
          '27416': '“双卡人”专属',
          '27417': '资讯',
          '27418': '财富专享',
          '27419': '私行尊享',
          '27420': '城市服务',
          '27422': '出国金融',
          }},
    {'2220':
         {'28074': '导航栏',
          '28075': '首页头部背景图',
          '28076': '大金刚',
          '28077': '小金刚',
          '28078': '战略位',
          '28079': '待办事项',
          '28080': '轮播banner（中部）',
          '28082': '财富专享',
          '28083': '发薪专享',
          '28084': '借钱专区',
          '28085': '杈益活动',
          '28086': '资讯',
          }}]

for page_template_info in page_template_map:
    for page_id, template_info in page_template_info.items():
        for template_id, template_name in template_info.items():
            if page_id == '2024':
                fac_page_type = "'dynamic'"
                template_name = "# 以下SQL为" + "算法的" + template_name + "查询脚本"
            else:
                fac_page_type = "'static'"
                template_name = "# 以下SQL为" + "静态的" + template_name + "查询脚本"

            sql_str = """
            {template_name}
            with template_element_map as
                     (select *
                      from (values ('{dynamic_page_id}', '{dynamic_template_id}', {page_type}),
                                   ('', '', '')) as temp(
                                                         map_cube_page_id,
                                                         map_template_id,
                                                         map_page_name
                          )),
                 click_tab as
                     (SELECT cstno,
                             SPLIT(page_name, '_')[3]  as page_id,
                             SPLIT(event_id, '\\|')[1] as template_instance_id,
                             SPLIT(event_id, '\\|')[2] as template_type,
                             SPLIT(event_id, '\\|')[3] as element_instance_id,
                             event_dt,
                             'click'                   as type
                      from SDMS_DW.D_CBAS_001_M_SDK_CUSTOM_EVENT_I event_tab
                               inner join template_element_map tem on 1 = 1
                          and SPLIT(event_tab.event_id, '\\|')[1] = tem.map_template_id
                          and SPLIT(event_tab.page_name, '_')[3] = tem.map_cube_page_id
                      where event_tab.dt between date_format(date_add(CURRENT_DATE, -15), 'YYYYMMdd')
                          and date_format(date_add(CURRENT_DATE, 1), 'YYYYMMdd')
                        and event_dt between date_format(date_add(CURRENT_DATE, -14), 'YYYY-MM-dd')
                          anD date_format(date_add(CURRENT_DATE, -1), 'YYYY-MM-dd')
                        and page_name like 'cube_page_id_%'
                        and SPLIT(event_id, '\\|')[0] like 'cube_page_id_%'),
                 show_tab as
                     (SELECT cstno,
                             CBAS_CUBE_PAGE_ID,
                             CBAS_TEMPLATE_INSTANCE_ID,
                             CBAS_TEMPLATE_TYPE,
                             CBAS_ELEMENT_INSTANCE_ID,
                             event_dt,
                             'impression' as type
                      FROM SDMS_DW.D_CBAS_001_M_SDK_EVENT_SHOW_I as show_tab
                               inner Join template_element_map tem
                                          on 1 = 1
                                              and show_tab.CBAS_TEMPLATE_INSTANCE_ID = tem.map_template_id
                                              and show_tab.CBAS_CUBE_PAGE_ID = tem.map_cube_page_id
                      WHERE show_tab.dt between date_format(date_add(CURRENT_DATE, -15), 'yyyyMMdd')
                          and date_format(date_add(CURRENT_DATE, -1), 'yyyyMMdd')
                        and event_dt between date_format(date_add(CURRENT_DATE, -14), 'yyyy-MM-dd')
                          and date_format(date_add(CURRENT_DATE, -1), 'yyyy-MM-dd')
                        and event_id = 'cube_element_show_event_cbas'),
                 click_show_union_tab as
                     (select cstno,
                             page_id,
                             template_instance_id,
                             template_type,
                             element_instance_id,
                             event_dt,
                             type
                      from click_tab
                      union all
                      select cstno,
                             CBAS_CUBE_PAGE_ID         as page_id,
                             CBAS_TEMPLATE_INSTANCE_ID as template_instance_id,
                             CBAS_TEMPLATE_TYPE        as template_type,
                             CBAS_ELEMENT_INSTANCE_ID  as element_instance_id,
                             event_dt,
                             type
                      from show_tab),
                 click_show_aggr_tab as
                     (select event_dt,
                             page_id,
                             template_instance_id,
                             template_type,
                             element_instance_id,
                             count(
                                     if(type = 'impression', cstno, null)
                             ) as show_pv,
                             count(
                                     distinct if(type = 'impression', cstno, null)
                             ) as show_uv,
                             count(
                                     if(type = 'click', cstno, null)
                             ) as click_pv,
                             count(
                                     distinct if(type = 'click', cstno, null)
                             ) as click_uv
                      from click_show_union_tab
                      group by event_dt,
                               page_id,
                               template_instance_id,
                               template_type,
                               element_instance_id),
                 template_tab as
                     (SELECT distinct id,
                                      template_instance_name
                      FROM SDMS_DW.d_imcs_00l_mkt_template_instance_a
                      where dt between date_format(date_add(CURRENT_DATE, -90), 'yyyyMMdd')
                                and date_format(date_add(CURRENT_DATE, -1), 'yyyyMMdd')),
                 element_tab as
                     (select distinct TEMPLATE_INSTANCE_ID,
                                      id as element_id,
                                      ELEMENT_INSTANCE_NAME
                      from sdms_dw.d_imcs_001_mkt_element_instance_a
                      where dt between date_format(date_add(CURRENT_DATE, -90), 'yyyyMMdd') and date_format(date_add(CURRENT_DATE, -1), 'yyyyMMdd'))
            SELECT csat.event_dt,
                   csat.page_id,
                   csat.template_instance_id,
                   tt.template_instance_name,
                   csat.template_type,
                   csat.element_instance_id,
                   csat.ELEMENT_INSTANCE_NAME,
                   csat.show_pv,
                   csat.show_uv,
                   csat.click_pv,
                   csat.click_uv
            from click_show_aggr_tab csat
                     left join template_tab tt on csat.template_instance_id = tt.id
                     Left join element_tab et on et.element_id = csat.element_instance_id
            ORDER BY csat.event_dt, csat.page_id,
                     csat.template_instance_id,
                     tt.template_instance_name,
                     csat.template_type,
                     csat.element_instance_id,
                     csat.ELEMENT_INSTANCE_NAME
            limit 30000;
            
            ------------------------------------------------------------------------------------------------------------------------------------------------
            
            """.format(
                dynamic_page_id=page_id,
                dynamic_template_id=template_id,
                page_type=fac_page_type,
                template_name=template_name,
            )

            print(sql_str)
