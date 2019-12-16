from sklearn import metrics as skm
import re
import os
import pandas as pd
import numpy as np
from IPython.core.interactiveshell import InteractiveShell
InteractiveShell.ast_node_interactivity = "all"


def preprocess(input_file):
    """
    required for cleaning input before passing to NbClust
    """
    df = pd.read_csv(input_file).T
    df.to_csv('sand_input')
    df.columns = df.iloc[0]
    df = df[1:]
    # df.reset_index(drop=True)
    meta = pd.read_table(input_file + '_meta')

    meta = meta.rename(columns={'ID': 'ID', 'Phase': 'Group'})
    meta['ID'] = meta['ID'].apply(lambda x: str(x))
    #
    meta.head()


def retrieve_clusterings_files(input_file_name):
    """
    build list of files successfully output from NbClust
    """
    file = 'CAMDA'  # the input file name
    path = 'partitions/' + file + '/'
    # get all file names in the 'path' directory where clustering output is stored
    files = []
    # r=root, d=directories, f = files
    for r, d, f in os.walk(path):
        for file in f:
            files.append(os.path.join(r, file))


def mi_score(res):
    """
    mutual info score calculation
    """
    res = res.sort_values('ID')
    score = skm.adjusted_mutual_info_score(meta['Group'], res['Group'])
    a = {'score': score, 'nc': len(res.groupby('Group'))}
    return a


def accuracy(res):
    """
    accuracy calculation
    """
    acc = pd.DataFrame(
        columns=['m_id', 'r_id', 'max', 'acc_correct', 'acc_total'])
    gres = res.groupby('Group')
    #group_labels = {}
    for i in gres.groups:
        mx = {'max': -1}
        for j in gmeta.groups:
            m = pd.merge(gres.get_group(i), gmeta.get_group(j),
                         how='inner', on='ID')
            if mx['max'] < len(m):
                mx = {'m_id': j, 'r_id': i, 'max': len(m)}
        mx['acc_correct'] = mx['max']
        mx['acc_total'] = len(gres.get_group(i))
        acc = acc.append(mx, ignore_index=True)
    acc['acc'] = mx['acc_correct'] / mx['acc_total']
    r = {'hi': np.max(acc['acc']), 'lo': np.min(acc['acc']), 'wt_avg': np.average(
        acc['acc'], weights=acc['max']), 'avg': np.average(acc['acc']), 'nc': int(np.max(acc['r_id']))}
    return r


def coverage(res):
    """
    coverage calculation
    """
    cov = pd.DataFrame(columns=['m_id', 'r_id', 'max', 'cov'])
    gres = res.groupby('Group')
    for i in gmeta.groups:
        mx = {'max': 0}
        for j in gres.groups:
            m = pd.merge(gres.get_group(j), gmeta.get_group(i),
                         how='inner', on='ID')
            if mx['max'] < len(m):
                mx = {'m_id': j, 'r_id': i, 'max': len(m)}
            mm = {'m_id': j, 'r_id': i, 'max': len(
                m), 'acc': len(m)/len(gmeta.get_group(i))}
        mx['cov'] = mx['max']/len(gmeta.get_group(i))
        cov = cov.append(mx, ignore_index=True)
    r = {'hi': np.max(cov['cov']), 'lo': np.min(cov['cov']), 'wt_avg': np.average(
        cov['cov'], weights=cov['max']), 'avg': np.average(cov['cov'])}
    return r


def analyze(input_file_name, files):
    """
    analyser
    built for mutual info score output
    to adjust, see output dictionary for object parameters
    and call the appropriate method to generate the object
    """
    # '  '_meta is meta file corresponding to input to clustering
    meta = pd.read_table(input_file_name + '_meta')[['ID', 'Group']]

    out = pd.DataFrame(columns=['Method', 'Distance', 'Index', ])

    gmeta = meta.groupby('Group')
    exp = re.compile(r'[xX\."]', re.IGNORECASE)
    g_key = {}
    g_num = 1
    for group in gmeta.groups:
        meta['Group'].loc[meta['Group'] == group] = g_num
        g_num += 1
    meta = meta.sort_values('ID')

    files = retrieve_clusterings_files(input_file_name)
    for f in files:
        res = pd.read_table(f, sep='\s', names=['ID', 'Group'])[1:]
        res['ID'] = res['ID'].apply(lambda x: re.sub(exp, '', x))
        res['ID'] = res['ID'].astype(int)
        a = mi_score(res)
        o = {'Method': f.split('_')[0].split('/')[2], 'Distance': f.split('_')[1], 'Index': f.split('_')[2].split('.')[0],
             'Mutual Info Score': a['score'], 'Best nc': a['nc']}
        out = out.append(o, ignore_index=True)
    out = out.sort_values('Mutual Info Score', ascending=False)
    out.to_csv('RESULTS.csv')
