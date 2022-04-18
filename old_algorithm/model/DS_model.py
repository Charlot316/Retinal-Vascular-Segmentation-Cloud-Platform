

# -*- coding: utf-8 -*-
"""
Created on Thu Jan  9 23:05:23 2020

@author: zhang
"""

import torch.nn as nn
import torch
from functools import partial
import torch.nn.functional as F
import math
nonlinearity = partial(F.relu, inplace=True)

class conv_block(nn.Module):
    def __init__(self, ch_in, ch_out):
        super(conv_block, self).__init__()
        self.conv1 = nn.Conv2d(ch_in, ch_out, kernel_size=3, padding=1)
        self.bn1 = nn.BatchNorm2d(ch_out)
        self.conv2 = nn.Conv2d(ch_out, ch_out, kernel_size=3, padding=1)
        self.bn2 = nn.BatchNorm2d(ch_out)
        self.relu = nn.ReLU(inplace=True)
        self.conv1x1 = nn.Conv2d(ch_in, ch_out, kernel_size=1)

    def forward(self, x):
        residual = self.conv1x1(x)
        out = self.relu(self.bn1(self.conv1(x)))
        out = self.relu(self.bn2(self.conv2(out)))
        out = residual + out
        out = self.relu(out)
        return out
    

class up_conv(nn.Module):
    def __init__(self, ch_in, ch_out):
        super(up_conv, self).__init__()
        self.up = nn.Sequential(
            nn.Upsample(scale_factor=2),
            nn.Conv2d(ch_in, ch_out, kernel_size=3, stride=1, padding=1, bias=True),
            nn.BatchNorm2d(ch_out),
            nn.ReLU(inplace=True)
        )

    def forward(self, x):
        x = self.up(x)
        return x
    
        
class up_conv8(nn.Module):
    def __init__(self, ch_in, ch_out):
        super(up_conv8, self).__init__()
        self.upsam = nn.Upsample(scale_factor=2)
        self.upconv1 = conv_block(ch_in, 256)
        self.upconv2 = conv_block(256, 128)
        self.upconv3 = conv_block(128, ch_out)

    def forward(self, x):
        x = self.upsam(x)
        x = self.upconv1(x)
        x = self.upsam(x)
        x = self.upconv2(x)
        x = self.upsam(x)
        x = self.upconv3(x)
        return x
    
        
class up_conv4(nn.Module):
    def __init__(self, ch_in, ch_out):
        super(up_conv4, self).__init__()
        self.upsam = nn.Upsample(scale_factor=2)
        self.upconv1 = conv_block(ch_in, 128)
        self.upconv2 = conv_block(128, ch_out)

    def forward(self, x):
        x = self.upsam(x)
        x = self.upconv1(x)
        x = self.upsam(x)
        x = self.upconv2(x)
        return x


class local_attention(nn.Module):
    def __init__(self, channel):
        super(local_attention, self).__init__()
        self.dilate1 = nn.Conv2d(channel, channel, kernel_size=3, dilation=1, padding=1)
        self.dilate2 = nn.Conv2d(channel, channel, kernel_size=3, dilation=3, padding=3)
        self.dilate3 = nn.Conv2d(channel, channel, kernel_size=3, dilation=5, padding=5)
        self.conv1x1 = nn.Conv2d(channel, 1, kernel_size=1, dilation=1, padding=0)
        for m in self.modules():
            if isinstance(m, nn.Conv2d) or isinstance(m, nn.ConvTranspose2d):
                if m.bias is not None:
                    m.bias.data.zero_()
        self.psi = nn.Sequential(
            nn.Conv2d(channel, 1, kernel_size=1,stride=1,padding=0,bias=True),
            nn.BatchNorm2d(1),
            nn.Sigmoid()
        )

        self.relu = nn.ReLU(inplace=True)

    def forward(self, x):
        dilate1_out = nonlinearity(self.dilate1(x))
        dilate2_out = nonlinearity(self.dilate2(self.dilate1(x)))
        dilate3_out = nonlinearity(self.dilate3(self.dilate2(self.dilate1(x))))

        fea1 = x + dilate1_out
        fea2 = x + dilate2_out
        fea3 = x + dilate3_out

        fea1 = self.relu(fea1)
        fea2 = self.relu(fea2)
        fea3 = self.relu(fea3)

        fea = self.psi(fea1)+self.psi(fea2)+self.psi(fea3)
        return x*fea


class global_attention_L1(nn.Module):
    def __init__(self,F_g,F_l,F_int):
        super(global_attention_L1,self).__init__()
        self.W_g = nn.Sequential(
            nn.Conv2d(F_g, F_int, kernel_size=1,stride=1,padding=0,bias=True),
            nn.BatchNorm2d(F_int)
            )
        
        self.W_x = nn.Sequential(
            nn.Conv2d(F_l, F_int, kernel_size=1,stride=1,padding=0,bias=True),
            nn.BatchNorm2d(F_int)
        )

        self.psi = nn.Sequential(
            nn.Conv2d(F_int, 1, kernel_size=1,stride=1,padding=0,bias=True),
            nn.BatchNorm2d(1),
            nn.Sigmoid()
        )
        
        self.relu = nn.ReLU(inplace=True)
        
    def forward(self,g,x):
        # 下采样的gating signal 卷积
        g1 = self.W_g(g)
        # 上采样的 l 卷积
        x1 = self.W_x(x)
        # concat + relu
        psi = self.relu(g1+x1)
        # channel 减为1，并Sigmoid,得到权重矩阵
        psi = self.psi(psi)
        # 返回加权的 x
        return x*psi

class global_attention_L2(nn.Module):
    def __init__(self,F_g,F_l,F_K,F_int):
        super(global_attention_L2,self).__init__()
        self.W_g = nn.Sequential(
            nn.Conv2d(F_g, F_int, kernel_size=1,stride=1,padding=0,bias=True),
            nn.BatchNorm2d(F_int)
            )
        
        self.W_x = nn.Sequential(
            nn.Conv2d(F_l, F_int, kernel_size=1,stride=1,padding=0,bias=True),
            nn.BatchNorm2d(F_int)
        )

        self.W_j = nn.Sequential(
            nn.Conv2d(F_K, F_int, kernel_size=1,stride=1,padding=0,bias=True),
            nn.BatchNorm2d(F_int)
        )

        self.psi = nn.Sequential(
            nn.Conv2d(F_int, 1, kernel_size=1,stride=1,padding=0,bias=True),
            nn.BatchNorm2d(1),
            nn.Sigmoid()
        )
        
        self.relu = nn.ReLU(inplace=True)
        self.upsam = nn.Upsample(scale_factor=2)
        
    def forward(self,g,x,k):
        # 下采样的gating signal 卷积
        g1 = self.W_g(g)
        # 上采样的 l 卷积
        x1 = self.W_x(x)

        m1 = self.W_j(self.upsam(k))
        # concat + relu
        psi = self.relu(g1+x1+m1)
        # channel 减为1，并Sigmoid,得到权重矩阵
        psi = self.psi(psi)
        # 返回加权的 x
        return x*psi


class global_attention_L3(nn.Module):
    def __init__(self,F_g,F_l,F_K,F_M,F_int):
        super(global_attention_L3,self).__init__()
        self.W_g = nn.Sequential(
            nn.Conv2d(F_g, F_int, kernel_size=1,stride=1,padding=0,bias=True),
            nn.BatchNorm2d(F_int)
            )
        
        self.W_x = nn.Sequential(
            nn.Conv2d(F_l, F_int, kernel_size=1,stride=1,padding=0,bias=True),
            nn.BatchNorm2d(F_int)
        )

        self.W_j = nn.Sequential(
            nn.Conv2d(F_K, F_int, kernel_size=1,stride=1,padding=0,bias=True),
            nn.BatchNorm2d(F_int)
        )

        self.W_M = nn.Sequential(
            nn.Conv2d(F_M, F_int, kernel_size=1,stride=1,padding=0,bias=True),
            nn.BatchNorm2d(F_int)
        )

        self.psi = nn.Sequential(
            nn.Conv2d(F_int, 1, kernel_size=1,stride=1,padding=0,bias=True),
            nn.BatchNorm2d(1),
            nn.Sigmoid()
        )
        
        self.relu = nn.ReLU(inplace=True)
        self.upsam = nn.Upsample(scale_factor=2)
        
    def forward(self,g,x,k,l):
        # 下采样的gating signal 卷积
        g1 = self.W_g(g)
        # 上采样的 l 卷积
        x1 = self.W_x(x)

        k = self.upsam(self.upsam(k))
        m1 = self.W_j(k)

        l = self.upsam(l)
        l1 = self.W_M(l)
        # concat + relu
        psi = self.relu(g1+x1+m1+l1)
        # channel 减为1，并Sigmoid,得到权重矩阵
        psi = self.psi(psi)
        # 返回加权的 x
        return x*psi

class shallow_fea_fusion(nn.Module):
    def __init__(self,F_g,F_l,F_int):
        super(shallow_fea_fusion,self).__init__()
        self.W_g = nn.Sequential(
            nn.Conv2d(F_g, F_int, kernel_size=1,stride=1,padding=0,bias=True),
            nn.BatchNorm2d(F_int)
            )
        
        self.W_x = nn.Sequential(
            nn.Conv2d(F_l, F_int, kernel_size=1,stride=1,padding=0,bias=True),
            nn.BatchNorm2d(F_int)
        )

        self.psi = nn.Sequential(
            nn.Conv2d(F_int, 1, kernel_size=1,stride=1,padding=0,bias=True),
            nn.BatchNorm2d(1),
            nn.Sigmoid()
        )
        
        self.relu = nn.ReLU(inplace=True)


        self.upsam = up_conv(ch_in=128, ch_out=64)
        self.shallow_conv = conv_block(ch_in=128, ch_out=64)
        self.conv1x1 = nn.Conv2d(64, 1, kernel_size=1, stride=1, padding=0)
        
    def forward(self,g,x):
        # 下采样的gating signal 卷积
        g = self.upsam(g)
        g1 = self.W_g(g)
        # 上采样的 l 卷积
        x1 = self.W_x(x)
        # concat + relu
        psi = self.relu(g1+x1)
        # channel 减为1，并Sigmoid,得到权重矩阵
        psi = self.psi(psi)
        # 返回加权的 x
        fea1 = x*psi
        fea2 = g*psi
        fea = torch.cat((fea1,fea2),dim=1)
        fea = self.shallow_conv(fea)
        fea = self.conv1x1(fea)
        return fea

class U_Net(nn.Module):
    def __init__(self, img_ch=3, output_ch=1):
        super(U_Net, self).__init__()

        self.Maxpool = nn.MaxPool2d(kernel_size=2, stride=2)

        self.Conv1 = conv_block(ch_in=img_ch, ch_out=64)
        self.Conv2 = conv_block(ch_in=64, ch_out=128)
        self.Conv3 = conv_block(ch_in=128, ch_out=256)
        self.Conv4 = conv_block(ch_in=256, ch_out=512)


        self.Up4 = up_conv(ch_in=512, ch_out=256)
        self.Att4 = global_attention_L1(F_g=256,F_l=256,F_int=256)
        self.l_at4 = local_attention(256)
        self.Up_conv4 = conv_block(ch_in=512, ch_out=256)

        self.Up3 = up_conv(ch_in=256, ch_out=128)
        self.Att3 = global_attention_L2(F_g=128,F_l=128,F_K=256,F_int=128)
        self.l_at3 = local_attention(128)
        self.Up_conv3 = conv_block(ch_in=256, ch_out=128)

        self.Up2 = up_conv(ch_in=128, ch_out=64)
        self.Att2 = global_attention_L3(F_g=64,F_l=64,F_K=256,F_M=128,F_int=64)
        self.l_at2 = local_attention(64)
        self.Up_conv2 = conv_block(ch_in=128, ch_out=64)
       
               
        self.Up8x8 = up_conv8(ch_in=512, ch_out=1)
        self.Up4x4 = up_conv4(ch_in=256, ch_out=1)

        self.fconv = nn.Conv2d(1, 1, kernel_size=1, stride=1, padding=0)

        self.shallow_fusion = shallow_fea_fusion(F_g=64,F_l=64,F_int=64)

    def forward(self, x):
        x1 = self.Conv1(x) 

        x2 = self.Maxpool(x1)
        x2 = self.Conv2(x2)

        x3 = self.Maxpool(x2)
        x3 = self.Conv3(x3)

        x4 = self.Maxpool(x3)
        x4 = self.Conv4(x4)


        d4 = self.Up4(x4)
        gt2 = self.Att4(g=d4,x=x3)
        lt2 = self.l_at4(x3)
        x3 = gt2+lt2
        d4 = torch.cat((x3, d4), dim=1)
        d4 = self.Up_conv4(d4)

        d3 = self.Up3(d4)
        gt3 = self.Att3(g=d3,x=x2,k=d4)
        lt3 = self.l_at3(x2)
        x2 = gt3+lt3
        d3 = torch.cat((x2, d3), dim=1)
        d3 = self.Up_conv3(d3)

        d2 = self.Up2(d3)
        gt4 = self.Att2(g=d2,x=x1,k=d4,l=d3)
        lt4 = self.l_at2(x1)
        x1 = gt4+lt4
        d2 = torch.cat((x1, d2), dim=1)
        d2 = self.Up_conv2(d2)

        m4 = self.Up8x8(x4)
        m3 = self.Up4x4(d4) 
        
        deep_fea = m4+m3

        shallow_fea = self.shallow_fusion(d3,d2)
        out = torch.sigmoid(self.fconv(deep_fea+shallow_fea))

        return out