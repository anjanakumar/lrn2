'''
Created on Sep 4, 2014

@author: Stefan Lattner
'''
import arff
import numpy as np
from __builtin__ import file
from lrn2.util.utils import uniquifier, ensure_ndarray
import logging

LOGGER = logging.getLogger(__name__)

def arff_dump(h_act, labels=None, fn_out="./features.arff",
              relation="RBM Feature Space",
              description="Automatically generated by MIDI RBM Toolbox"):
    """
    Saves features learned by an RBM as a WEKA .arff file.

    Parameters
    ----------
    h_act : array-like
        M x N matrix of hidden unit activations, where M = number of instances
        and N = number of hidden units.
        Each row represents an instance, projected into the feature space
        Each column represents the activity for a hidden unit over all instances
    labels : list, optional
        A list of labels with M entries (an entry per instance)
    fn_out : string, optional
        Filename (full path) where data will be written to
        (default = './features.arff')
    relation: string, optional
        The 'relation' attribute of WEKA, typically describes the type of data
    description: string, optional
        Further description of the data
    """

    LOGGER.info("Saving to WEKA arff file {0}...".format(fn_out))

    LOGGER.debug("Formatting data for WEKA export...".format(fn_out))

    h_act = ensure_ndarray(h_act)

    assert(h_act.shape[0] == len(labels))

    attr = []
    if len(h_act) > 0:
        format_str = "{" + "0:0{0}d".format(len(str(h_act.shape[1]))) + "}"
        attr = [('unit' + format_str.format(i), "REAL") for i in range(h_act.shape[1])]
        if labels is not None:
            attr = attr + [('label', list(map(str, sorted(uniquifier(labels)))))]
            data = [act.tolist() + [label] for act, label in zip(h_act, labels)]
        else:
            data = h_act

    export = {'descripton': description,
              'relation': relation,
              'attributes': attr,
              'data': data}

    f = open(fn_out, 'w')
    LOGGER.debug("Dumping to arff file...".format(fn_out))
    arff.dump(export, f)

if __name__ == '__main__':
    arff_dump([[i for i in range(10)] for j in range(20)])
