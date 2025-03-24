import dash
from dash import html
import dash_bootstrap_components as dbc
from utils import encode_images


dash.register_page(__name__, path="/home")  # 使用 `dash.pages`


# 获取所有编码后的图片
encoded_logos = encode_images.encode_images_from_assets()


# 主页
layout = html.Div([
    # 引入 Google Fonts
    html.Link(
        href="https://fonts.googleapis.com/css2?family=Poppins:wght@600&family=Roboto:wght@400;700&display=swap",
        rel="stylesheet",
    ),
    dbc.Card(
        [
            dbc.CardImg(
                src=f"data:image/png;base64,{encoded_logos['background.png']}",
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
    dbc.Container(
        children=[
            html.H4(
                "拥有127所双一流高校专利成果数据",
                className="text-center",
                style={
                    "fontFamily": "'Poppins', sans-serif",  # 使用 Poppins 字体
                    "fontSize": "2.5rem",  # 增加字体大小
                    "fontWeight": "600",  # 设置字体粗细
                    "color": "#003366",  # 主标题颜色（深蓝色）
                    "marginBottom": "3rem",  # 增大底部边距以提供更好的间距
                }
            ),  # 标题
            dbc.Row(
                [
                    dbc.Col(html.Img(src=f"data:image/png;base64,{encoded_logos['北京大学-logo-512px.png']}",
                                     height="100px", className="mx-auto d-block"), md=2, style={"padding": "15px"}),
                    # 增加内边距
                    dbc.Col(html.Img(src=f"data:image/png;base64,{encoded_logos['山东大学-logo-512px.png']}",
                                     height="100px", className="mx-auto d-block"), md=2, style={"padding": "15px"}),
                    dbc.Col(html.Img(src=f"data:image/png;base64,{encoded_logos['上海交通大学-logo-512px.png']}",
                                     height="100px", className="mx-auto d-block"), md=2, style={"padding": "15px"}),
                    dbc.Col(html.Img(src=f"data:image/png;base64,{encoded_logos['湖南大学-logo-512px.png']}",
                                     height="100px", className="mx-auto d-block"), md=2, style={"padding": "15px"}),
                    dbc.Col(html.Img(src=f"data:image/png;base64,{encoded_logos['四川大学-logo-512px.png']}",
                                     height="100px", className="mx-auto d-block"), md=2, style={"padding": "15px"}),
                    dbc.Col(html.Img(src=f"data:image/png;base64,{encoded_logos['复旦大学-logo-512px.png']}",
                                     height="100px", className="mx-auto d-block"), md=2, style={"padding": "15px"}),
                ],
                justify="center",  # 居中对齐
                className="mb-4",  # 设置行间距（通过添加底部边距）
                style={"maxWidth": "100%"}  # 确保行不超过容器宽度
            ),
            dbc.Row(
                [
                    dbc.Col(html.Img(src=f"data:image/png;base64,{encoded_logos['清华大学-logo-512px.png']}",
                                     height="100px", className="mx-auto d-block"), md=2, style={"padding": "15px"}),
                    dbc.Col(html.Img(src=f"data:image/png;base64,{encoded_logos['南开大学-logo-512px.png']}",
                                     height="100px", className="mx-auto d-block"), md=2, style={"padding": "15px"}),
                    dbc.Col(html.Img(src=f"data:image/png;base64,{encoded_logos['厦门大学-logo-512px.png']}",
                                     height="100px", className="mx-auto d-block"), md=2, style={"padding": "15px"}),
                    dbc.Col(html.Img(src=f"data:image/png;base64,{encoded_logos['南京大学-logo-512px.png']}",
                                     height="100px", className="mx-auto d-block"), md=2, style={"padding": "15px"}),
                    dbc.Col(html.Img(src=f"data:image/png;base64,{encoded_logos['东南大学-logo-512px.png']}",
                                     height="100px", className="mx-auto d-block"), md=2, style={"padding": "15px"}),
                    dbc.Col(html.Img(src=f"data:image/png;base64,{encoded_logos['武汉大学-logo-512px.png']}",
                                     height="100px", className="mx-auto d-block"), md=2, style={"padding": "15px"}),
                ],
                justify="center",  # 居中对齐
                className="mb-4",  # 设置行间距（通过添加底部边距）
                style={"maxWidth": "100%"}
            ),
            dbc.Row(
                [
                    dbc.Col(html.Img(src=f"data:image/png;base64,{encoded_logos['同济大学-logo-512px.png']}",
                                     height="100px", className="mx-auto d-block"), md=2, style={"padding": "15px"}),
                    dbc.Col(html.Img(src=f"data:image/png;base64,{encoded_logos['北京航空航天大学-logo-512px.png']}",
                                     height="100px", className="mx-auto d-block"), md=2, style={"padding": "15px"}),
                    dbc.Col(html.Img(src=f"data:image/png;base64,{encoded_logos['西北工业大学-logo-512px.png']}",
                                     height="100px", className="mx-auto d-block"), md=2, style={"padding": "15px"}),
                    dbc.Col(html.Img(src=f"data:image/png;base64,{encoded_logos['中国科学技术大学-logo-512px.png']}",
                                     height="100px", className="mx-auto d-block"), md=2, style={"padding": "15px"}),
                    dbc.Col(html.Img(src=f"data:image/png;base64,{encoded_logos['浙江大学-logo-512px.png']}",
                                     height="100px", className="mx-auto d-block"), md=2, style={"padding": "15px"}),
                    dbc.Col(html.Img(src=f"data:image/png;base64,{encoded_logos['哈尔滨工业大学-logo-512px.png']}",
                                     height="100px", className="mx-auto d-block"), md=2, style={"padding": "15px"}),
                ],
                justify="center",  # 居中对齐
                className="mb-4",  # 设置行间距（通过添加底部边距）
                style={"maxWidth": "100%"}
            ),
        ],
        fluid=True,  # 让容器在不同屏幕尺寸下流式布局
        style={"height": "100vh", "display": "flex", "flexDirection": "column", "justifyContent": "center",
               "alignItems": "center"},  # 页面居中显示
    ),
])
