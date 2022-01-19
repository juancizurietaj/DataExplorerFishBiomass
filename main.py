import os
import pandas as pd
import numpy as np
import dash
from dash import dcc, html, Input, Output, State
import plotly.graph_objects as go
import dash_bootstrap_components as dbc
from helpers import *

# Data loading
data = pd.read_feather(r"C:\Users\juancarlos.izurieta\PycharmProjects\KnowingMoreMarine\data\fish.feather")

# App definition
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.FLATLY])

# Controls
bioregion_selection = checklist_creator(data, "Bioregion", _id="bioregion-selection")
zone_selection = checklist_creator(data, "Subzone.name", _id="zone-selection")
island_selection = checklist_creator(data, "Island", _id="island-selection")
order_selection = checklist_creator(data, "ORDER", _id="order-selection")
family_selection = checklist_creator(data, "Family", _id="family-selection")
functional_group_selection = checklist_creator(data, "Functional.Group", _id="functional-group-selection")
season_selection = dbc.Checklist(id="season-selection",
                                 options=[{"label": i, 'value': i} for i in data["epoca"].dropna().unique()],
                                 value=["Fría", "Caliente"],
                                 switch=True)
years = data["year"].dropna().unique()
year_selection = dcc.RangeSlider(id="year-selection",
                                 min=years[0],
                                 max=years[-1],
                                 value=[years[0], years[-1]],
                                 tooltip={"placement": "bottom", "always_visible": True})

# Controls layout (accordion)
controls = html.Div(
    [
        html.Label("Filtros y controles", className="labels"),
        html.Br(),
        html.Br(),
        dbc.Accordion(
            dbc.AccordionItem(
                title="Filtros temporales",
                children=[html.Label("Época", className="subLabels"),
                          season_selection,
                          html.Br(),
                          html.Label("Años", className="subLabels"),
                          year_selection]
            ),
            # flush=True,
            start_collapsed=True
        ),
        html.Br(),
        dbc.Accordion(
            dbc.AccordionItem(
                title="Filtros geográficos",
                children=[
                    html.Label("Bioregión", className="subLabels"),
                    check_all_creator("bioregion-all-checked"),
                    bioregion_selection,
                    html.Br(),

                    html.Label("Zona", className="subLabels"),
                    check_all_creator("zone-all-checked"),
                    zone_selection,
                    html.Br(),

                    html.Label("Isla", className="subLabels"),
                    check_all_creator("island-all-checked"),
                    island_selection
                ]
            ),
            # flush=True,
            start_collapsed=True
        ),
        html.Br(),
        dbc.Accordion(
            dbc.AccordionItem(
                title="Filtros taxonómicos",
                children=[
                    dbc.Accordion(
                        dbc.AccordionItem(title="Orden",
                                          children=[check_all_creator("order-all-checked"),
                                                    order_selection]),
                        start_collapsed=True,
                        flush=True
                    ),

                    html.Br(),

                    dbc.Accordion(
                        dbc.AccordionItem(title="Familia",
                                          children=[check_all_creator("family-all-checked"),
                                                    family_selection]),
                        start_collapsed=True,
                        flush=True
                    ),
                ]
            ),
            # flush=True,
            start_collapsed=True
        )

    ]
)

# Chart controls
variable_one = dcc.Dropdown(id="variable-one",
                            options=[{"label": i, 'value': i} for i in data.select_dtypes([object]).columns],
                            placeholder="Seleccione una variable",
                            value="Bioregion", clearable=False)

add_second_variable = dbc.Checklist(id="add-second-variable",
                                    options=[{"label": "Añadir otra métrica al gráfico", "value": False}],
                                    value=False,
                                    switch=True)

chart_controls = html.Div(
    children=[
        html.Label("Métrica", className="labels"),
        variable_one,
        add_second_variable,
        html.Div(dcc.Dropdown(id="variable-two",
                              options=[{"label": i, 'value': i} for i in
                                       data.select_dtypes([object]).columns],
                              placeholder="Seleccione una variable",
                              value="Functional.Group", disabled=True, clearable=False))
    ]
)

# Charts
charts = html.Div(
    children=[
        dcc.Graph("chart", config={'displayModeBar': False}),
        html.Button("Descargar imagen", id="btn-image", className="download-button"),
        dcc.Download(id="download-image")
    ]
)

# Tab layout: charts
chart_tab_sections = html.Div(
    dbc.Row(
        [
            dbc.Col(dbc.Card(controls, body=True),
                    width=3,
                    style={"marginTop": "20px"},
                    id="controls-col"),
            dbc.Col([dbc.Card(chart_controls, body=True),
                     html.Br(),
                     dbc.Card(charts, body=True)],
                    width=9,
                    style={"marginTop": "20px"},
                    id="charts-col")
        ], style={"display": "flex"}, id="controls"
    )
)

# Tabs
tab2 = tab_creator("GRÁFICOS", chart_tab_sections)
tab3 = tab_creator("MAPAS", "PENDIENTE")
tab4 = tab_creator("DESCARGAS", "DESCARGAS")

share_icon = html.Img(
    src="https://cdn-icons.flaticon.com/png/512/1358/premium/1358023.png?token=exp=1642524724~hmac=72a76b6f63a9bfbcaac9cfe95820576a",
    height="15px")
tab5 = tab_creator(list(share_icon), share_icon)
tabs = dbc.Tabs([tab2, tab3, tab4, tab5])

# App layout
app.layout = html.Div(
    [
        header,
        tabs
    ], style={"width": "99%"}  # This avoids the horizontal scroll bar
)


# Callbacks
@app.callback(
    Output("download-image", "data"),
    Input("btn-image", "n_clicks"),
    Input("chart", "figure")
)
def func(n_clicks, chart_dict):
    file_name = chart_dict["layout"]["title"]["text"]
    idx1 = file_name.index("<b>")
    idx2 = file_name.index("</b>")
    file_name = file_name[idx1 + len("<b>"): idx2] + ".png"
    if n_clicks:
        fig = go.Figure(chart_dict)
        fig.write_image(file_name)
        return dcc.send_file(file_name)


@app.callback(
    Output("bioregion-selection", "value"),
    Output("zone-selection", "value"),
    Output("island-selection", "value"),
    Output("order-selection", "value"),
    Output("family-selection", "value"),
    Input("bioregion-all-checked", "value"),
    Input("zone-all-checked", "value"),
    Input("island-all-checked", "value"),
    Input("order-all-checked", "value"),
    Input("family-all-checked", "value"),
    State("bioregion-selection", "options"),
    State("zone-selection", "options"),
    State("island-selection", "options"),
    State("order-selection", "options"),
    State("family-selection", "options")
)
def select_all(checkA, checkB, checkC, checkD, checkE, bioregion_options, zone_options, island_options, order_options,
               family_options):
    bioregion_all = []
    bioregion_all = [i["value"] for i in bioregion_options if checkA]
    zone_all = []
    zone_all = [i["value"] for i in zone_options if checkB]
    island_all = []
    island_all = [i["value"] for i in island_options if checkC]
    order_all = []
    order_all = [i["value"] for i in order_options if checkD]
    family_all = []
    family_all = [i["value"] for i in family_options if checkE]

    return bioregion_all, zone_all, island_all, order_all, family_all


@app.callback(
    Output("variable-two", "disabled"),
    Input("add-second-variable", "value"),
    State("variable-two", "disabled")
)
def generate_second_variable_input(check, status):
    if check:
        status = False
    else:
        status = True
    return status


@app.callback(
    Output("chart", "figure"),
    Input("variable-one", "value"),
    Input("add-second-variable", "value"),
    Input("variable-two", "value"),
    Input("bioregion-selection", "value"),
    Input("zone-selection", "value"),
    Input("island-selection", "value"),
    Input("order-selection", "value"),
    Input("family-selection", "value"),
    Input("season-selection", "value"),
    Input("year-selection", "value")
)
def generate_figures(variable_one, check, variable_two, selectionA, selectionB, selectionC, selectionD, selectionE,
                     selectionF, selectionG):
    # Year range generates top and bottom years, a sequence need to be created:
    selectionG = np.arange(selectionG[0], selectionG[-1]).tolist()
    # Create a list of selections to use later:
    selections = [selectionA, selectionB, selectionC, selectionD, selectionE, selectionF, selectionG]

    data_copy = data.copy(deep=True)

    if selections:
        data_copy = data_copy[
            data_copy["Bioregion"].isin(selections[0]) &
            data_copy["Subzone.name"].isin(selections[1]) &
            data_copy["Island"].isin(selections[2]) &
            data_copy["ORDER"].isin(selections[3]) &
            data_copy["Family"].isin(selections[4]) &
            data_copy["epoca"].isin(selections[5]) &
            data_copy["year"].isin(selections[6])]
        data_copy = pd.DataFrame(data_copy)
        data_copy.reset_index(col_level=1, inplace=True)

    if variable_two is None:
        # PreventUpdate prevents ALL outputs updating
        raise dash.exceptions.PreventUpdate

    df = data_copy.groupby(variable_one)["Biomass.250m2"].sum()
    df = pd.DataFrame(df).sort_values("Biomass.250m2")
    df = df[df["Biomass.250m2"] > 0]
    df.reset_index(col_level=0, inplace=True)
    fig1 = bar_chart_creator(df, variable_one)
    if check:
        df = data_copy.groupby([variable_one, variable_two]).agg({"Biomass.250m2": "sum"})
        df.reset_index(col_level=0, inplace=True)
        df = pd.crosstab(index=df[variable_one], columns=df[variable_two], values=df["Biomass.250m2"], aggfunc="sum")
        df.reset_index(col_level=0, inplace=True)
        fig1 = bivariate_bar_chart_creator(df, variable_one, variable_two)
    return fig1


if __name__ == '__main__':
    app.run_server(debug=True)
