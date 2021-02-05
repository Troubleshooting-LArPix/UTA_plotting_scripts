#!/usr/bin/env python3
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import matplotlib.colors as colors
import os,sys
import glob
import h5py
from collections import defaultdict
import time
import yaml
from matplotlib import cm

'''
geometrypath='/home/herogers/SingleCube/larpix-geometry/larpixgeometry/layouts/csu_layout-2.4.0.yaml'
datapath='/home/herogers/SingleCube/data/test'
'''
geometrypath = '/Users/jamesdeleon/Documents/larpix/larpix_v3_4_0/layout-2.4.0.yaml'
#datapath = '/Users/jamesdeleon/Documents/larpix/larpix_v3_4_0/UTA_plotting_scripts/data_files/'#datalog_2021_01_28_19_19_41_CST_.h5'
#datapath = '/Volumes/deleon_py/larpix_test_files/pedestal_data/'
datapath = '/Volumes/deleon_py/larpix_test_files/leakage_current_data/'

files = sorted([os.path.basename(path) for path in glob.glob(datapath+'/*.h5')])
data_cache = dict()

def unique_channel_id(d):
    return ((d['io_group'].astype(int)*256 + d['io_channel'].astype(int))*256 \
            + d['chip_id'].astype(int))*64 + d['channel_id'].astype(int)

def unique_channel_id_2_str(unique_id,*args,**kwargs):
    return (unique_id//(256*256*64)).astype(int).astype(str) \
        + '-' + ((unique_id//(256*64))%256).astype(int).astype(str) \
        + '-' + ((unique_id//64)%256).astype(int).astype(str) \
        + '-' + (unique_id%64).astype(int).astype(str)

def unique_chip_id(d):
    return (d['io_group'].astype(int)*256 + d['io_channel'].astype(int))*256 + d['chip_id'].astype(int)

with open(geometrypath) as fi:
    geo = yaml.full_load(fi)
chip_pix = dict([(chip_id, pix) for chip_id,pix in geo['chips']])

def main(filenames=files):
    plt.close('all')
    fig1 = None
    for filename in filenames:
        if not filename in data_cache:
            print('opening',filename,'...')
            f = h5py.File(os.path.join(datapath,filename),'r')
            unixtime = f['packets']['timestamp'][f['packets']['packet_type'] == 4]
            livetime = np.max(unixtime) - np.min(unixtime)
            data_mask = f['packets']['packet_type'] == 0
            data_mask = np.logical_and(f['packets']['valid_parity'], data_mask)
            dataword = f['packets']['dataword'][data_mask]
            if 'configs' in f.keys():
                configs_unique_chip_id = unique_chip_id(f['configs'])
            else:
                configs_unique_chip_id = np.zeros((1,))-1
            unique_id = unique_channel_id(f['packets'][data_mask])
            unique_id_set = np.unique(unique_id)
            d = defaultdict(dict)
            last = time.time()
            for i,id in enumerate(unique_id_set):
                if time.time() > last + 1:
                    #print('{}/{} {}'.format(i+1,len(unique_id_set),unique_channel_id_2_str(id)),end='\r')
                    last = time.time()
                id_mask = unique_id == id
                config_mask = configs_unique_chip_id == id//64
                if np.sum(id_mask) < 3:
                    continue
                masked_dataword = dataword[id_mask]
                if np.any(config_mask):
                    d[id]['trim'] = f['configs']['registers'][config_mask,id%64][-1]
                    d[id]['threshold'] = f['configs']['registers'][config_mask,64][-1]
                    d[id]['threshold_88K_mV'] = d[id]['threshold']*1800/256 + 465 + 2.34 * d[id]['trim']
                    d[id]['threshold_300K_mV'] = d[id]['threshold']*1800/256 + 210 + 1.45 * d[id]['trim']
                d[id]['min'] = np.min(masked_dataword)
                d[id]['mean'] = np.mean(masked_dataword)
                d[id]['med'] = np.median(masked_dataword)
                d[id]['std'] = np.std(masked_dataword)
                d[id]['rate'] = len(masked_dataword) / (livetime + 1e-9)
                #d[id]['rate'] = len(masked_dataword) / 1 #default leakage current runtime is 1 sec
                #test
                #if d[id]['rate'] > 7:
                #    print(unique_channel_id_2_str(id),d[id]['rate'])
                #end_test
                pix = chip_pix[(id//64)%256][id%64] if (id//64)%256 in chip_pix else None
                if pix:
                    d[id]['x'] = geo['pixels'][pix][1]
                    d[id]['y'] = geo['pixels'][pix][2]
                else:
                    d[id]['x'] = 0.
                    d[id]['y'] = 0.
                #if np.std(masked_dataword)>10:
                #if np.mean(masked_dataword)>200:
                    #print('{}-{}-{}\t{}\tmean:{:.02f}\tstd:{:.02f}\trate:{:.02f}\n'.format( (id//(256*256*64)) % 256, ((id//(256*64))%256), ((id//64)%256), (id%64), np.mean(masked_dataword), np.std(masked_dataword), len(masked_dataword) / (livetime+1e-9) ) )
            data_cache[filename] = d
        else:
            print('loading',filename,'from cache')
            d = data_cache[filename]

        fig, axes = plt.subplots(3,1,sharex='col',sharey='col',num='summary 2 {}'.format(filename),figsize=(5,10))
        x = np.array([d[key]['x'] for key in d if 'x' in d[key]])
        y = np.array([d[key]['y'] for key in d if 'y' in d[key]])
        c0 = fig.colorbar(axes[0].scatter(x,y,c=[d[key]['mean'] for key in d if 'mean' in d[key]], 
                                           marker='.', alpha=0.5*2), ax=axes[0])
        c1 = fig.colorbar(axes[1].scatter(x,y,c=[d[key]['std'] for key in d if 'std' in d[key]], 
                                           marker='.', norm=colors.LogNorm(), alpha=0.5*2), ax=axes[1])
        c2 = fig.colorbar(axes[2].scatter(x,y,c=[d[key]['rate'] for key in d if 'rate' in d[key]], 
                                           marker='.', norm=colors.LogNorm(), alpha=0.5*2), ax=axes[2])
        axes[2].set(xlabel='x [mm]')
        axes[0].set(ylabel='y [mm]',title=filename)
        c0.set_label('mean ADC')
        axes[1].set(ylabel='y [mm]')
        c1.set_label('std ADC')
        axes[2].set(ylabel='y [mm]')
        c2.set_label('rate [Hz]')
        ax2 = axes[0].secondary_xaxis('top', functions=(lambda x: x, lambda x: x))

        ax2.set(xlabel='x [mm]')
        plt.tight_layout()
        plt.savefig(datapath + "summary_" + filename + ".png")
        plt.show()

if __name__ == '__main__':
    main(*sys.argv[1:])
