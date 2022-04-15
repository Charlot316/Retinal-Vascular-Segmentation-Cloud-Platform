import os
import json
import sys
import os.path as osp
import argparse
import warnings
from tqdm import tqdm
import time
from PIL import Image
from skimage.measure import regionprops

import numpy as np
from skimage.io import imsave
from skimage.util import img_as_ubyte
from skimage.transform import resize
import torch
from utils.model_saving_loading import str2bool
from models.get_model import get_arch
from utils.get_loaders import get_test_dataset
from utils.model_saving_loading import load_model
from sobel import edge_conv2d
from utils import paired_transforms_tv04 as p_tr

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
    full_pred = np.zeros_like(mask, dtype=float)
    full_pred[coords_crop[0]:coords_crop[2], coords_crop[1]:coords_crop[3]] = pred
    full_pred[~mask.astype(bool)] = 0

    return full_pred


def save_pred(full_pred, im_name):
    im_name = im_name.rsplit('/', 1)[-1]
    save_name = im_name[:-4] + '.png'

    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        # this casts preds to int, loses precision but meh
        imsave(save_name, img_as_ubyte(full_pred))


def crop_to_fov(img, mask):
    mask = np.array(mask).astype(int)
    minr, minc, maxr, maxc = regionprops(mask)[0].bbox
    im_crop = Image.fromarray(np.array(img)[minr:maxr, minc:maxc])
    return im_crop, [minr, minc, maxr, maxc]


if __name__ == '__main__':
    '''
    Example:
    python test.py --config_file experiments/drive/config.cfg --im_name 'picture.jpg' --im_size 512 --device cuda:0
    '''

    args = parser.parse_args()
    print('* args parsed...')
    # parse device
    if args.device.startswith("cuda"):
        # In case one has multiple devices, we must first set the one
        # we would like to use so pytorch can find it.
        os.environ['CUDA_VISIBLE_DEVICES'] = args.device.split(":", 1)[1]
        if not torch.cuda.is_available():
            raise RuntimeError("cuda is not currently available!")
        print(f"* Running prediction on device '{args.device}'...")
        device = torch.device("cuda")
    else:
        # cpu
        device = torch.device(args.device)

    # parse image path
    im_name = args.im_name
    print('* image name parsed: ' + im_name)
    # parse experiment path
    # experiment_path = args.experiment_path
    experiment_path = 'experiments/drive'
    if experiment_path is None:
        raise Exception('must specify path to experiment')

    # parse config file if provided
    config_file = args.config_file
    if config_file is not None:
        if not osp.isfile(config_file):
            raise Exception('non-existent config file')
        with open(args.config_file, 'r') as f:
            args.__dict__.update(json.load(f))

    im_size = tuple([int(item) for item in args.im_size.split(',')])
    if isinstance(im_size, tuple) and len(im_size) == 1:
        tg_size = (im_size[0], im_size[0])
    elif isinstance(im_size, tuple) and len(im_size) == 2:
        tg_size = (im_size[0], im_size[1])
    else:
        sys.exit('im_size should be a number or a tuple of two numbers')

    model_name = args.model_name
    print('* Instantiating model  = ' + model_name)
    model = get_arch(model_name).to(device)
    print('* Loading trained weights...')
    try:
        model, stats = load_model(model, experiment_path, device)
    except RuntimeError:
        sys.exit('---- bad config specification (check layers, n_classes, etc.) ---- ')
    model.eval()
    print('* Start predicting...')

    mask = Image.open('test_mask.jpg').convert('L')
    image, coords_crop = crop_to_fov(Image.open(im_name), mask)
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
