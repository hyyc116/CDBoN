#coding:utf-8
from basic_config import *

## from a citation distribution dict {count: #(count)}, to split papers to three levels
def classify_papers(citation_list,distribution_path,paras_path):
    # 所有文章的被引次数
    citation_dis = Counter(citation_list)
    total = np.sum(citation_dis.values())
    xs = []
    ys = []
    _max_y = 0
    _min_y = 1
    for citation_count in sorted(citation_dis.keys()):
        if citation_count==0:
            continue

        xs.append(citation_count)
        y = citation_dis[citation_count]
        ys.append(y/float(total))
        if y>_max_y:
            _max_y = y

        if y<_min_y:
            _min_y = y

    ccdf = []
    for i,x in enumerate(xs):
        ccdf.append(np.sum(ys[i:]))

    logging.info('Optimize ... ')
    start,end = fit_xmin_xmax(xs,ccdf,paras_path)
    # start,end = 0,len(xs)
    logging.info('from {:} to {:} ...'.format(start,end))
    popt,pcov = curve_fit(power_low_func,xs[start:end],ccdf[start:end])
    fig,ax = plt.subplots(figsize=(5,5))
    ax.plot(xs,ccdf,fillstyle='none')
    ax.plot(np.linspace(start, end, 10), power_low_func(np.linspace(start, end, 10), *popt),label='$\\alpha={:.2f}$'.format(popt[0]))
    
    ax.plot([start]*10, np.linspace(_min_y, 1, 10),'--',label='$x_{min}$'+'$={:}$'.format(start))
    ax.plot([end]*10, np.linspace(_min_y, 1, 10),'--',label='$x_{max}$'+'$={:}$'.format(end))

    ax.legend()
    ax.set_title('Citation distribution')
    ax.set_xlabel('$x=$citation count\n(a)')
    ax.set_ylabel('$\#(x)/N$')
    ax.set_xscale('log')
    ax.set_yscale('log')
    plt.tight_layout()
    plt.savefig(distribution_path,dpi=200)
    logging.info('distribution saved to {:}.'.format(distribution_path))


def fit_xmin_xmax(xs,ys,path):

    rxs=[]
    rys=[]
    rzs=[]

    max_y = np.log(np.max(ys))
    min_y = np.log(np.min(ys))
    norm_ys = (np.log(ys)-min_y)/(max_y-min_y)

    mid = len(xs)/2
    x_is = np.arange(1,80,2)
    y_is = np.arange(120,len(xs),5)

    ROWS = len(x_is)
    COLS = len(y_is)

    max_start=0
    max_end =0
    max_z = 0

    ## 第一步 找出最符合数据集的那条线，只是用R2进行
    for i,start in enumerate(x_is):
        for j,end in enumerate(y_is):

            x = xs[start:end]
            y = ys[start:end]

            popt,pcov = curve_fit(power_low_func,x,y)
            fit_y = power_low_func(x, *popt)
            r2 = r2_score(np.log(y),np.log(fit_y))

            # normed_y = (np.log(y)-min_y)/(max_y-min_y)

            # percent = np.sum(normed_y)/float(np.sum(norm_ys))*(1-(float(len(y))/len(ys)))
            # percent = np.sum(normed_y)/float(np.sum(norm_ys))*np.log((len(ys)/float(len(y))))


            # r2 = r2*percent

            rxs.append(x[0])
            rys.append(x[-1])
            rzs.append(r2)

            if r2>max_z:
                max_start = x[0],start
                max_end = x[-1],end
                max_z = r2

    fig=plt.figure(figsize=(14,10))
    ax = Axes3D(fig)
    ax.view_init(60, 210)
    X = np.reshape(rys,(ROWS,COLS))
    Y = np.reshape(rxs,(ROWS,COLS))
    Z = np.reshape(rzs,(ROWS,COLS))
    ax.set_xlabel('$x_{max}$')
    ax.set_ylabel('$x_{min}$')
    ax.set_zlabel('Global $R^2$')
    # ax.set_zscale('log')
    logging.info('max_start: {:}, max_end:{:}.'.format(max_start,max_end))
    ax.set_title('$x_{min}$:'+'{:}'.format(max_start[0])+' - $x_{max}$:'+'{:}'.format(max_end[0])+', $R^2={:.4f}$'.format(max_z))
    surf = ax.plot_surface(X,Y,Z, cmap=CM.coolwarm)
    fig.colorbar(surf, shrink=0.5, aspect=10)
    plt.savefig(path,dpi=200)
    logging.info('paras saved to {:}.'.format(path))

    return max_start[-1],max_end[-1]


def divide_dataset(dataset):
    if dataset == 'MAG':
        data_path =  'data/mag/stats/plot_dict.json'
    elif dataset== 'Aminer':
        data_path = 'data/plot_dict.json'
    else:
        logging.info('no such dataset!')
        return
    logging.info('load dataset {:} ... '.format(dataset))

    citation_list = json.loads(open(data_path).read())['cxs']
    dis_path = 'pdf/paper_levels_{:}_dis.pdf'.format(dataset)
    paras_path = 'pdf/paper_levels_{:}_paras.pdf'.format(dataset)
    classify_papers(citation_list,dis_path,paras_path)

def experiments():
    divide_dataset('Aminer')
    divide_dataset('MAG')

if __name__ == '__main__':
    experiments()













