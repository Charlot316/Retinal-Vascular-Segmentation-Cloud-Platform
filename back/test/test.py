import os
import sys
import warnings
import cv2
from PIL import Image
from skimage.measure import regionprops

import numpy as np
from skimage.io import imsave
from skimage.util import img_as_ubyte
from skimage.transform import resize
import torch
from models.get_model import get_arch
from utils.model_saving_loading import load_model
from utils import paired_transforms_tv04 as p_tr


def test():
    image_path = './media/test/' + sys.argv[1]
    roi_path = './test/test_mask.gif'

    if hasattr(torch.cuda, 'empty_cache'):
        torch.cuda.empty_cache()

    img = cv2.imread(image_path)
    cv2.imwrite('./media/test/' + os.path.splitext(sys.argv[1])[0] + '_origin.png', img, )  # 保存为png
    img = cv2.resize(img, (568, 584))
    os.remove(image_path)


    img = np.array(img, np.float32).transpose(2, 0, 1) / 255.0
    roi = np.array(Image.open(roi_path))
    roi = cv2.resize(roi, (568, 584))
    roi[roi >= 0.5] = 1
    roi[roi <= 0.5] = 0

    img1 = torch.Tensor(img)
    img1 = img1.unsqueeze(0)
    img1 = img1.cuda()

    if hasattr(torch.cuda, 'empty_cache'):
        torch.cuda.empty_cache()

    pred = model(img1)
    pred = (pred.squeeze(0)).squeeze(0)
    pred = pred.cpu().detach().numpy()
    pred = pred * roi
    # bytemap = pred

    pred = Image.fromarray(np.uint8(pred * 255))
    pred.convert('L').save('./media/test/' + os.path.splitext(sys.argv[1])[0] + '_promap.png')

    # bytemap[bytemap >= 0.5] = 1
    # bytemap[bytemap < 0.5] = 0
    #
    # # bytemap = cv2.resize(bytemap,(565,584))
    #
    # bytefig = Image.fromarray(np.uint8(bytemap * 255))
    # bytefig.convert('L').save('./media/test/' + os.path.splitext(sys.argv[1])[0] + '_bytemap.png')


if __name__ == '__main__':
    test()
