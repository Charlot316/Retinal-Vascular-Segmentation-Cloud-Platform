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

"""
# argument parsing
parser = argparse.ArgumentParser()
required_named = parser.add_argument_group('required arguments')
parser.add_argument('--config_file', type=str, default=None)
# im_size overrides config file
parser.add_argument('--experiment_path', help='experiments/. where checkpoint is', default=None)
parser.add_argument('--im_size', help='delimited list input, could be 600,400', type=str, default='512')
parser.add_argument('--im_name', help='the path of the image', type=str)
parser.add_argument('--device', type=str, default='cpu',
                    help='where to run the training code (e.g. "cpu" or "cuda:0") [default: %(default)s]')
parser.add_argument('--result_path', type=str, default='results', help='path to save predictions (defaults to results')
"""


def flip_ud(tens):
    return torch.flip(tens, dims=[1])


def flip_lr(tens):
    return torch.flip(tens, dims=[2])


def flip_lrud(tens):
    return torch.flip(tens, dims=[1, 2])


def create_pred(model, tens, mask, coords_crop, original_sz, tta='no'):
    act = torch.sigmoid if model.n_classes == 1 else torch.nn.Softmax(dim=0)
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    with torch.no_grad():
        logits = model(tens.unsqueeze(dim=0).to(device))
        logits = logits.squeeze(dim=0)
    pred = act(logits)

    if tta != 'no':
        with torch.no_grad():
            logits_lr = model(tens.flip(-1).unsqueeze(dim=0).to(device))
            logits_lr = logits_lr.squeeze(dim=0).flip(-1)

            logits_ud = model(tens.flip(-2).unsqueeze(dim=0).to(device))
            logits_ud = logits_ud.squeeze(dim=0).flip(-2)

            logits_lrud = model(tens.flip(-1).flip(-2).unsqueeze(dim=0).to(device))
            logits_lrud = logits_lrud.squeeze(dim=0).flip(-1).flip(-2)

        if tta == 'from_logits':
            mean_logits = torch.mean(torch.stack([logits, logits_lr, logits_ud, logits_lrud]), dim=0)
            pred = act(mean_logits)
        elif tta == 'from_preds':
            pred_lr = act(logits_lr)
            pred_ud = act(logits_ud)
            pred_lrud = act(logits_lrud)
            pred = torch.mean(torch.stack([pred, pred_lr, pred_ud, pred_lrud]), dim=0)
        else:
            raise NotImplementedError
    pred = pred.detach().cpu().numpy()[-1]  # this takes last channel in multi-class, ok for 2-class
    # Orders: 0: NN, 1: Bilinear(default), 2: Biquadratic, 3: Bicubic, 4: Biquartic, 5: Biquintic
    pred = resize(pred, output_shape=original_sz, order=3)
    #full_pred = pred
    full_pred = np.zeros_like(mask, dtype=float)
    full_pred[coords_crop[0]:coords_crop[2], coords_crop[1]:coords_crop[3]] = pred
    #full_pred[~mask.astype(bool)] = 0

    return full_pred


def save_pred(full_pred, im_name):
    im_name = im_name.rsplit('/', 1)[-1]
    # save_name = '/media/test/' + os.path.splitext(sys.argv[1])[0] + '_promap.png'
    save_name = im_name[:-4] + '.png'
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        # this casts preds to int, loses precision but meh
        imsave(save_name, img_as_ubyte(full_pred))


def crop_to_fov(img, mask):
    img_g = np.array(img)
    h,w,c = img_g.shape
    for i in range(0,h):
        summ = np.sum(img_g[i,:,:])
        if summ!=0:
            up_r = i
            break
    for i in range(0,w):
        summ = np.sum(img_g[:,i,:])
        if summ!=0:
            left_r = i
            break
    for i in range(h-1,-1,-1):
        summ = np.sum(img_g[i,:,:])
        if summ!=0:
            down_r = i
            break
    for i in range(w-1,-1,-1):
        summ = np.sum(img_g[:,i,:])
        if summ!=0:
            right_r = i
            break
    new_img = img_g[up_r:down_r,left_r:right_r]
    im_crop = Image.fromarray(new_img)
    return im_crop, [up_r, left_r, down_r, right_r]


if __name__ == '__main__':
    os.environ['CUDA_VISIBLE_DEVICES'] = '2,1,0,3'
    device = torch.device("cuda")
    im_name = "picture.jpg"
    print('* image name parsed: ' + im_name)
    """
    im_name = './media/test/' + sys.argv[1]
    img = cv2.imread(im_name)
    im_name = './media/test/' + os.path.splitext(sys.argv[1])[0] + '_origin.png'
    cv2.imwrite(im_name, img)
    """
    experiment_path = 'experiments/drive'

    config_file = "experiments/drive/config.cfg"

    im_size = (512, 512)
    tg_size = im_size

    model_name = "unet"
    print('* Instantiating model  = ' + model_name)
    model = get_arch(model_name).to(device)
    print('* Loading trained weights...')
    try:
        model, stats = load_model(model, experiment_path, device)
    except RuntimeError:
        sys.exit('---- bad config specification (check layers, n_classes, etc.) ---- ')
    model.eval()
    print('* Start predicting...')
    image = Image.open(im_name)
    mask = np.zeros_like(np.array(image)[:,:,1], dtype=float)
    image, coords_crop = crop_to_fov(image, mask)
    
    # in numpy convention
    original_sz = image.size[1], image.size[0]
    rsz = p_tr.Resize((512, 512))
    tnsr = p_tr.ToTensor()
    tr = p_tr.Compose([rsz, tnsr])
    # only transform image
    image = tr(image)
    mask = np.array(mask).astype(bool)
    full_pred = create_pred(model, image, mask, coords_crop, original_sz)
    print('* Saving predictions...')
    save_pred(full_pred,  im_name)
    print('* Done')