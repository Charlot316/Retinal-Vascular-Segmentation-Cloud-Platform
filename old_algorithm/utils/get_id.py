# GREY先输入，RGB后输入

import torch

def get_nonzeroid(image1_tensor,image2_tensor):
    GREY_tensor = image1_tensor.squeeze(0)
    GREY_tensor = GREY_tensor + 1
    nonzeroid = torch.nonzero(GREY_tensor)
    return nonzeroid

def get_nonzeroid1(image1_tensor,image2_tensor):
    GREY_tensor = image1_tensor.squeeze(0)
    nonzeroid = torch.nonzero(GREY_tensor)
    return nonzeroid