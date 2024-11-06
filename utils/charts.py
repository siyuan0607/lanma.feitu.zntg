import pandas as pd
import mplfinance as mpf
import matplotlib.pyplot as plt
from io import BytesIO
from mplfonts.bin.cli import init as font_inti

font_inti()
from mplfonts import use_font

use_font("Songti SC")

CONTENT_TYPE = "image/png"


def draw_kline_chart(df: pd.DataFrame, date='Date', open='Open', high='High', low='Low', close='Close',
                     volume='Volume'):
    """
    生成k线图
    :return image_bytes, image_type
    """
    # 改写column，准备绘图
    df['Date'] = df[date]
    df['Open'] = df[open]
    df['High'] = df[high]
    df['Low'] = df[low]
    df['Close'] = df[close]
    df['Volume'] = df[volume]

    # 调整绘制图片
    df['Date'] = pd.to_datetime(df['Date'])
    df.set_index('Date', inplace=True)
    # 设置绘图样式
    mpf_style = mpf.make_mpf_style(base_mpf_style='charles', rc={'font.size': 14, 'font.family': 'Songti SC'})

    # 创建一个BytesIO对象来存储图像
    image_buffer = BytesIO()

    # 保存图片
    mpf.plot(df, type='candle', style=mpf_style, title='K线图示例', ylabel='价格', ylabel_lower='成交量',
             savefig=image_buffer)
    image_bytes = image_buffer.getvalue()
    image_buffer.close()
    return image_bytes, CONTENT_TYPE


def draw_bar_chart(df: pd.DataFrame, y_label: str, x_label: str, ys: dict, title: str):
    """
    绘制柱状图
    """
    # 创建一个BytesIO对象来存储图像
    image_buffer = BytesIO()

    # 绘制柱状图
    plt.figure(figsize=(8, 6))
    i = 0
    for key, value in ys.items():
        plt.bar(df[x_label], df[value], label=key, color=plt.cm.tab20(i))
        i += 1
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.title(title)

    # 保存图像到BytesIO对象
    plt.savefig(image_buffer, format='png')

    # 将BytesIO对象转换为字节数组
    image_bytes = image_buffer.getvalue()

    # 清理资源
    plt.close()
    image_buffer.close()

    # 返回字节数组
    return image_bytes, CONTENT_TYPE


def draw_line_chart(df: pd.DataFrame, x: str, ys: dict, x_label='', title: str = ""):
    """
    绘制折线图
    """
    # 创建一个BytesIO对象来存储图像
    image_buffer = BytesIO()

    plt.figure(figsize=(10, 5))  # 可以指定图像大小
    for y_label, y_value in ys.items():
        plt.plot(df[x], df[y_value], marker='o', label=y_label)

    # 添加标题和标签
    plt.title(title)
    plt.xlabel(x_label)

    # 显示网格
    plt.grid(True)

    # 显示图例
    plt.legend()
    plt.savefig(image_buffer, format='png')

    image_bytes = image_buffer.getvalue()
    image_buffer.close()
    return image_bytes, CONTENT_TYPE
