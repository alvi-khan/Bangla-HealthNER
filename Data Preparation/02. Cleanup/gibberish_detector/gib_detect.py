import pickle
from gibberish_detector import gib_detect_train

model_data = pickle.load(open('./gibberish_detector/gib_model.pki', 'rb'))

def is_gibberish(string):
    model_mat = model_data['mat']
    threshold = model_data['thresh']
    return gib_detect_train.avg_transition_prob(string, model_mat) < threshold
