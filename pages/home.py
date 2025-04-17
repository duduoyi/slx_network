import dash
from dash import html
import dash_bootstrap_components as dbc
import logging


logger = logging.getLogger(__name__)


dash.register_page(__name__, path='/')


# 主页
logger.info("加载主页布局")
layout = html.Div([
    dbc.Card(
        [
            dbc.CardImg(
                src=dash.get_asset_url('images/background.png'),
                top=True,
                style={
                    "opacity": 0.3,  # 调整背景图片透明度
                    "height": "100vh",  # 背景图片高度为视口高度
                    "objectFit": "cover",  # 图片填充整个区域
                    "position": "absolute",  # 绝对定位
                    "top": 0,
                    "left": 0,
                    "width": "100%",  # 宽度为100%
                },
            ),
            dbc.CardImgOverlay(
                dbc.CardBody(
                    [
                        html.H4(
                            "三螺旋 小世界",
                            className="card-title",
                            style={
                                "fontSize": "3.5rem",  # 主标题字体大小
                                "fontFamily": "'Poppins', sans-serif",  # 使用 Poppins 字体
                                "fontWeight": "600",  # 字体粗细
                                "color": "#003366",  # 主标题颜色（深蓝色）
                                "textAlign": "center",  # 文字居中
                                "marginBottom": "1rem",  # 主标题与副标题的间距
                            },
                        ),
                        html.P(
                            "Triple helix model of innovation",
                            className="card-text",
                            style={
                                "fontSize": "1.8rem",  # 副标题字体大小
                                "fontFamily": "'Roboto', sans-serif",  # 使用 Roboto 字体
                                "fontWeight": "400",  # 字体粗细
                                "color": "#003366",  # 副标题颜色（深蓝色）
                                "textAlign": "center",  # 文字居中
                                "marginBottom": "0",  # 去除默认的段落底部间距
                            },
                        ),
                    ],
                    style={
                        "display": "flex",  # 使用 Flexbox 布局
                        "flexDirection": "column",  # 垂直排列
                        "justifyContent": "center",  # 垂直居中
                        "alignItems": "center",  # 水平居中
                        "height": "calc(100vh - 60px)",  # 减去导航栏的高度
                        "paddingTop": "60px",  # 添加顶部内边距以避免内容被导航栏遮挡
                    },
                ),
            ),
        ],
        style={
            "width": "100%",  # 卡片宽度
            "height": "100vh",  # 卡片高度为视口高度
            "position": "relative",  # 相对定位
            "overflow": "hidden",  # 隐藏溢出内容
            "border": "none",  # 去掉黑色细边框
        },
    ),
])
