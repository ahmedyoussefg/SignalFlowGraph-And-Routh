from dash import Dash, html, dcc, Input, Output, State, callback
import dash
import dash_cytoscape as cyto

cyto.load_extra_layouts()

app = Dash(__name__)

# Initial elements
elements = [
    {'data': {'id': 'A', 'label': 'A'}},
    {'data': {'id': 'B', 'label': 'B'}},
    {'data': {'id': 'C', 'label': 'C'}},
    {'data': {'id': 'D', 'label': 'D'}},
    {'data': {'source': 'A', 'target': 'B', 'weight': '5'}},
    {'data': {'source': 'B', 'target': 'C', 'weight': '3'}},
    {'data': {'source': 'C', 'target': 'D', 'weight': '2'}},
    {'data': {'source': 'D', 'target': 'A', 'weight': '4'}}
]

# Define the app layout
app.layout = html.Div([
    cyto.Cytoscape(
        id='cytoscape',
        elements=elements,
        style={'width': '100%', 'height': '400px'},
        layout={'name': 'dagre',
                'animate': True,
                'rankDir': 'LR',
                'acyclicer': 'greedy',
                'nodeDimensionsIncludeLabels':True,
                # 'align': 'DR',
                
                },
        stylesheet=[
            {'selector': 'node', 'style': {'label': 'data(label)'}},
            {'selector': 'edge', 'style': {'curve-style': 'bezier', 'target-arrow-shape': 'triangle', 'label': 'data(weight)'}}
        ]
    ),
    html.Div([
        dcc.Input(id='input-edge-weight', type='text', placeholder='Enter edge weight'),
        html.Button('Add Edge', id='add-edge-button'),
    ]),
    html.Div([
        dcc.Input(id='input-node-name', type='text', placeholder='Enter node name'),
        html.Button('Add Node', id='add-node-button')
    ]),
    html.Div(id='output-container')
])

# Callback for adding an edge
@callback(
    Output('cytoscape', 'elements',allow_duplicate=True),
    Input('add-edge-button', 'n_clicks'),
    State('cytoscape', 'selectedNodeData'),
    State('input-edge-weight', 'value'),
    State('cytoscape', 'elements'),
    prevent_initial_call=True)
def add_edge(n_clicks, selected_nodes, weight, elements):
    if n_clicks is None or not selected_nodes or weight is None:
        raise dash.exceptions.PreventUpdate
    # Assuming selected_edges is a list of dicts with 'source' and 'target'
    source = selected_nodes[0]['label']
    target = selected_nodes[1]['label']
    new_edge = {'data': {'source': source, 'target': target, 'weight': weight}}
    elements.append(new_edge)
    return elements

# Callback for adding a node
@callback(
    Output('cytoscape', 'elements',allow_duplicate=True),
    Input('add-node-button', 'n_clicks'),
    State('input-node-name', 'value'),
    State('cytoscape', 'elements'),
    prevent_initial_call=True)
def add_node(n_clicks, node_name, elements):
    if n_clicks is None or node_name is None:
        raise dash.exceptions.PreventUpdate
    new_node = {'data': {'id': node_name, 'label': node_name}}
    elements.append(new_node)
    return elements

if __name__ == '__main__':
    app.run_server(debug=False)
