from dash import Dash, html, dcc, Input, Output, State, exceptions
import dash_cytoscape as cyto

app = Dash(__name__)

# Initial elements
elements = [
    {'data': {'id': 'A', 'label': 'Node A'}},
    {'data': {'id': 'B', 'label': 'Node B'}},
    {'data': {'id': 'C', 'label': 'Node C'}},
    {'data': {'id': 'D', 'label': 'Node D'}},
    {'data': {'source': 'A', 'target': 'B'}},
    {'data': {'source': 'B', 'target': 'C'}},
    {'data': {'source': 'C', 'target': 'D'}},
    {'data': {'source': 'D', 'target': 'A'}}
]

# Define the app layout
app.layout = html.Div([
    cyto.Cytoscape(
        id='cytoscape',
        elements=elements,
        style={'width': '100%', 'height': '400px'},
        layout={'name': 'cose'}
    ),
    html.Div([
        dcc.Input(id='input-node-name', type='text', placeholder='Enter node name'),
        html.Button('Add Node', id='add-node-button')
    ]),
    html.Div(id='output-container')
])

# Callback for adding a node
@app.callback(
    Output('cytoscape', 'elements'),
    Input('add-node-button', 'n_clicks'),
    State('input-node-name', 'value'),
    State('cytoscape', 'elements'))
def add_node(n_clicks, node_name, elements):
    if n_clicks is None or node_name is None:
        raise exceptions.PreventUpdate
    new_node = {'data': {'id': node_name, 'label': node_name}}
    elements.append(new_node)
    return elements

if __name__ == '__main__':
    app.run_server(debug=False)
