import matplotlib
matplotlib.use('Agg')
from brian import *
from brian.tools.datamanager import *
from numpy.random import choice
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
    '''
    For now, plot some things from random samples.
    '''
    datakeys = data.keys()
    somekeys = choice(datakeys, 8)
    duration = 3*second
    dt = 0.1*ms
    t = arange(0, float(duration), float(dt))
    for sk in somekeys:
        datum = data.get(sk)
        datum = datum.get(datum.keys()[0])
        wExc = datum.get('wExc')
        wInh = datum.get('wInh')
        syncrate = datum.get('syncrate')
        randrate = datum.get('randrate')
        mems = datum.get('mems')
        gExc = datum.get('gExc')
        gInh = datum.get('gInh')
        figure(1)
        clf()
        imgname = 'V%05.2f%05.2f%05.1f%05.1f.png' % (wExc*1e9, wInh*1e9,
                randrate, syncrate)
        suptitle('wE: %5.2f nS, wI: %5.2f nS, fR: %5.1f, fS: %5.1f' % (
            wExc*1e9, wInh*1e9, randrate, syncrate))
        ax1 = subplot(2,1,1)
        title('S=0')
        ax1.plot(t, mems[0], color='black', label='V(t)')
        ax2 = twinx()
        ax2.plot(t, gExc[0], color='blue', linestyle='--', label='gExc')
        #ax2.plot(t, gInh[0], color='red', linestyle='--', label='gInh')
        ax3 = subplot(2,1,2)
        title('S=1')
        ax3.plot(t, mems[-1], color='black', label='V(t)')
        ax4 = twinx()
        ax4.plot(t, gExc[-1], color='blue', linestyle='--', label='gExc')
        #ax4.plot(t, gInh[-1], color='red', linestyle='--', label='gInh')
        ax1.legend(loc='upper left')
        ax2.legend(loc='upper right')
        ax3.legend(loc='upper left')
        ax4.legend(loc='upper right')
        savepath = os.path.join('.', save_location, imgname)
        while os.path.exists(savepath):
            print('%s exists.' % savepath)
            savepath = os.path.join('.',save_location,
                    '%f%s' % (time(), imgname))
        savefig(savepath)
        print('Figure saved to "%s".' % savepath)


