import matplotlib
matplotlib.use('Agg')
from brian import *
from brian.tools.datamanager import *
import os
import sys
from time import time

save_location = 'figures'

if __name__ == '__main__':
    data_dir = sys.argv[1]
    if data_dir.endswith('.data'):
        data_dir = data_dir.replace('.data', '')
    elif data_dir.endswith('.data/'):
        data_dir = data_dir.replace('.data/', '')
    data = DataManager(data_dir)
    print('Reading data from %s' % (data_dir))
    save_location = os.path.join(save_location, data_dir)
    if not os.path.exists(save_location):
        try:
            os.mkdir(save_location)
        except OSError:
            print('Error creating directory.'
                    ' Perhaps a file exists with the same name.')
            raise
    #numrecs = data.itemcount()
    #print("Total number of records: %i" % (numrecs))
    for d in data.itervalues():
        hg = d.get('slopehist')
        S = d.get('S')
        bins = d.get('bins')
        wExc = d.get('wExc')
        wInh = d.get('wInh')
        randrate = d.get('randrate')
        syncrate = d.get('syncrate')
        outrates = d.get('outrates')
        mslope = array([average(bins[:-1], weights=hgrow) if any(hgrow) else 0\
                for hgrow in hg])
        clf()
        subplot2grid((9,1), (0,0), rowspan=5)
        imshow(transpose(hg), extent=(S[0], S[-1], bins[0], bins[-2]),
                aspect='auto', origin='lower',
                cmap='gray_r', interpolation='none')
        plot(S, mslope, color='red', linestyle='--')
        axis(ymin=min(bins), ymax=max(bins)) # ignore zeros in mean
        xlabel('S')
        ylabel('V(t-w), volt')
        colorbar(orientation='horizontal')
        subplot2grid((9,1), (6,0), rowspan=3)
        plot(S, outrates)
        xlabel('S')
        ylabel('outrate, Hz')
        suptitle('wE: %5.2f nS, wI: %5.2f nS, fR: %5.1f, fS: %5.1f' % (
            wExc*1e9, wInh*1e9, randrate, syncrate))
        imgname = '%05.2f%05.2f%05.1f%05.1f.png' % (wExc*1e9, wInh*1e9,
                randrate, syncrate)
        savepath = os.path.join('.',save_location,imgname)
        while os.path.exists(savepath):
            print('%s exists.' % savepath)
            savepath = os.path.join('.',save_location,
                    '%f%s' % (time(), imgname))
        savefig(savepath)
        print('Figure saved to "%s".' % savepath)



