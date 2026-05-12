# service/impl_cap/u2_fast_cap.py
import cv2
import numpy as np
import uiautomator2 as u2
from airtest.core.android.cap_methods.base_cap import BaseCap
from src.utils.my_logger import my_logger as logger


class U2FastCap(BaseCap):
    """基于 uiautomator2 的高速截图（自动使用 minicap）"""

    def __init__(self, adb, *args, **kwargs):
        super().__init__(adb=adb)
        self.device = None
        try:
            # 根据 ADB serial 连接设备（支持 USB 和 WiFi 连接）
            self.device = u2.connect(adb.serialno)
        except Exception as e:
            logger.error(f"U2FastCap 连接设备失败: {e}")

    def snapshot(self, ensure_orientation=True, *args, **kwargs):
        """
        重写 snapshot 方法，直接返回 RGB 格式的 numpy 数组
        :param ensure_orientation: 是否确保方向（由调用方决定，这里忽略）
        :return: numpy array (RGB) 或 None
        """
        if self.device is None:
            logger.error("U2FastCap 设备未连接")
            return None

        try:
            # uiautomator2 截图（内部优先使用 minicap，速度很快）
            pil_img = self.device.screenshot()
            if pil_img is None:
                logger.error("U2FastCap 截图返回 None")
                return None

            # 转换为 numpy 数组（RGB 格式）
            img_rgb = np.array(pil_img)
            # 转换为 numpy 数组（BGR 格式）
            img_rgb = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2BGR)
            return img_rgb
        except Exception as e:
            logger.error(f"U2FastCap 截图失败: {e}")
            return None

    # 保留 get_frame_from_stream 以兼容父类调用，但实际 snapshot 已重写
    def get_frame_from_stream(self):
        """兼容旧调用，直接调用 snapshot"""
        return self.snapshot()