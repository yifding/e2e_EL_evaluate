import os
import json
import numpy as np

from cleanlab.pruning import get_noise_indices

input_dir = "/scratch365/yding4/e2e_EL_evaluate/data/has_prob/cleanlab_input"
output_dir = "/scratch365/yding4/e2e_EL_evaluate/data/has_prob/cleanlab_output"
assert input_dir != output_dir
os.makedirs(output_dir, exist_ok=True)
datasets = "['aida_testa','aida_testb','aida_train','ace2004','aquaint','clueweb','msnbc','wikipedia']"
datasets = eval(datasets)

for dataset in datasets:
    input_file = os.path.join(input_dir, dataset + ".json")
    output_file = os.path.join(output_dir, dataset + ".json")

    with open(input_file) as reader:
        dic = json.load(reader)
    entity_set = set()
    num_instance = 0
    index2signature = dict()
    signature2index = dict()
    for index, signature in enumerate(dic):
        anno = dic[signature]
        index2signature[index] = signature
        signature2index[signature] = index

        entity_before_anno = anno["entity_before_anno"]
        entity_set.add(entity_before_anno)
        num_instance += 1

    num_class = len(entity_set)
    entity_list = sorted(entity_set)
    labels = np.ones(num_instance, dtype=np.int32)
    probs = np.zeros((num_instance, num_class), dtype=np.float32)

    for index, signature in enumerate(dic):
        anno = dic[signature]
        entity_before_anno = anno["entity_before_anno"]
        predict_index = entity_list.index(entity_before_anno)
        prob = anno["prob"]
        labels[index] = predict_index
        probs[index][predict_index] = prob

    # apply cleanlab
    ordered_label_errors = get_noise_indices(
        s=labels, # numpy_array_of_noisy_labels,
        psx=probs,  # numpy_array_of_predicted_probabilities,
        sorted_index_method='normalized_margin',  # Orders label errors
    )
    print(dataset, ordered_label_errors)
