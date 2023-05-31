# -*- coding: utf-8 -*-
# @Time    : 2023年05月31日 17:51
# @Author  : orcakill
# @File    : onmyoji_service.py
# @Description : 服务接口

from abc import ABC, abstractmethod


class OnmyojiService(ABC):
    @abstractmethod
    def area(self):
        pass
