import numpy as np
import pandas as pd
import dash_bootstrap_components as dbc
import plotly_express as px
from plotly.subplots import make_subplots
from dash import html
import plotly.graph_objects as go
from plotly.colors import n_colors
from dash import dash_table

# Colors (gradient generated between FCD "blue" #39499B and "orange" #F47B29)
# color_gradients = ["#39499b", "#57489d", "#70469d", "#86449c", "#9b4197", "#ae3e92", "#bf3b8a", "#ce3b81",
# "#db3d76", "#e5426b", "#ed4a5f", "#f35453", "#f66046", "#f66d38", "#f47b29"]

color_gradients = ["rgb(57, 73, 155)", "rgb(87, 72, 157)", "rgb(112, 70, 157)", "rgb(134, 68, 156)",
                   "rgb(155, 65, 151)", "rgb(174, 62, 146)", "rgb(191, 59, 138)", "rgb(206, 59, 129)",
                   "rgb(219, 61, 118)", "rgb(229, 66, 107)", "rgb(237, 74, 95)", "rgb(243, 84, 83)", "rgb(246, 96, 70)",
                   "rgb(246, 109, 56)", "rgb(244, 123, 41)"]

# Texts

methods_text_1 = "¿De dónde provienen estos datos?"
methods_text_2 = "Los datos de esta sección provienen censos visuales de peces y macroinvertebrados marinos. La " \
                 "metodología usada que se encuentra ampliada en el Manual de Monitoreo Submareal Ecológico para la " \
                 "Reserva Marina de Galápagos (Banks et al. 2016). De manera general el monitoreo de peces y " \
                 "vertebrados marinos se realiza al identificar especies, estimar abundancia relativa y tallas, " \
                 "información con la que luego se genera la estimación de biomasa. Estas identificaciones se realizan " \
                 "en un transecto de 50 m como unidad mínima de muestreo. En algunos estudios los transectos se " \
                 "extienden a 100 m de largo para mejorar la detección de ciertas especies de interés comercial pero " \
                 "de baja abundancia como Mycteroperca olfax (bacalao)."
methods_text_3 = "El área de monitoreo se establece al formar un túnel imaginario de 5 m a cada lado de la cinta " \
                 "fijada longitudinalmente y 5 m por encima del fondo marino, donde se registran y cuentan las " \
                 "especies de peces presentes. A partir de la información de número de individuos se realiza la " \
                 "estimación de abundancia y a partir de sus tallas se estima la biomasa. Estos muestreos se han " \
                 "realizado en más de 100 sitios alrededor del archipiélago, en varias fechas en el año y desde 2004 " \
                 "hasta 2020. Es importante notar que existe una diferencia en la cobertura, en número de registros y " \
                 "sitios parte del monitoreo entre diferentes años."

footer_grant_text = html.P(
    "Los datos para este visualizador han sido desarrollados gracias a la Fundación Gordon y Betty Moore a través del proyecto Saber más, gobernar mejor: Dinámica de los sistemas marinos y terrestres hacia la sostenibilidad de Galápagos en colaboración con Conservación Internacional, Ministerio de Agricultura y la Agencia de Regulación y Control de la Bioseguridad y Cuarentena para Galápagos",
    className="footer-grant")

# Header, Methods and Footer

header = html.Div(
    [
        html.Img(src=r"./assets/de_logo.png",
                 width="130px",
                 style={'display': 'inline-block', "padding": "10px"}),
        html.H4("Data explorer: Biomasa en peces",
                style={'display': 'inline-block', "color": "white", 'marginLeft': 30, "bottom": 0})
    ], style={"background": "#333f54", 'display': 'inline-block', "width": "100%"}
)

## Labels and vues for methods section:


footer = html.Div(
    [
        html.Div(
            [
                html.Img(src="https://poliswaterproject.org/files/2017/06/moore-logo-color-transparent.png",
                         height="60px",
                         style={"padding": "10px 15px", "display": "inline-block"}),
                footer_grant_text
            ]
        ),
        html.P("©Fundación Charles Darwin", className="footer-fcd")
    ], style={"display": "flex", "justify-content": "space-between"}
)


# Helper functions

def tab_creator(label_name, content):
    tab = dbc.Tab(content, label=label_name,
                  tab_style={'backgroundColor': '#e9ebef'},
                  active_label_style={'color': '#333f54', 'fontWeight': 'bold'},
                  label_style={'color': 'gray'})
    return tab


def checklist_creator(df, column, _id):
    unique_values = sorted(df[column].dropna().unique())
    checklist = dbc.Checklist(id=_id,
                              options=[{"label": i, 'value': i} for i in unique_values],
                              value=[],
                              switch=True)
    return checklist


def check_all_creator(_id):
    check_all = dbc.Checkbox(id=_id,
                             label="Seleccionar todo",
                             value=["Seleccionar todo"])
    return check_all


# Deprecated add logo function as logo is not rendering right in responsive scenarios
# def add_logo_to_charts(fig):
#     image_path = r"./assets/fcd_logo.png"
#     fig = fig.add_layout_image(
#         dict(
#             source=image_path,
#             xref="paper", yref="paper",
#             x=1, y=1,
#             sizex=0.2, sizey=0.2,
#             xanchor="right", yanchor="bottom"
#         )
#     )
#
#     return fig


def bar_chart_creator(df, names):
    header = "<b>Biomasa por " + names.lower() + "</b><br>"
    description = "<i>Total de biomasa estimada por 250 metros cuadrados</i>"
    fig = px.bar(df, x="Biomass.250m2", y=names, color="Biomass.250m2")
    fig.update_layout(title=(header + description),
                      title_font_family="Roboto",
                      title_font_color="#333f54")
    return fig


def bivariate_bar_chart_creator(df, names_x, names_y):
    header = "<b>Biomasa por " + names_x.lower() + " y por " + names_y.lower() + "</b><br>"
    description = "<i>Total de biomasa estimada por 250 metros cuadrados</i>"
    fig = px.bar(df, x=names_x, y=df.columns[1:],
                 color_discrete_sequence=color_gradients,
                 labels={"value": "Biomasa por 250 m2",
                         "variable": names_y})
    fig.update_layout(title=(header + description),
                      title_font_family="Roboto",
                      title_font_color="#333f54")
    return fig


# Maybe reactivate this chart if only 2 categorical values are mapped for chart
# def donut_creator(df, names, values):
#     fig = px.pie(data_frame=df,
#                  names=names,
#                  values=values,
#                  hole=0.5,
#                  color_discrete_sequence=px.colors.sequential.Agsunset)
#     # print(px.colors.sequential.Agsunset)
#     fig.update_layout(legend=dict(
#         orientation="h",
#         yanchor="bottom",
#         xanchor="center",
#         x=0.5
#     ))
#     return fig


def value_cards(label, values):
    card = html.Div(
        [
            html.Div(label, className="value-cards-label"),
            html.Div(len(values), className="value-cards-value")
        ], className="value-cards"
    )
    return card


def two_axis_line_chart(df, x_column, y1_value_to_count, y2_value_to_count, x_name, y1_name, y2_name):
    x = df[x_column].unique()
    y1 = df.groupby([x_column])[y1_value_to_count].count()
    y2 = df.groupby([x_column])[y2_value_to_count].nunique()

    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(
        go.Scatter(x=x, y=y1, name=y1_name, line=dict(color="#333f54"), line_shape="spline"),
        secondary_y=False
    )

    fig.add_trace(
        go.Scatter(x=x, y=y2, name=y2_name, line=dict(color="orange"), line_shape="spline"),
        secondary_y=True,
    )

    # Set x-axis title
    fig.update_xaxes(title_text=x_name)

    # Set y-axes titles
    fig.update_yaxes(title_text=y1_name, secondary_y=False)
    fig.update_yaxes(title_text=y2_name, secondary_y=True)

    fig.update_layout(title="<b>Esfuerzos de monitoreo por año</b><br>Número de registros y sitios monitoreados",
                      title_font_family="Roboto",
                      title_font_color="#333f54",
                      plot_bgcolor="#ffffff",
                      width=500)

    return fig


def simple_map(df, lat, long, dimension, value_to_count):
    df = pd.DataFrame(df.groupby([dimension, lat, long])[value_to_count].count())
    df.reset_index(col_level=0, inplace=True)
    df.rename(columns={'id': 'Registros'}, inplace=True)

    fig = px.scatter_mapbox(df, lat=lat, lon=long, hover_name=dimension, hover_data=[dimension, "Registros"],
                            color_discrete_sequence=["gold"], zoom=6, height=450, width=600)
    fig.update_layout(mapbox_style="carto-positron")
    # fig.update_layout(
    #     mapbox_style="white-bg",
    #     mapbox_layers=[
    #         {
    #             "below": 'traces',
    #             "sourcetype": "raster",
    #             "sourceattribution": "United States Geological Survey",
    #             "source": [
    #                 "https://basemap.nationalmap.gov/arcgis/rest/services/USGSImageryOnly/MapServer/tile/{z}/{y}/{x}"
    #             ]
    #         }
    #     ])

    fig.update_layout(title="<b>Cobertura geográfica</b><br>Ubicación de los sitios de monitoreo",
                      title_font_family="Roboto",
                      title_font_color="#333f54")

    return fig


# Deprecated table function. Plotly renders wrong some values in table.
# def create_one_variable_table(df, names):
#     header = "<b>Biomasa por " + names.lower() + "</b><br>"
#     description = "<i>Total de biomasa estimada por 250 metros cuadrados</i>"
#     colors = n_colors(color_gradients[0],
#                       color_gradients[-1],
#                       len(df["Biomass.250m2"].unique()),
#                       colortype='rgb')
#     fig = go.Figure(data=[go.Table(
#         header=dict(
#             values=["<b>" + i + "</b>" for i in df.columns],
#             line_color=None, fill_color="#333f54",
#             align='center', font=dict(color='white', size=11)
#         ),
#         cells=dict(
#             values=df.T.values,
#             line_color=None, fill_color=["white", colors],
#             align='center', font=dict(color=["black", "white"], size=11)
#         ))
#     ])
#
#     add_logo_to_charts(fig)
#
#     fig.update_layout(title=(header + description),
#                       title_font_family="Roboto",
#                       title_font_color="#333f54")
#
#     return fig

def create_one_variable_table(df, names):
    header = "Biomasa por " + names.lower()
    description = "Total de biomasa estimada por 250 metros cuadrados"
    table = html.Div(
        [
            html.Label(header, className="labels"),
            html.P(description, style={"fontStyle": "italic"}),
            dash_table.DataTable(
                id='table',
                columns=[{"name": i, "id": i} for i in df.columns],
                data=df.to_dict('records'),
                style_table={'overflowX': 'auto'},
                style_header={
                    "backgroundColor": "#333f54",
                    "fontWeight": "bold",
                    "color": "white",
                },
                style_cell={'textAlign': 'center',
                            'font-family': 'sans-serif',
                            'fontSize': 12},
                style_data_conditional=[
                    {
                        "if": {"state": "selected"},
                        "backgroundColor": "rgba(0, 116, 217, 0.3)",
                        "border": "1px solid #333f54",
                    }
                ]
            )
        ], style={"padding": "20px"}
    )

    return table


# Deprecated table funtion. Plotly renders wrong values.
# def create_two_variable_table(df, names_a, names_b):
#     header = "<b>Biomasa por " + names_a.lower() + " y por " + names_b.lower() + "</b><br>"
#     description = "<i>Total de biomasa estimada por 250 metros cuadrados</i>"
#     colors = n_colors(px.colors.sequential.Agsunset[0],
#                       px.colors.sequential.Agsunset[-1],
#                       sum([df[i].nunique() for i in df.columns][1:-1]),
#                       colortype='rgb')
#     fig = go.Figure(data=[go.Table(
#         header=dict(
#             values=["<b>" + i + "</b>" for i in df.columns],
#             line_color=None, fill_color="#333f54",
#             align='center', font=dict(color='white', size=11)
#         ),
#         cells=dict(
#             values=df.T.values,
#             line_color=None, fill_color=["white", "white", colors],
#             align='center', font=dict(color=["black", "black", "white"], size=11)
#         ))
#     ])
#
#     fig.update_layout(title=(header + description),
#                       title_font_family="Roboto",
#                       title_font_color="#333f54")
#
#     return fig


def create_two_variable_table(df, names_a, names_b):
    header = "Biomasa por " + names_a.lower() + " y por " + names_b.lower()
    description = "Total de biomasa estimada por 250 metros cuadrados"
    table = html.Div(
        [
            html.Label(header, className="labels"),
            html.P(description, style={"fontStyle": "italic"}),
            dash_table.DataTable(
                id='table',
                columns=[{"name": i, "id": i} for i in df.columns],
                data=df.to_dict('records'),
                style_table={'overflowX': 'auto'},
                style_header={
                    "backgroundColor": "#333f54",
                    "fontWeight": "bold",
                    "color": "white",
                },
                style_cell={'textAlign': 'center',
                            'font-family': 'sans-serif',
                            'fontSize': 12},
                style_data_conditional=[
                    {
                        "if": {"state": "selected"},
                        "backgroundColor": "rgba(0, 116, 217, 0.3)",
                        "border": "1px solid #333f54",
                    }
                ]
            )
        ], style={"padding": "20px"}
    )

    return table
