# The annotation format is a dictionary of list
# the key of the dictionary is the doc_name while each element of the list is a dictionary

# anno = {
#   'testa_1001': [
#       {'start': , 'end', 'mention_txt': , 'entity_txt': ,
#        }
#   ]
# }


class ConfusionMatrix(object):
    def __init__(self, TP, TN, FP, FN):
        self.TP = TP
        self.TN = TN
        self.FP = FP
        self.FN = FN

    @property
    def recall(self):
        return self.TP / (self.TP + self.FN)

    @property
    def precision(self):
        return self.TP / (self.TP + self.FP)

    @property
    def F1(self):
        return 2 * self.recall * self.precision / (self.recall + self.precision)


def confusion_matrix_from_xml(doc_name2txt, model_doc_name2anno, GT_doc_name2anno):
    for doc_name in model_doc_name2anno:
        assert doc_name in doc_name2txt

    for doc_name in GT_doc_name2anno:
        assert doc_name in doc_name2txt

    fake_TP = 0
    TP = TN = FP = FN = 0
    for doc_name in model_doc_name2anno:
        for anno in model_doc_name2anno[doc_name]:
            if doc_name in GT_doc_name2anno and anno in GT_doc_name2anno[doc_name]:
                TP += 1
            else:
                FP += 1

    for doc_name in GT_doc_name2anno:
        for anno in GT_doc_name2anno[doc_name]:
            if doc_name in model_doc_name2anno and anno in model_doc_name2anno[doc_name]:
                fake_TP += 1
            else:
                FN += 1

    assert TP == fake_TP

    confusion_matrix = ConfusionMatrix(TP, TN, FP, FN)
    return confusion_matrix
