import dash_bootstrap_components as dbc
import plotly_express as px
from dash import html

header = html.Div(
    [
        html.Img(src=r"./assets/fcd_logo_white.png",
                 width="130px",
                 style={'display': 'inline-block', "padding": "10px"}),
        html.H4("Data explorer: Biomasa en peces",
                style={'display': 'inline-block', "color": "white", 'marginLeft': 30, "bottom": 0})
    ], style={"background": "#333f54", 'display': 'inline-block', "width": "100%"}
)


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


def add_logo_to_charts(fig):
    image_path = r"./assets/fcd_logo.png"
    fig = fig.add_layout_image(
        dict(
            source=image_path,
            xref="paper", yref="paper",
            x=1, y=1,
            sizex=0.2, sizey=0.2,
            xanchor="right", yanchor="bottom"
        )
    )

    return fig


def bar_chart_creator(df, names):
    header = "<b>Biomasa por " + names.lower() + "</b><br>"
    description = "<i>Total de biomasa estimada por 250 metros cuadrados</i>"
    fig = px.bar(df, x="Biomass.250m2", y=names, color="Biomass.250m2",
                 color_discrete_sequence=px.colors.sequential.Agsunset)
    add_logo_to_charts(fig)
    fig.update_layout(title=(header + description),
                      title_font_family="Roboto",
                      title_font_color="#333f54")
    return fig


def bivariate_bar_chart_creator(df, names_x, names_y):
    header = "<b>Biomasa por " + names_x.lower() + " y por " + names_y.lower() + "</b><br>"
    description = "<i>Total de biomasa estimada por 250 metros cuadrados</i>"
    fig = px.bar(df, x=names_x, y=df.columns[1:],
                 color_discrete_sequence=px.colors.sequential.Agsunset,
                 labels={"value": "Biomasa por 250 m2",
                         "variable": names_y})
    add_logo_to_charts(fig)
    fig.update_layout(title=(header + description),
                      title_font_family="Roboto",
                      title_font_color="#333f54")
    print(df.columns)
    return fig


def donut_creator(df, names, values):
    fig = px.pie(data_frame=df,
                 names=names,
                 values=values,
                 hole=0.5,
                 color_discrete_sequence=px.colors.sequential.Agsunset)
    # print(px.colors.sequential.Agsunset)
    fig.update_layout(legend=dict(
        orientation="h",
        yanchor="bottom",
        xanchor="center",
        x=0.5
    ))
    return fig
