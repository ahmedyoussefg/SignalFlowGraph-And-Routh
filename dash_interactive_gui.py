from dash import Dash, html, dcc, Input, Output, State, callback
import dash
import dash_cytoscape as cyto
from SignalFlowGraph import SignalFlowGraph
cyto.load_extra_layouts()

app = Dash(__name__)
app.title='Signal Flow Solver'
app._favicon='./assets/icon/favicon.ico'
# Initial elements
elements = [
    {'data': {'id': 'A', 'label': 'A'}},
    {'data': {'id': 'B', 'label': 'B'}},
    {'data': {'id': 'C', 'label': 'C'}},
    {'data': {'id': 'D', 'label': 'D'}},
    # {'data': {'id': 'E', 'label': 'E'}},
    {'data': {'source': 'A', 'target': 'B', 'weight': '5'}},
    {'data': {'source': 'B', 'target': 'C', 'weight': '3'}},
    {'data': {'source': 'C', 'target': 'D', 'weight': '2'}},
    # {'data': {'source': 'D', 'target': 'A', 'weight': '4'}}
]

# Define the app layout
app.layout = html.Div([
    cyto.Cytoscape(
        id='cytoscape',
        elements=elements,
        style={'width': '100%', 'height': '90vh'},
        layout={'name': 'dagre',
                'animate': True,
                'rankDir': 'LR',
                'acyclicer': 'greedy',
                'nodeDimensionsIncludeLabels':True,
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
    html.Div([
        html.Button('Solve', id='solve-button', style={'display': 'inline-block', 'background-color': 'green', 'color': 'white', 'border': 'none', 'border-radius': '5px', 'cursor': 'pointer'}),
        html.Button('Delete Node', id='delete-node-button', style={'margin': '1vh', 'display': 'inline-block', 'background-color': 'red', 'color': 'white', 'border': 'none', 'border-radius': '5px', 'cursor': 'pointer'})
    ]),
    html.Div(id='overlay-container', style={'position': 'absolute', 'top': 0, 'left': 0, 'width': '100%', 'height': '100%', 'background-color': 'rgba(255, 255, 255, 0.5)', 'display': 'none'}, children=[
        
        html.Div(style={'display': 'flex', 'justify-content': 'center', 'text-align': 'center', 'width':'100%'}, children=[
            html.H1('Results')
        ]),

        html.Div(id='output-container', style={'min-height':'82vh', 'display': 'flex', 'flex-flow': 'row wrap', 'gap': '5vh', 'flex-wrap':'wrap', 'top': '20%', 'left': '10%', 'background-color': 'rgba(255, 255, 255, 0.7)', 'border-radius': '10px', 'padding': '20px'}, children=[
            html.H1('Results'),
            html.Div(['Forward Paths:', html.Br(), 'hello world']),
            html.Div('Loops:'),
            html.Div('Non-touching Loops:'),
            html.Div('Overall Transfer Function:')
        ]),
        html.Div(style={'display': 'flex', 'justify-content': 'center', 'text-align': 'center', 'width':'100%'}, children=[
        ]),
        html.Button('Close', id='close-button', style={'position': 'fixed', 'left':'50%', 'margin':'0 auto', 'transform': 'translate(-50%, -50%)', 'padding': '10px 20px', 'background-color': '#ff6347', 'color': 'white', 'border': 'none', 'border-radius': '5px', 'cursor': 'pointer'})
    ])
])

# Callback for adding an edge
@callback(
    Output('cytoscape', 'elements', allow_duplicate=True),
    Input('add-edge-button', 'n_clicks'),
    State('cytoscape', 'selectedNodeData'),
    State('input-edge-weight', 'value'),
    State('cytoscape', 'elements'),
    prevent_initial_call=True)
def add_edge(n_clicks, selected_nodes, weight, elements):
    if n_clicks is None or not selected_nodes or weight is None:
        raise dash.exceptions.PreventUpdate
    source = selected_nodes[0]['label']
    if len(selected_nodes) >= 2:
        target = selected_nodes[1]['label']
    else:
        target=source
    new_edge = {'data': {'source': source, 'target': target, 'weight': weight}}
    elements.append(new_edge)
    return elements

# Callback for adding a node
@callback(
    Output('cytoscape', 'elements', allow_duplicate=True),
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

# Callback for delete a node
@callback(
    Output('cytoscape', 'elements', allow_duplicate=True),
    Input('delete-node-button', 'n_clicks'),
    State('cytoscape', 'selectedNodeData'),
    State('cytoscape', 'elements'),
    prevent_initial_call=True)
def delete_node(n_clicks, selected_nodes, elements):
    if n_clicks is None or not selected_nodes:
        raise dash.exceptions.PreventUpdate
    for node in selected_nodes:
        node_id = node['id']
        for element in elements:
            if 'source' in element['data']:
                if element['data']['source'] == node_id or element['data']['target'] == node_id:
                    elements.remove(element)
            elif element['data']['id'] == node_id:
                elements.remove(element)
    # elements = [element for element in elements if element['data']['id'] != node_id and element['data']['source'] != node_id and element['data']['target'] != node_id]
    return elements

def solve(elements):
    graph = parse_elements(elements)

    sfg_solve = SignalFlowGraph(graph)
    forward_paths = sfg_solve.get_forward_paths()
    loops = sfg_solve.find_loops()
    all_non_touching_loops = sfg_solve.get_all_non_touching_loops()


    forward_paths_gains = sfg_solve.calculate_forward_path_gains()
    forward_paths_delta = sfg_solve.calculate_paths_delta()

    output_divs = []
    overall_transfer_function = round(sfg_solve.calculate_overall_transfer_function(), 4)
    overall_delta = round(sfg_solve.calculate_overall_delta(), 4)
    input_node = sfg_solve.find_input_node()
    output_node = sfg_solve.find_output_node()

    output_divs.append(html.Div([
        html.Div(f'Input Node: {input_node}', style={'font-weight': 'bold', 'display': 'block'}),
        html.Div(f'Output Node: {output_node}', style={'font-weight': 'bold', 'display': 'block'}),
        html.Div(f'Overall Transfer Function: {overall_transfer_function}', style={'font-weight': 'bold', 'display': 'block'}),
        html.Div(f'Overall Delta: {overall_delta}', style={'font-weight': 'bold'})
    ]))


    forward_path_html = []
    forward_path_html.append(html.Div(f'Number Of Forward Paths: {len(forward_paths)}', style={'font-weight': 'bold'}))  # Bold text
    for i, path in enumerate(forward_paths):
        forward_path_html.append(html.Div(f'Forward Path {i+1}: {path}'))
        forward_path_html.append(html.Div(f'Gain: {round(forward_paths_gains[i], 4)}'))
        forward_path_html.append(html.Div(f'Delta: {round(forward_paths_delta[i], 4)}'))
        forward_path_html.append(html.Div(html.Hr())) 

    output_divs.append(html.Div(forward_path_html, style = {'border': '1px solid black', 'border-radius': '2vh', 'padding': '1vh', 'background-color': 'rgba(180, 230, 197, 0.5)', 'height': '10%'}))

    loop_gains = sfg_solve.calculate_loop_gains()
    loops_html = []
    loops_html.append(html.Div(f'Number Of Loops: {len(loops)}', style={'font-weight': 'bold'}))
    for i, loop in enumerate(loops):
        loops_html.append(html.Div(f'Loop {i+1}: {loop}'))
        loops_html.append(html.Div(f'Gain: {round(loop_gains[i], 4)}'))
        loops_html.append(html.Div(html.Hr()))

    output_divs.append(html.Div(loops_html, style={'flex-shrink':'3', 'border': '1px solid black', 'border-radius': '2vh', 'padding': '1vh', 'height': '10%'}))

    counter = 2
    for list_of_loops in all_non_touching_loops:
        non_touching_loops_html = []
        non_touching_loops_html.append(html.Div(f'All {counter} Non-touching loops:', style={'font-weight': 'bold'}))
        counter += 1
        for loops in list_of_loops:
            for loop in loops:
                non_touching_loops_html.append(html.Div(f'Loop: {sfg_solve.loops[loop]}', style={'margin-bottom': '5px'}))
            non_touching_loops_html.append(html.Div(html.Hr()))
        non_touching_loops_html.append(html.Div(html.Hr()))
        output_divs.append(html.Div(non_touching_loops_html, style={'flex-shrink':'3', 'border': '1px solid black', 'border-radius': '2vh', 'padding': '1vh', 'height': '10%'}))

    return output_divs

# Callback to show/hide overlay and output container
@callback(
    # Output('overlay-container', 'children'),
    Output('output-container', 'children'),
    Output('overlay-container', 'style'),
    Input('solve-button', 'n_clicks'),
    Input('close-button', 'n_clicks'),
    State('cytoscape', 'elements'),
    prevent_initial_call=True
)
def toggle_overlay(solve_clicks, close_clicks, elements):
    ctx = dash.callback_context

    if ctx.triggered_id == 'solve-button' and solve_clicks:
        solver = solve(elements)
        
        return solver, {'display': 'block', 'position': 'absolute', 'top': 0, 'left': 0, 'width': '100%', 'height': '100%', 'background-color': 'rgba(255, 255, 255, 0.5)'}
    
    return dash.no_update, {'display': 'none', 'position': 'absolute', 'top': 0, 'left': 0, 'width': '100%', 'height': '100%', 'background-color': 'rgba(255, 255, 255, 0.5)'}


def parse_elements(elements):
    graph = {}
    for element in elements:
        if 'source' in element['data']:
            source = element['data']['source']
            target = element['data']['target']
            weight = float(element['data']['weight'])
            if source in graph:
                graph[source].append((target, weight))
            else:
                graph[source] = [(target, weight)]
        else:
            node = element['data']['id']
            if node not in graph:
                graph[node] = []
    return graph

if __name__ == '__main__':
    app.run_server(debug=False)
