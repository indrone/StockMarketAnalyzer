import matplotlib.pyplot as plt


def plot_stock(data):
    plt.plot(data)
    plt.show()
colors=["#e8b5b5","#b5e8cf","#e8e8b5","#892a58"]

def formatChartJsLine(data):
    typeOf=[]
    c=0
    for label in data:
        typeOf.append(
            {
                "data":data[label],
                "label":label.upper(),
                "borderColor": colors[c],
                "fill": False,
                "pointRadius": 0,
             }
        )
        c+=1
    return typeOf
