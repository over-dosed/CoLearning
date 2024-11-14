# skeleton.py
# use mmpose

import time
import cv2
import numpy as np
from mmpose.apis import MMPoseInferencer


def get_skeleton_data(shared_list, lock, max_len=100, fps = 30):
        # 使用模型别名创建推理器
    inferencer = MMPoseInferencer('rtmo-s_8xb32-600e_body7-640x640', device='cpu')
    result_generator = inferencer('webcam', show=True, num_instances = 1, draw_heatmap = True, draw_bbox=True,  return_vis=True)

    interval = 1 / fps

    while True:
        start_time = time.time()

        result = next(result_generator)

        # # 拼接图像，左边是return_vis, 右边是黑色背景
        # vis_image = cv2.cvtColor(result['visualization'][0], cv2.COLOR_RGB2BGR)
        # vis_image = cv2.resize(vis_image, (416, 416))
        # black_image = np.zeros((416, 416, 3), np.uint8)
        # vis_image = cv2.hconcat([vis_image, black_image])
        # cv2.imshow('vis_image', vis_image)
        # cv2.waitKey(1)

        with lock:
            # 假设 result 是你想要存储的数据
            if len(shared_list) >= max_len:
                shared_list.pop(0)  # 移除最旧的数据
            shared_list.append(result)  # 添加新数据
            print("get one skeleton data, now length is ", len(shared_list))

        elapsed_time = time.time() - start_time
        time_to_wait = max(0, interval - elapsed_time)
        time.sleep(time_to_wait)