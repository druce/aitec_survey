from aitec_plotly import *

# convenience functions for common chart scenarios
def onecolumn_barchart(chartdata, question_col, 
                       x_label="",
                       y_label="",
                       title=None,
                       show_no_answer=True,
                       col_order=None
                       ):
    """Single choice, no other"""
    if title is None:
        title = chartdata.columns[question_col]

    if show_no_answer:
        question_name = chartdata.columns[question_col]        
        #print(question_name)
        chartdata.loc[pd.isnull(chartdata[question_name]),
                      question_name] = "No Answer"
        
    return aitec_bar(chartdata, question_col, title, x_label, y_label, col_order=col_order)


def twocolumn_barchart(chartdata, question_col, 
                       otherval="Other (please specify)",
                       x_label="",
                       y_label="",
                       title=None,
                       show_no_answer = True,
                       **kwargs # additional args passed to layout
                       ):
    """Single choice plus other"""
    question_name = chartdata.columns[question_col]
    other_name = chartdata.columns[question_col+1] # Other (please specify)
    # copy 'other' value
    chartdata.loc[chartdata[question_name] == otherval, question_name] = chartdata.loc[chartdata[question_name] == otherval, other_name]

    if show_no_answer:
        chartdata.loc[pd.isnull(chartdata[question_name]),
                      question_name] = "No Answer"
    
    # TODO: arg to merge n smallest others into 'other'
    if title is None:
        #default title
        title = question_name

    return aitec_bar(chartdata, question_col, title, x_label, y_label, **kwargs)

def multicolumn_barchart(chartdata, startcol, ncols,
                         x_label="",
                         y_label="",
                         othertext=True,
                         title=None,
                         show_no_answer=True,
                         **kwargs # additional args passed to layout
                         ):
    """Multiple choices spread out over multiple columns"""
    question_cols = range(startcol,startcol+ncols)

    if othertext:
        # remove catchall 'other', include text freefrom
        question_cols.remove(question_cols[len(question_cols)-2])

    if title is None:
        #default title
        title = chartdata.columns[question_cols][0]
        title = title[:title.find(" - ")]

    return aitec_bar_multi(chartdata, question_cols, title, x_label, y_label, show_no_answer=show_no_answer, **kwargs)

def default_boxplot(chartdata, 
                    startcol, 
                    ncols,
                    x_label="",
                    y_label="",
                    title=None
                    ):

    question_cols = range(startcol, startcol + ncols)
    colnames = chartdata.columns[question_cols]
    chartframe = chartdata[colnames]

    question_name = colnames[0]
    question_name = question_name[:question_name.find(" - ")]

    colnames = [mystr[len(question_name)+3:] for mystr in colnames]
    chartframe.columns = colnames

    if title is None:
        title = question_name
    
    return aitec_boxplot(chartframe, title, x_label, y_label)




