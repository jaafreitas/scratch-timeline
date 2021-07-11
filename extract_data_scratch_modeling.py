#TIMELINE FOR MODELING - VERSION 2021 06
import json
import csv
import pandas as pd
from matplotlib import pyplot
import plotly
import plotly.io as pio
from plotly.subplots import make_subplots
import plotly.graph_objects as go
from pathlib import Path
import dash
import dash_core_components as dcc
import dash_html_components as html
import base64 
import glob
import os
import re

def json_extract(obj, key):
    """Recursively fetch values from nested JSON."""
    arr = []

    def extract(obj, arr, key):
        """Recursively search for values of key in JSON tree."""
        if isinstance(obj, dict):
            for k, v in obj.items():
                if isinstance(v, (dict, list)):
                    extract(v, arr, key)
                elif k == key:
                    arr.append(v)
        elif isinstance(obj, list):
            for item in obj:
                extract(item, arr, key)
        return arr

    values = extract(obj, arr, key)
    return values

#open file
data_folder = Path(r".\")
file_to_open = data_folder / "timeline.json"

with open(file_to_open) as json_file:
    data = json.load(json_file)

# time_zero --> beggining of the project
time_zero = (int(next(iter(data))[0:10])) 
print(time_zero)
 

#new dictionary to save time and blocks
#not being used
newdict =  { }
dict_events = { }
dict_blocks = { }

#lists to save blocks and events
list_blocks = []
time_blocks = []

list_events = []
time_events = []

list_events_stop = []
time_events_stop = []

list_events_target = []
time_events_target = []

list_events_backdrop = []
time_events_backdrop = []

list_blocks_extension = []
time_blocks_extension = []

list_blocks_others = []
time_blocks_others = []

list_runstop = []
time_runstop = []

list_glow = []
time_glow = []

list_events_blockdrag = []
time_events_blockdrag = []

list_events_newsprite = []
time_events_newsprite = []

list_events_deletesprite = []
time_events_deletesprite = []

list_events_deleteblock = []
time_events_deleteblock = []

list_events_addblock = []
time_events_addblock = []

list_events_table = []
time_events_table = []

list_events_projectchanged = []
time_events_projectchanged = []



n_initial_blocks = 0 #Usado para quando é usado um programa exemplo como modelo - pode ser automatizado
size_bars = 5 #tamanho das barras nos gráficos


#reading and printing the time and the blocks used
for k in data:
    new_time = int(k[0:10]) - time_zero
    blocks = json_extract(data[k], 'opcode')
    if blocks: #se houver algum bloco neste momento
        #print ('chave:', k)
        #print('time(s):', new_time)
        print ('Number of blocks: ', len(blocks))
        #print('Blocks used: ', blocks)
        dict_blocks[new_time] = blocks #dictionary with blocks used at each time
        #print ('dict blocks: ',dict_blocks)
        newdict[new_time] = len(blocks)
        dict_events[new_time] = "0"
        #SALVANDO TAMBÉM COMO LISTA
        list_blocks.append(len(blocks) - n_initial_blocks)
        time_blocks.append(new_time)


#reading events and classnames 
#if the selected event is found, save the value 10 to a list
#the value is used to create a bar/line graph at that moment
    events  = json_extract(data[k], 'event')
    classname  = json_extract(data[k], 'classname')

    if 'PROJECT_RUN_START' in events: 
        print('time(s):', new_time)
        print('Run Start')
        dict_events[new_time] = size_bars 

        list_events.append(10)
        time_events.append(new_time)

        list_runstop.append(size_bars)
        time_runstop.append(new_time)

    if 'PROJECT_RUN_STOP' in events: 
        print('time(s):', new_time)
        print('Run Stop')
        dict_events[new_time] = size_bars

        list_events_stop.append(10)
        time_events_stop.append(new_time)

        list_runstop.append(0)
        time_runstop.append(new_time)


    if 'SCRIPT_GLOW_ON' in events: 
        list_glow.append(size_bars) 
        time_glow.append(new_time)

    if 'SCRIPT_GLOW_OFF' in events: 
        list_glow.append(0)
        time_glow.append(new_time)


    if 'BLOCK_DRAG_UPDATE' in events: 
        print('time(s):', new_time)
        print('Run Stop')
        dict_events[new_time] = size_bars

        list_events_blockdrag.append(10)
        time_events_blockdrag.append(new_time)

    #SVGSkin corresponde a mudanças tanto no palco quanto no backdrop
    if 'SVGSkin' in classname:
        list_events_backdrop.append(size_bars)
        time_events_backdrop.append(new_time)
    else: 
        list_events_backdrop.append(0)
        time_events_backdrop.append(new_time)


    if  'PROJECT_CHANGED' in events: 
        list_events_projectchanged.append(size_bars)
        time_events_projectchanged.append(new_time)
    else: 
        list_events_projectchanged.append(0)
        time_events_projectchanged.append(new_time)

    if 'addSprite*' in events:
        list_events_newsprite.append(size_bars)
        time_events_newsprite.append(new_time)
    else: 
        list_events_newsprite.append(0)
        time_events_newsprite.append(new_time)

    if 'deleteBlock*' in events:
        list_events_deleteblock.append(size_bars)
        time_events_deleteblock.append(new_time)
    else: 
        list_events_deleteblock.append(0)
        time_events_deleteblock.append(new_time)

    if 'createBlock*' in events:
        list_events_addblock.append(size_bars)
        time_events_addblock.append(new_time)
    else: 
        list_events_addblock.append(0)
        time_events_addblock.append(new_time)

    if 'deleteSprite*' in events:
        list_events_deletesprite.append(size_bars)
        time_events_deletesprite.append(new_time)
    else:
        if 'targetWasRemoved*' in events:
            list_events_deletesprite.append(size_bars)
            time_events_deletesprite.append(new_time) 
        else: 
            list_events_deletesprite.append(0)
            time_events_deletesprite.append(new_time)


    if 'openDataviewerTable*' in events:
        list_events_table.append(size_bars)
        time_events_table.append(new_time)

    if 'closeDataviewerTable*' in events:
        list_events_table.append(0)
        time_events_table.append(new_time)


#Gráficos com Graph Object
fig = go.Figure()
fig = make_subplots(rows=5, cols=1, 
                    shared_xaxes=True,
                    vertical_spacing=0.1)

fig.add_trace(go.Bar(
    x=time_runstop,
    y=list_runstop,
    width=5, 
    name = 'Project Running'
), 
    row=2, col=1
)

fig.add_trace(go.Scatter(
    x=time_glow,
    y=list_glow,
    mode = 'lines',
    name = 'Project Glow',
    fill="tozeroy",
    line = dict(width=1, shape = 'hv') #shape hv define que é uma linha do tipo step
), 
    row=2, col=1
)

fig.add_trace(go.Scatter(
    x=time_events_table,
    y=list_events_table,
    mode = 'lines',
    name = 'Table open',
    fill="tozeroy",
    line = dict(color='seagreen', width=1, shape = 'hv') 
), 
    row=1, col=1
)

fig.add_trace(go.Scatter(
    x=time_blocks,
    y=list_blocks,
    #mode = 'lines+markers',
    name = 'Blocks used',
    fill="tozeroy",
    line = dict(color='lightsteelblue', width=1, shape = 'hv') 
    ), 
    row=4, col=1
)

fig.add_trace(go.Bar(
    x=time_events_blockdrag,
    y=list_events_blockdrag, 
    width= 5 , 
    name = 'Block drag'
), 
    row=5, col=1
)

fig.add_trace(go.Bar(
    x=time_events_newsprite,
    y=list_events_newsprite, 
    width= 5 , #largura da barra - vai variar dependendo do tempo total do arquivo
    name = 'New sprite added'
), 
    row=1, col=1
)

fig.add_trace(go.Bar(
    x=time_events_deletesprite,
    y=list_events_deletesprite, 
    width= 5 ,
    name = 'Sprite deleted'
), 
    row=1, col=1
)

fig.add_trace(go.Bar(
    x=time_events_deleteblock,
    y=list_events_deleteblock, 
    width= 5 , 
    name = 'Block deleted'
), 
    row=3, col=1
)

fig.add_trace(go.Bar(
    x=time_events_addblock,
    y=list_events_addblock, 
    width= 5 , 
    name = 'Block added'
), 
    row=3, col=1
)



fig.add_trace(go.Scatter(
    x = time_events_backdrop,
    y= list_events_backdrop,
    name = 'Editing backdrop or costume',
    mode = 'lines',
    fill="tozeroy",
    line = dict(color='midnightblue', width=1, shape = 'hv'),
), 
    row=1, col=1
)

fig.update_layout(
    showlegend=True, 
    plot_bgcolor='rgba(0,0,0,0)',
    legend=dict(
    orientation="h",
    yanchor="bottom",
    y=-0.4,
    xanchor="center",
    x=0.5,
    ),
    font = dict(size = 8), 
)

#fig.update_yaxes(title_text="# of blocks")
#fig.update_xaxes(title_text="time (s)")


#Adicionando as imagens (screenshots) ao gráfico
list_images =  []
list_new_images = []

file_images = glob.glob(os.path.join(data_folder, '*.jpg')) #adiciona todas as imagens da pasta a uma lista

print (file_images)
for fname in file_images:
    res = re.findall("timeline_(\d+).jpg", fname)
    if not res: continue
    file_new_images = res[0] #res[0] é o número da cada arquivo de imagem, correspondente ao tempo em que foi salvo
    list_images.append(res[0]) 
    new_image_time = int(file_new_images[0:10]) - time_zero
    list_new_images.append(new_image_time) 
#print (list_images)

#adding local images to the plot
#adicionando múltiplas imagens - uma para cada run
i=0
length = len(list_images)
for i in range(length):
    image_filename = file_images[i]  #nome da imagem
    screenshot = base64.b64encode(open(data_folder / image_filename, 'rb').read())
    fig.add_layout_image(dict(
        source='data:image/jpg;base64,{}'.format(screenshot.decode()),
        x=list_new_images[i], 
        y=1,
        xref="x",
        yref="paper",
        )
    )

fig.update_layout_images(dict(
        sizex= 50,#(time_events[-1])/8, #tamanho da imagem - tempo total/10
        sizey=20, # time_events[-1])/10, 
        xanchor="right",
        yanchor="bottom"
))


#salvando o dicionário com os blocos a cada time como csv
#não está sendo usao no momento
with open('blocks used.csv', 'w') as f:  
    w = csv.DictWriter(f, dict_blocks.keys())
    w.writeheader()
    w.writerow(dict_blocks)


#visualizando os gráficos com Dash
app = dash.Dash()
app.layout = html.Div([
    dcc.Graph(figure=fig)
])

app.run_server(debug=True, port=3010)
