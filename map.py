#!/usr/bin/python
# -*- coding: UTF-8 -*-


from pyecharts.echarts import Geo,Map


from pyecharts import Bar, Pie, Grid


def main():
  print("HELLO")
  # 省和直辖市
  province_distribution = {'河南': 45.23, '北京': 37.56, '河北': 21, '辽宁': 12, '江西': 6, '上海': 20, '安徽': 10, '江苏': 16, '湖南': 9,
                           '浙江': 13, '海南': 2, '广东': 22, '湖北': 8, '黑龙江': 11, '澳门': 1, '陕西': 11, '四川': 7, '内蒙古': 3,
                           '重庆': 3, '云南': 6, '贵州': 2, '吉林': 3, '山西': 12, '山东': 11, '福建': 4, '青海': 1, '舵主科技，质量保证': 1,
                           '天津': 1, '其他': 1}
  provice = list(province_distribution.keys())
  values = list(province_distribution.values())
  # maptype='china' 只显示全国直辖市和省级
  # 数据只能是省名和直辖市的名称
  map = Map("华东营销中心", '中国地图', width=1200, height=600)
  map.add("", provice, values, visual_range=[0, 50], maptype='china', is_visualmap=True,
          visual_text_color='#000')
  #map.show_config()
  #map.render(path="D:/04-01中国地图.html")

  data = [
      ("海门", 9), ("鄂尔多斯", 12), ("招远", 12), ("舟山", 12), ("齐齐哈尔", 14), ("盐城", 15),
      ("赤峰", 16), ("青岛", 18), ("乳山", 18), ("金昌", 19), ("泉州", 21), ("莱西", 21),
      ("日照", 21), ("胶南", 22), ("南通", 23), ("拉萨", 24), ("云浮", 24), ("梅州", 25)]

  attr, value = Geo.cast(data)

  geo = Geo("全国主要城市空气质量热力图", "data from pm2.5", title_color="#fff", title_pos="center", width=1200, height=600,
            background_color='#404a59')

  geo.add("空气质量热力图", attr, value, visual_range=[0, 25], type='heatmap', visual_text_color="#fff", symbol_size=15,
          is_visualmap=True, is_roam=False)
  #geo.show_config()
  #geo.render(path="./data/04-04空气质量热力图.html")

  grid = Grid(height=720, width=1200)  # 初始化，参数可传page_title,width,height
  grid.add(map, grid_bottom="60%", grid_left="60%")  # 添加要展示的图表，并设置显示位置
  grid.add(geo, grid_bottom="60%", grid_right="60%")  # 添加要展示的图表，并设置显示位置

  grid.render('D:/中国地图.html')

if __name__ == '__main__':
      main()