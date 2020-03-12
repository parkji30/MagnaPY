from matplotlib import pyplot as plt
import numpy as np, sys, os
from astropy import units as u
import math
from scipy.optimize import curve_fit
plt.rcParams.update({'font.size': 14})
from astropy.io import fits


def disect_name(name):
        nums = []
        strs = []
        for s in name.split("_"):
            if s.isdigit():
                nums.append(int(s))
            else:
                strs.append(s)
        #nums = [int(s) for s in name.split("_") if s.isdigit()]
        return nums,strs
    
def get_time(name):
    """Get the UTC time the image was taken extracted from the image name"""
    nums, strs = disect_name(name)
    return nums[0]

def is_fits(name):
    """Checks if the image is a fits image"""
    return ".fits" in name
    
    
def get_times(path):
    """Get all the times of the images in the directory"""
    times = []
    for i in os.listdir(path):
        times.append(get_time(i))
    return times

# implement a function that gets you bias closest in time to that image!
def get_corresponding_bias(name,bias_imgs):
    bias_times = np.vectorize(get_time)(bias_imgs)
    time = get_time(name)
    btime = min(bias_times, key= lambda x:abs(x-time))
    
    for i in bias_imgs:
        if get_time(i) == btime and is_fits(i):
            return i
        
    return "Not Found!"

def indices_array_generic(m,n):
    r0 = np.arange(m) # Or r0,r1 = np.ogrid[:m,:n], out[:,:,0] = r0
    r1 = np.arange(n)
    out = np.empty((m,n,2),dtype=int)
    out[:,:,0] = r0[:,None]
    out[:,:,1] = r1
    return out

def get_distance(x,y):
    cent_x = 4453/2 + 0.5
    cent_y = 6665/2 +0.5
    
    return np.sqrt((x-cent_x)**2+(y-cent_y)**2)

def image_vs_distance(path,name,bin_size,pc=50,bias_path = None):
    """Vectorized optimized version of the previous function"""
    loop_len = int(math.ceil(get_distance(4453-(pc-1),6665-(pc-1))/bin_size))
    loops = []
    
    for i in range(loop_len):
        loops.append([])
        
    def vdist(idx):
        return get_distance(idx[:,:,0],idx[:,:,1])
    
    idx = indices_array_generic(4453,6665)
    dist = vdist(idx)
    
    def process(count,dist):
        index = int(math.ceil(dist/bin_size)) - 1
        loops[index].append(count)
        
    vprocess = np.vectorize(process)
        
    with fits.open(path + name) as flat:
        if bias_path is not None:
            with fits.open(bias_path + get_corresponding_bias(name,bias_path)) as bias:
                sub = flat[0].data - bias[0].data
                vprocess(sub[pc:(4453-pc),pc:(6665-pc)],dist[pc:(4453-pc),pc:(6665-pc)])
        else:
            vprocess(flat[0].data[pc:(4453-pc),pc:(6665-pc)],dist[pc:(4453-pc),pc:(6665-pc)])
    
    means = []
    medians = []
    for i in range(len(loops)):
        means.append(np.mean(loops[i]))
        medians.append(np.median(loops[i]))
    
    return means, medians

def image_vs_distance2(img,pc=50,bin_size=5):
    loop_len = int(math.ceil(get_distance(4453-(pc-1),6665-(pc-1))/bin_size))
    loops = []

    for i in range(loop_len):
        loops.append([])

    def vdist(idx):
        return get_distance(idx[:,:,0],idx[:,:,1])

    idx = indices_array_generic(4453,6665)
    dist = vdist(idx)

    def process(count,dist):
        index = int(math.ceil(dist/bin_size)) - 1
        loops[index].append(count)

    vprocess = np.vectorize(process)

    vprocess(img[pc:(4453-pc),pc:(6665-pc)],dist[pc:(4453-pc),pc:(6665-pc)])

    means = []
    medians = []
    stds = []
    for i in range(len(loops)):
        means.append(np.mean(loops[i]))
        medians.append(np.median(loops[i]))
        stds.append(np.std(loops[i]))

    return means, medians, stds

def get_sorted_bias(name,bias_imgs,num=1):
    res = []
    bias_times = np.vectorize(get_time)(bias_imgs)
    time = get_time(name)
    btime = sorted(bias_times, key= lambda x:abs(x-time))
    
    for n in np.arange(num):
        for i in bias_imgs:
                if get_time(i) == btime[n] and is_fits(i):
                    res.append(i)
    return res



def apply_filters(imgs,filters):
    for f in filters:
        imgs = imgs[f]
    
    return imgs


def master_mean(imgs,filters,path,sbias=False,bimgs=None,bpath=None,mbias=None,imsize=(4453,6665)):
    
    fimgs = apply_filters(imgs,filters)
    sum_arr = np.zeros(imsize)
    
    for img in fimgs:
        with fits.open(path + img) as hdul:
            sum_arr += hdul[0].data
            
        if sbias:
            sbias = get_sorted_bias(img,bimgs,2)
            sum_arr -= (fits.getdata(bpath + sbias[0]) + fits.getdata(bpath + sbias[1]))/2
            
        if mbias is not None:
            sum_arr -= mbias
            
    mean_arr = sum_arr/len(fimgs)
    return mean_arr


def master_estimator(imgs,filters,path,width=10,sbias=False,bimgs=None,bpath=None,mbias=None):
    
    mean_arr = []
    median_arr = []
    fimgs = apply_filters(imgs,filters)

    for i in range(int(math.floor(len(fimgs)/width))):
        ims = []
        for img in fimgs[width*i:width*(i+1)]:
            with fits.open(path + img) as hdul:
                if sbias:
                    sum_arr = np.zeros((4453,6665))
                    sbias = get_sorted_bias(img,bimgs,2)
                    sum_arr += hdul[0].data
                    sum_arr -= (fits.getdata(bpath + sbias[0]) + fits.getdata(bpath + sbias[1]))/2
                    ims.append(sum_arr)
                    del sum_arr
                    
                elif mbias is not None:
                    sum_arr = np.zeros((4453,6665))
                    sum_arr += hdul[0].data
                    sum_arr -= mbias
                    ims.append(sum_arr)
                    del sum_arr
                    
                else:
                    ims.append(hdul[0].data)

        ims = np.array(ims)
        median_arr.append(np.median(ims,axis=0))
        mean_arr.append(np.mean(ims,axis=0))
        del ims

    std_arr = np.std(np.array(mean_arr),axis=0)
    median_arr = np.median(np.array(median_arr),axis=0)

    return median_arr, std_arr


from IPython.display import HTML
import random

def hide_toggle(for_next=False,ttext="Code"):
    this_cell = """$('div.cell.code_cell.rendered.selected')"""
    next_cell = this_cell + '.next()'

    toggle_text = ttext  # text shown on toggle link
    target_cell = this_cell  # target cell to control with toggle
    js_hide_current = ''  # bit of JS to permanently hide code in current cell (only when toggling next cell)

    if for_next:
        target_cell = next_cell
        toggle_text += ' next cell'
        js_hide_current = this_cell + '.find("div.input").hide();'

    js_f_name = 'code_toggle_{}'.format(str(random.randint(1,2**64)))

    html = """
        <script>
            function {f_name}() {{
                {cell_selector}.find('div.input').toggle();
            }}

            {js_hide_current}
        </script>

        <a href="javascript:{f_name}()">{toggle_text}</a>
    """.format(
        f_name=js_f_name,
        cell_selector=target_cell,
        js_hide_current=js_hide_current, 
        toggle_text=toggle_text
    )

    return HTML(html)


def plotimg(img,sig=3,title="",cb=True,report=True):
    mini =np.mean(img)-sig*np.std(img)
    maxi = np.mean(img)+sig*np.std(img)
    plt.figure(figsize=(14,8))
    plt.imshow(img,vmin=mini,vmax=maxi,cmap="viridis")
    if cb:
        plt.colorbar();
    plt.title(title);
    if report:
        print(np.mean(img),np.median(img),np.std(img))
    
def plothist(img,title="",bins=10000,sig=1,nfig=True,label="",report=True):
    m = np.mean(img)
    s = np.std(img)
    hist, edge = np.histogram(img,bins=bins)
    if nfig:
        plt.figure(figsize=(14,8))
    plt.plot(edge[1:],hist,label=label)
    plt.xlim([m-(sig*s),m+(sig*s)]);
    plt.title(title);
    plt.legend();
    temp = sorted(hist, key= lambda x:abs(x-np.max(hist)/2))
    print("Peak =", np.max(hist),"FWHM = ",np.abs(edge[np.where(hist == temp[0])] - edge[np.where(hist == temp[1])])[0] )
    if report:
        print(m,np.median(img),s)
    



