import uuid

class Learner():
    '''
    This is a Learner base class.
    All algorithms inherit from Learner.
    '''
    def __init__(self, params):
        self.params = params
        self.stop_training = False
        self.library_version = None
        self.algorithm_name = 'Unknown'
        self.algorithm_short_name = 'Unknown'
        self.model = None
        self.uid = params.get('uid', str(uuid.uuid4()))

    def fit(self, X, y):
        pass
    def predict(self, X):
        pass
    def update(self, update_params):
        pass
    def copy(self):
        pass
    def save(self):
        pass
    def load(self, model_path):
        pass
    #def importance(self, column_names, normalize = True):
    #    pass
