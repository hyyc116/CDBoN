#coding:utf-8
from basic_config import *

## from a citation distribution dict {count: #(count)}, to split papers to three levels
def classify_papers(citation_list,distribution_path):
    # 所有文章的被引次数
    citation_dis = Counter(citation_list)
    total = np.sum(citation_dis.values())
    xs = []
    ys = []
    _max_y = 0
    _min_y = 1
    for citation_count in sorted(citation_dis):
        if citation_count==0:
            continue

        xs.append(citation_count)
        y = citation_dis[citation_count]/float(total)
        ys.append(y)
        if y>_max_y:
            _max_y = y

        if y<_min_y:
            _min_y = y

    # fig,axes = plt.subplots(4,2,figsize=(14,20))
    fig = plt.figure(figsize=(14,20))
    ## first plot citation distribution
    # ax00 = axes[0,0]
    ax00 = fig.add_subplot(4,2,1)
    logging.info('plot the original distribution...')
    plot_citation_distribution(ax00,xs,ys)
    ## plot the grid search result of using R2 directly
    ax10 = fig.add_subplot(4,2,3)
    ax11 = fig.add_subplot(4,2,4, projection='3d')
    plot_fitting_and_distribution(fig,ax10,ax11,xs,ys,'r2',_min_y,_max_y)

    ## plot the grid search result of using percentage r2
    ax20 = fig.add_subplot(4,2,5)
    ax21 = fig.add_subplot(4,2,6, projection='3d')
    plot_fitting_and_distribution(fig,ax20,ax21,xs,ys,'percentage_r2',_min_y,_max_y)
    
    ## plot the grid search result of using percentage r2
    ax30 = fig.add_subplot(4,2,7)
    ax31 = fig.add_subplot(4,2,8, projection='3d')
    plot_fitting_and_distribution(fig,ax30,ax31,xs,ys,'adjusted_r2',_min_y,_max_y)

    plt.tight_layout()
    plt.savefig(distribution_path,dpi=200)
    logging.info('distribution saved to {:}.'.format(distribution_path))


def plot_fitting_and_distribution(fig,ax1,ax2,xs,ys,evaluator_name,_min_y,_max_y):
    logging.info('Optimize using {:} ... '.format(evaluator_name))
    start,end = fit_xmin_xmax(xs,ys,fig,ax2,evaluator_name)
    logging.info('Search result: X_min =  {:},  X_max = {:} ...'.format(start,end))
    popt,pcov = curve_fit(power_low_func,xs[start:end],ys[start:end])
    plot_citation_distribution(ax1,xs,ys)
    ax1.plot(np.linspace(start, end, 10), power_low_func(np.linspace(start, end, 10), *popt),label='$\\alpha={:.2f}$'.format(popt[0]))
    ax1.plot([start]*10, np.linspace(_min_y, _max_y, 10),'--',label='$x_{min}$'+'$={:}$'.format(start))
    ax1.plot([end]*10, np.linspace(_min_y, _max_y, 10),'--',label='$x_{max}$'+'$={:}$'.format(end))
    ax1.legend()

def plot_citation_distribution(ax,xs,ys):
    ax.plot(xs,ys,'o',fillstyle='none')
    ax.set_title('Citation Distribution')
    ax.set_xlabel('Citation Count')
    ax.set_ylabel('Relative Frequency')
    ax.set_xscale('log')
    ax.set_yscale('log')

def fit_xmin_xmax(xs,ys,fig,ax,evaluator_name='adjusted_r2',end_x=80,start_y=100):

    rxs=[]
    rys=[]
    rzs=[]

    max_y = np.log(np.max(ys))
    min_y = np.log(np.min(ys))
    normed_total_ys = (np.log(ys)-min_y)/(max_y-min_y)

    x_is = np.arange(1,end_x,2)
    y_is = np.arange(start_y,len(xs),5)

    ROWS = len(x_is)
    COLS = len(y_is)

    max_start=0
    max_end =0
    max_z = 0

    for i,start in enumerate(x_is):
        for j,end in enumerate(y_is):

            x = xs[start:end]
            y = ys[start:end]

            popt,pcov = curve_fit(power_low_func,x,y)
            fit_y = power_low_func(x, *popt)
            r2 = r2_score(np.log(y),np.log(fit_y))

            normed_y = (np.log(y)-min_y)/(max_y-min_y)
            percent_of_num = np.sum(normed_y)/float(np.sum(normed_total_ys))
            percentage_r2 = r2*percent_of_num
            ## efficiency of description
            percent_of_x = float(len(y))/float(len(ys))
            efficiency = percent_of_num/percent_of_x
            adjusted_r2 = percentage_r2*efficiency

            if evaluator_name=='adjusted_r2':
                evaluator = adjusted_r2
            elif evaluator_name =='percentage_r2':
                evaluator = percentage_r2
            elif evaluator_name == 'r2':
                evaluator = r2

            rxs.append(x[0])
            rys.append(x[-1])
            rzs.append(evaluator)

            if evaluator>max_z:
                max_start = x[0],start
                max_end = x[-1],end
                max_z = evaluator

    # fig=plt.figure(figsize=(14,10))
    # ax = Axes3D(fig)
    ax.view_init(60, 210)
    X = np.reshape(rys,(ROWS,COLS))
    Y = np.reshape(rxs,(ROWS,COLS))
    Z = np.reshape(rzs,(ROWS,COLS))
    ax.set_xlabel('$x_{max}$')
    ax.set_ylabel('$x_{min}$')
    ax.set_zlabel(evaluator_name)
    # ax.set_zscale('log')
    logging.info('max_start: {:}, max_end:{:}.'.format(max_start,max_end))
    ax.set_title('$x_{min}$:'+'{:}'.format(max_start[0])+' - $x_{max}$:'+'{:}'.format(max_end[0])+', {:}={:.4f}'.format(evaluator_name,max_z))
    surf = ax.plot_surface(X,Y,Z, cmap=CM.coolwarm)
    fig.colorbar(surf, shrink=0.5, aspect=10,ax=ax)
    # plt.savefig(path,dpi=200)
    # logging.info('paras saved to {:}.'.format(path))

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
    # paras_path = 'pdf/paper_levels_{:}_paras.pdf'.format(dataset)
    classify_papers(citation_list,dis_path)

def experiments():
    divide_dataset('Aminer')
    divide_dataset('MAG')

if __name__ == '__main__':
    experiments()













