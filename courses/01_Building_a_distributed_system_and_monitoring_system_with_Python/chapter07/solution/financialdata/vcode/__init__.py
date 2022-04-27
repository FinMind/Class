import numpy as np
from financialdata.vcode.model import load_model
from loguru import logger


class VerifyCode:
    def __init__(self):
        self.model = load_model()

    def _change_character(self, pred_prob):
        total_set = []
        for i in range(65, 91):
            total_set.append(chr(i))

        for i in range(10):
            total_set.append(str(i))

        total_set.append("")
        for i in range(len(pred_prob)):
            if pred_prob[i] == max(pred_prob):
                value = total_set[i]
        return value


    def predict(self, image):
        train_set = np.ndarray((1, 60, 200, 3), dtype=np.uint8)
        train_set[0] = image
        result = self.model.predict(train_set)
        resultlist = ""
        for i in range(len(result)):
            resultlist += self._change_character(result[i][0])
        return resultlist


