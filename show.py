import pandas as pd
from pyecharts import options as opts
from pyecharts.charts import Pie, Bar, Timeline

df = pd.read_csv('weather.csv', encoding='gb18030')
# print(df['日期'])

# datetime
df['日期'] = df['日期'].apply(lambda x: pd.to_datetime(x))
# print(df['日期'])

"""
0     2022-01-01
1     2022-01-02
2     2022-01-03
3     2022-01-04
4     2022-01-05
"""

df['month'] = df['日期'].dt.month

# size 计算分组的大小
df_agg = df.groupby(['month', '天气']).size().reset_index()
# print(df_agg)

# 设置列名
df_agg.columns = ['month', 'tianqi', 'count']

# 天气数据组成
(df_agg[df_agg['month'] == 1][['tianqi', 'count']]
 .sort_values(by='count', ascending=False).values.tolist())

# 画图
# 实例化一个时间间隔 1 s
timeline = Timeline()
timeline.add_schema(play_interval=1000)

# 循环遍历
for month in df_agg['month'].unique():
    data = (
        df_agg[df_agg['month']==month][['tianqi','count']]
        .sort_values(by='count', ascending=True)
        .values.tolist()
    )
    # print(data)
    bar = Bar()
    bar.add_xaxis([x[0] for x in data])
    bar.add_yaxis('',[x[1] for x in data])
    # 横着放
    bar.reversal_axis()
    # 计数标签放在图形右边
    bar.set_series_opts(label_opts=opts.LabelOpts(position='right'))
    # 设置图表的名称
    bar.set_global_opts(title_opts=opts.TitleOpts(title='武汉2022年每月的天气变化'))
    # 将设置好的bar对象放置到时间轮播图当中，并且标签选择月份， 格式为数字月
    timeline.add(bar,f'{month}')

# 将生成的图表保存为html文件
timeline.render('weather.html')
