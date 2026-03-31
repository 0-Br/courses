from torchvision import models
import torch
import torch.nn as nn
import torch.nn.functional as F


def model_A(num_classes, pretrained=False):
    model_resnet = models.resnet18(pretrained=pretrained)
    num_features = model_resnet.fc.in_features
    model_resnet.fc = nn.Linear(num_features, num_classes)
    return model_resnet


def model_B(num_classes):

    mymodel = MyConvNeXt_v1(num_classes)
    # mymodel = MyConvNeXt_v2(num_classes)
    # mymodel = MyConvNeXt_v3(num_classes)
    # mymodel = MyDenseNet(num_classes)
    return mymodel


class Dense_block(nn.Module):

    def __init__(self, blocks):
        super(Dense_block, self).__init__()

        self.layers = nn.Sequential(*blocks)

    def forward(self, x):
        for layer in self.layers:
            out = layer(x)
            x = torch.cat([x, out], dim=1)
        return x


class Res_block_v1(nn.Module):
    '''Inspired by ResNet50, Inception-v3'''

    def __init__(self, size, in_channels, out_channels, cardinality, width_ratio=0.25):
        super(Res_block_v1, self).__init__()

        group_width = (int)(in_channels * width_ratio)
        assert group_width % cardinality == 0

        self.conv_in = nn.Sequential(
            nn.Conv2d(in_channels, group_width, kernel_size=1, stride=1, padding=0, bias=False),
        )

        self.conv_core = nn.Sequential(
            nn.LayerNorm(normalized_shape=[group_width, size, size], eps=1e-6),
            nn.Conv2d(group_width, group_width, kernel_size=(1, 3), stride=1, padding=1, groups=cardinality, bias=False),
            nn.Conv2d(group_width, group_width, kernel_size=(3, 1), stride=1, padding=0, groups=cardinality, bias=False),
            nn.GELU(),
        )

        self.conv_out = nn.Sequential(
            nn.Conv2d(group_width, out_channels, kernel_size=1, stride=1, padding=0, bias=False),
        )

        self.highway = nn.Sequential()
        if in_channels != out_channels:
            self.highway = nn.Sequential(
                nn.LayerNorm(normalized_shape=[in_channels, size, size], eps=1e-6),
                nn.Conv2d(in_channels, out_channels, kernel_size=1, stride=1, padding=0, bias=False),
            )

    def forward(self, x):
        out = self.conv_in(x)
        out = self.conv_core(out)
        out = self.conv_out(out)
        return F.gelu(self.highway(x) + out)


class MyDenseNet(nn.Module):
    'Inspired by DenseNet'

    def _make_stage(self, num, size, in_channel, out_channel, growth_width, cardinality):
        dense_width = in_channel + growth_width * num
        return nn.Sequential(
            Dense_block([Res_block_v1(size, in_channel + i * growth_width, growth_width, cardinality) for i in range(num)]),
            nn.LayerNorm([dense_width, size, size], eps=1e-6),
            nn.Conv2d(dense_width, out_channel, kernel_size=1, stride=1, padding=0, bias=False),
        )

    def _down_sample(self, size, channel):
        return nn.Sequential(
            nn.LayerNorm([channel, size, size], eps=1e-6),
            nn.Conv2d(channel, channel, kernel_size=2, stride=2, padding=0, bias=False) # 降采样 x2
        )

    def __init__(self, num_classes, base_width=128, growth_width=64, cardinality=16):
        super(MyDenseNet, self).__init__()

        self.preprocess = nn.Sequential(
            nn.Conv2d(3, base_width, kernel_size=4, stride=4, padding=0), # 降采样 x4
            nn.LayerNorm([base_width, 56, 56], eps=1e-6)
        )

        self.stage_1 = nn.Sequential(self._make_stage(2, 56, base_width * 1, base_width * 1, growth_width * 1, cardinality), self._down_sample(56, base_width * 1))
        self.stage_2 = nn.Sequential(self._make_stage(3, 28, base_width * 1, base_width * 2, growth_width * 2, cardinality * 2), self._down_sample(28, base_width * 2))
        self.stage_3 = nn.Sequential(self._make_stage(6, 14, base_width * 2, base_width * 4, growth_width * 2, cardinality * 2), self._down_sample(14, base_width * 4))
        self.stage_4 = nn.Sequential(self._make_stage(3, 7, base_width * 4, base_width * 8, growth_width * 8, cardinality * 8))

        self.aggregate = nn.Sequential(
            nn.AdaptiveAvgPool2d(1),
            nn.LayerNorm([base_width * 8, 1, 1], eps=1e-6),
        )
        self.fc = nn.Linear(base_width * 8, num_classes)

    def forward(self, x):
        out = self.preprocess(x)
        out = self.stage_1(out)
        out = self.stage_2(out)
        out = self.stage_3(out)
        out = self.stage_4(out)
        out = self.aggregate(out)

        out = out.view(out.size(0), -1)
        out = self.fc(out)
        return out


class Res_block_v2(nn.Module):
    '''Inspired by ConvNeXt'''

    def __init__(self, size, in_channels, out_channels, width_ratio=4.0):
        super(Res_block_v2, self).__init__()

        group_width = (int)(out_channels * width_ratio)
        assert out_channels % in_channels == 0

        self.conv_in = nn.Sequential(
            nn.Conv2d(in_channels, out_channels, kernel_size=7, stride=1, padding=3, groups=in_channels),
            nn.LayerNorm(normalized_shape=[out_channels, size, size], eps=1e-6),
        )

        self.conv_core = nn.Sequential(
            nn.Conv2d(out_channels, group_width, kernel_size=1, stride=1, padding=0),
            nn.GELU(),
        )

        self.conv_out = nn.Sequential(
            nn.Conv2d(group_width, out_channels, kernel_size=1, stride=1, padding=0),
        )

        self.highway = nn.Sequential()
        if in_channels != out_channels:
            self.highway = nn.Conv2d(in_channels, out_channels, kernel_size=1, stride=1, padding=0)

    def forward(self, x):
        out = self.conv_in(x)
        out = self.conv_core(out)
        out = self.conv_out(out)
        return self.highway(x) + out


class MyConvNeXt_v1(nn.Module):
    '''Inspired by ConvNeXt'''

    def _make_stage(self, num, size, in_channel, out_channel):
        layers = []
        layers.append(Res_block_v2(size, in_channel, out_channel))
        for i in range(num - 1):
            layers.append(Res_block_v2(size, out_channel, out_channel))
        return nn.Sequential(*layers)

    def _down_sample(self, size, channel):
        return nn.Sequential(
            nn.LayerNorm([channel, size, size], eps=1e-6),
            nn.Conv2d(channel, channel, kernel_size=2, stride=2, padding=0, bias=False) # 降采样 x2
        )

    def __init__(self, num_classes, base_width=96):
        super(MyConvNeXt_v1, self).__init__()

        self.preprocess = nn.Sequential(
            nn.Conv2d(3, base_width, kernel_size=4, stride=4, padding=0), # 降采样 x4
            nn.LayerNorm([base_width, 56, 56], eps=1e-6)
        )

        self.stage_1 = nn.Sequential(self._make_stage(3, 56, base_width * 1, base_width * 1), self._down_sample(56, base_width * 1))
        self.stage_2 = nn.Sequential(self._make_stage(3, 28, base_width * 1, base_width * 2), self._down_sample(28, base_width * 2))
        self.stage_3 = nn.Sequential(self._make_stage(9, 14, base_width * 2, base_width * 4), self._down_sample(14, base_width * 4))
        self.stage_4 = nn.Sequential(self._make_stage(3, 7, base_width * 4, base_width * 8))

        self.aggregate = nn.Sequential(
            nn.AdaptiveAvgPool2d(1),
            nn.LayerNorm([base_width * 8, 1, 1], eps=1e-6),
        )
        self.fc = nn.Linear(base_width * 8, num_classes)

    def forward(self, x):
        out = self.preprocess(x)
        out = self.stage_1(out)
        out = self.stage_2(out)
        out = self.stage_3(out)
        out = self.stage_4(out)
        out = self.aggregate(out)

        out = out.view(out.size(0), -1)
        out = self.fc(out)
        return out


class Res_block_v3(nn.Module):

    def __init__(self, size, in_channels, out_channels, width_ratio=4.0):
        super(Res_block_v3, self).__init__()

        group_width = (int)(out_channels * width_ratio)
        assert out_channels % in_channels == 0

        self.conv_in = nn.Sequential(
            nn.Conv2d(in_channels, out_channels, kernel_size=5, stride=1, padding=2, groups=in_channels),
            nn.LayerNorm(normalized_shape=[out_channels, size, size], eps=1e-6),
        )

        self.conv_core = nn.Sequential(
            nn.Conv2d(out_channels, group_width, kernel_size=1, stride=1, padding=0),
            nn.GELU(),
        )

        self.conv_out = nn.Sequential(
            nn.Conv2d(group_width, out_channels, kernel_size=1, stride=1, padding=0),
        )

        self.highway = nn.Sequential()
        if in_channels != out_channels:
            self.highway = nn.Conv2d(in_channels, out_channels, kernel_size=1, stride=1, padding=0)

    def forward(self, x):
        out = self.conv_in(x)
        out = self.conv_core(out)
        out = self.conv_out(out)
        return self.highway(x) + out


class MyConvNeXt_v2(nn.Module):

    def _make_stage(self, num, size, in_channel, out_channel):
        layers = []
        layers.append(Res_block_v3(size, in_channel, out_channel))
        for i in range(num - 1):
            layers.append(Res_block_v3(size, out_channel, out_channel))
        return nn.Sequential(*layers)

    def _down_sample(self, size, channel):
        return nn.Sequential(
            nn.LayerNorm([channel, size, size], eps=1e-6),
            nn.Conv2d(channel, channel, kernel_size=2, stride=2, padding=0, bias=False) # 降采样 x2
        )

    def __init__(self, num_classes, base_width=64):
        super(MyConvNeXt_v2, self).__init__()

        self.preprocess = nn.Sequential(
            nn.Conv2d(3, base_width, kernel_size=4, stride=4, padding=0), # 降采样 x4
            nn.LayerNorm([base_width, 56, 56], eps=1e-6)
        )

        self.stage_1 = nn.Sequential(self._make_stage(3, 56, base_width * 1, base_width * 1), self._down_sample(56, base_width * 1))
        self.stage_2 = nn.Sequential(self._make_stage(3, 28, base_width * 1, base_width * 2), self._down_sample(28, base_width * 2))
        self.stage_3 = nn.Sequential(self._make_stage(9, 14, base_width * 2, base_width * 4), self._down_sample(14, base_width * 4))
        self.stage_4 = nn.Sequential(self._make_stage(3, 7, base_width * 4, base_width * 8))

        self.aggregate = nn.Sequential(
            nn.AdaptiveAvgPool2d(1),
            nn.LayerNorm([base_width * 8, 1, 1], eps=1e-6),
        )
        self.fc = nn.Linear(base_width * 8, num_classes)

    def forward(self, x):
        out = self.preprocess(x)
        out = self.stage_1(out)
        out = self.stage_2(out)
        out = self.stage_3(out)
        out = self.stage_4(out)
        out = self.aggregate(out)

        out = out.view(out.size(0), -1)
        out = self.fc(out)
        return out


class MyConvNeXt_v3(nn.Module):

    def _make_stage(self, num, size, in_channel, out_channel):
        layers = []
        layers.append(Res_block_v3(size, in_channel, out_channel))
        for i in range(num - 1):
            layers.append(Res_block_v3(size, out_channel, out_channel))
        return nn.Sequential(*layers)

    def _down_sample(self, size, channel):
        return nn.Sequential(
            nn.LayerNorm([channel, size, size], eps=1e-6),
            nn.Conv2d(channel, channel, kernel_size=2, stride=2, padding=0, bias=False) # 降采样 x2
        )

    def __init__(self, num_classes, base_width=48):
        super(MyConvNeXt_v3, self).__init__()

        self.preprocess = nn.Sequential(
            nn.Conv2d(3, base_width, kernel_size=4, stride=4, padding=0), # 降采样 x4
            nn.LayerNorm([base_width, 56, 56], eps=1e-6)
        )

        self.stage_1 = nn.Sequential(self._make_stage(3, 56, base_width * 1, base_width * 1), self._down_sample(56, base_width * 1))
        self.stage_2 = nn.Sequential(self._make_stage(3, 28, base_width * 1, base_width * 2), self._down_sample(28, base_width * 2))
        self.stage_3 = nn.Sequential(self._make_stage(9, 14, base_width * 2, base_width * 4), self._down_sample(14, base_width * 4))
        self.stage_4 = nn.Sequential(self._make_stage(3, 7, base_width * 4, base_width * 8))

        self.aggregate = nn.Sequential(
            nn.AdaptiveAvgPool2d(1),
            nn.LayerNorm([base_width * 8, 1, 1], eps=1e-6),
        )
        self.fc = nn.Linear(base_width * 8, num_classes)

    def forward(self, x):
        out = self.preprocess(x)
        out = self.stage_1(out)
        out = self.stage_2(out)
        out = self.stage_3(out)
        out = self.stage_4(out)
        out = self.aggregate(out)

        out = out.view(out.size(0), -1)
        out = self.fc(out)
        return out
