import unittest
import tempfile
import json
import numpy as np
import pandas as pd

from sklearn import datasets

from iterative_learner_framework import IterativeLearner
from callbacks.early_stopping import EarlyStopping
from callbacks.metric_logger import MetricLogger
from supervised.metric import Metric

class IterativeLearnerTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.X, cls.y = datasets.make_classification(
                                n_samples=200, n_features=5, n_informative=5, n_redundant=0,
                                n_classes = 2, n_clusters_per_class = 1,
                                n_repeated=0, shuffle=False, random_state=0)
        cls.data = {
            'train': {
                'X': cls.X,
                'y': cls.y
            }
        }

        cls.train_params = {
            'preprocessing': {},
            'validation': {
                'validation_type': 'split',
                'train_ratio': 0.5,
                'shuffle': True
            },
            'learner': {
                'learner_type': 'xgb',
                'objective': 'binary:logistic',
                'eval_metric': 'logloss',
                'max_iters': 3,
                'silent': 1,
                'max_depth': 1
            }
        }

    def test_fit_and_predict(self):

        early_stop = EarlyStopping({'metric': {'name': 'logloss'}})
        metric_logger = MetricLogger({'metric_names': ['logloss', 'auc']})
        il = IterativeLearner(self.train_params, callbacks = [early_stop, metric_logger])
        il.train(self.data)

        y_predicted = il.predict(self.X)
        metric = Metric({'name': 'logloss'})
        loss = metric(self.y, y_predicted)
        self.assertTrue(loss < 0.4)

    def test_save_and_load(self):
        il = IterativeLearner(self.train_params, callbacks = [])
        il.train(self.data)

        desc = il.save()
        print(desc)

        il.load(desc)
