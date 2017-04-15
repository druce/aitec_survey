import numpy as np
import pandas as pd

from plotly.offline import download_plotlyjs, init_notebook_mode, iplot
from plotly.graph_objs import *

from IPython.display import HTML
#import colorlover as cl

# bar chart - all responses in single column (radio button)
# TODO: show %

chart_width=720
chart_height=580

aitec_colors = ['rgb(51,160,44)',
                'rgb(227,26,28)',
                'rgb(31,120,180)',
                'rgb(255,127,0)',
                'rgb(106,61,154)',
                'rgb(255,237,111)',
                'rgb(177,89,40)',
                'rgb(178,223,138)',
                'rgb(251,154,153)',
                'rgb(166,206,227)',
                'rgb(253,191,111)',
                'rgb(202,178,214)',
                'rgb(255,255,153)',
                'rgb(141,211,199)',
                'rgb(190,186,218)',
                'rgb(251,128,114)',
                'rgb(128,177,211)',
                'rgb(253,180,98)',
                'rgb(179,222,105)',
                'rgb(252,205,229)',
                'rgb(217,217,217)',
                'rgb(188,128,189)',
                'rgb(204,235,197)',
]

aitec_color_dict = {'div': {},
                    'qual': {'AITEC': aitec_colors,},
                    'seq': {}}

#HTML(cl.to_html( cl.scales['12'] )) # All scales with 12 colors
#HTML(cl.to_html( aitec_color_dict )) # AITEC colors grabbed from above

def aitec_bar(chartdata, question_col, title, x_label, y_label, col_order=None, **kwargs):
    """Take chart column, dataframe, options, create simple bar chart"""
    chartframe = chartdata[[question_col]]
    chartframe.columns = ['col_name']
    countframe = pd.DataFrame(chartframe['col_name'].value_counts(sort=True, ascending=False,dropna=True))
    if col_order is not None:
        order_dict = dict(zip(col_order, range(len(col_order))))
        countframe["order"] = [order_dict[v] for v in countframe.index.values]
        countframe = countframe.sort_values("order")
        del countframe["order"]
    
    layout = aitec_bar_layout(title, x_label, y_label, **kwargs)

    data = [Bar(
            x = countframe.index.tolist(),
            y = countframe.col_name.tolist(),
            marker=dict(color=aitec_colors),
            opacity=0.9,
        )
    ]
    
    return dict(data=data, layout=layout)

# bar chart - responses across multiple column (checkbox button)
def aitec_bar_multi(chartdata,
                    question_cols,
                    title,
                    x_label,
                    y_label,
                    col_order=None,
                    show_no_answer=True,
                    **kwargs
                    ):
                    
    """Take chart columns, dataframe, options, create simple bar chart"""

    colnames = chartdata.columns[question_cols]
    chartframe = chartdata[colnames]

    if show_no_answer:
        # add no answer column where all in row are null
        allnulls = chartframe.isnull().all(axis=1)
        replace_list = ["No Answer" if an else None for an in allnulls]
        chartframe.assign(No_Answer=pd.Series(replace_list))
        colnames = chartframe.columns
        
    # melt multiple columns into 1, i.e. gather/unflatten
    colnums = ["%d" % i for i in range(len(colnames))]
    chartframe.columns= colnums
    meltframe = pd.melt(chartframe, value_vars=colnums)
    
    # count occurrences of each response
    countframe = meltframe['value'].value_counts(sort=True, ascending=False,dropna=True)

    if col_order is not None: # use order provided
        order_dict = dict(zip(col_order, range(len(col_order))))
        countframe["order"] = [order_dict[v] for v in countframe.index.values]
        countframe = countframe.sort_values("order")
        del countframe["order"]
    
    # return plotly chart spec, data and layout
    layout = aitec_bar_layout(title, x_label, y_label, **kwargs)

    data = [Bar(
        x = countframe.index.tolist(),
        y = countframe.tolist(),
        marker=dict(color=aitec_colors),
        opacity=0.9,
        )
    ]
    
    return dict(data=data, layout=layout)

def aitec_barstack(tracedict, title, x_label, y_label, col_order=None):
    """takes a dict 'name' : dataframe pairs, plot count column (could prob use cleanup)"""
    layout = aitec_barstack_layout(title, x_label, y_label)

    group_colors = [aitec_colors[1], 
                    aitec_colors[3], 
                    aitec_colors[2],
                    aitec_colors[8], 
                   ]
    group_colors.reverse()
    
    data=[]

    keylist = tracedict.keys()
    for key in keylist:
        trace = tracedict[key]
        trace1 = Bar(
            x=trace.index.values.tolist(),
            y=trace['count'].tolist(),
            name=key,
            marker={
                'color' : group_colors.pop(),
            },
            opacity=0.9,
        )
        data.append(trace1)
        
    return dict(data=data, layout=layout)

def aitec_bargroup(tracedict, title, x_label, y_label, col_order=None):
    """takes a dict 'name' : dataframe pairs"""
    layout = aitec_bargroup_layout(title, x_label, y_label)

    data=[]
    color_index = 0
    
    if col_order:
        keys = col_order
    else:
        keys = sorted(list(tracedict.keys()))        
        
    for key in keys:
        traceframe = tracedict[key]
        trace1 = Bar(
            x=traceframe.index.values.tolist(),
            y=traceframe.tolist(),
            name=key,
            marker={
                'color' : aitec_colors[color_index],
            },
            opacity=0.9,
        )
        data.append(trace1)
        color_index += 1
        
    return dict(data=data, layout=layout)


def scatter_chart_jitter(chartframe, chart_title, x_label, y_label, spread):
    
    chartframe[x_label]=chartframe[x_label] + np.random.uniform(low=0.0, high=spread, size=len(chartframe))
    #chartframe[y_label]=chartframe[y_label] + np.random.uniform(low=0.0, high=spread, size=len(chartframe))

    trace0 = Scatter(
        x=chartframe[x_label].tolist(),
        y=chartframe[y_label].tolist(),
        mode='markers',
        marker = {
            'size' : 3,
        },
        opacity=0.7,    
    )
    
    data = [trace0]
    layout = aitec_bar_layout(chart_title, x_label, y_label)

    return dict(data=data, layout=layout)

def aitec_histogram(val_list, chart_title, x_label, y_label):

    layout = aitec_bar_layout(chart_title, x_label, y_label)

    data = [Histogram(
        x = val_list,
        marker=dict(color=aitec_colors),
        opacity=0.9,
        )
    ]
    
    return dict(data=data, layout=layout)

def aitec_boxplot(chartframe, title, x_label, y_label, col_order=None):

    colnames = chartframe.columns
   
    layout = aitec_bar_layout(title, x_label, y_label)

    data = []
    color_index = 0
    for key in colnames:
        trace = Box(
            y = chartframe[key].tolist(),
            name = key,
            marker = {
                'color' : aitec_colors[color_index],
            },            
            opacity=0.9,
        )
        data.append(trace)
        color_index += 1

    return dict(data=data, layout=layout)
        
def aitec_bar_layout(title, x_label, y_label, **kwargs):

    kwargs.setdefault('x_label_size', 12)
    kwargs.setdefault('bottom_margin', 100)
    #print kwargs['x_label_size']
    layout = Layout(
        title="%s" % title,
        titlefont=dict(
            family='Times New Roman, Times, serif',
            size=24,
            color='#000000',
        ),
        showlegend=False,
        height=chart_height,
        width=chart_width,
        margin=dict(b=kwargs['bottom_margin']),
        xaxis=dict(
            title=x_label,
            titlefont=dict(
                family='Arial, Helvetica, sans serif',
                color='#7f7f7f'
            ),
        tickangle=45,
            tickfont=dict(
                family='Arial, Helvetica, sans serif',
                size=kwargs['x_label_size'],
                color='#7f7f7f'
            )
    ),
    yaxis=dict(
        title=y_label,
        titlefont=dict(
            family='Arial, Helvetica, sans serif',
            size=18,
            color='#7f7f7f'
        ),
        )    
    )
    return layout

# adds barmode="stack", legend
def aitec_barstack_layout(title, x_label, y_label):
    layout = aitec_bar_layout(title, x_label, y_label)
    layout["barmode"] ='stack'
    layout["showlegend"] = True
    return layout

# adds barmode="group", legend
def aitec_bargroup_layout(title, x_label, y_label):
    layout = aitec_bar_layout(title, x_label, y_label)
    layout["barmode"] ='group'
    layout["showlegend"] = True
    return layout

