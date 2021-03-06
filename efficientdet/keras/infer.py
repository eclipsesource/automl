# Lint as: python3
# Copyright 2020 Google Research. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================
"""A simple example on how to use keras model for inference."""
import os
from PIL import Image
import numpy as np

import inference
import hparams_config
from keras import efficientdet_keras


# Prepare images and checkpoints: please run these commands in shell.
# !mkdir tmp
# !wget https://user-images.githubusercontent.com/11736571/77320690-099af300-6d37-11ea-9d86-24f14dc2d540.png -O tmp/img.png
# !wget https://storage.googleapis.com/cloud-tpu-checkpoints/efficientdet/coco/efficientdet-d0.tar.gz -O tmp/efficientdet-d0.tar.gz
# !tar zxf tmp/efficientdet-d0.tar.gz -C tmp
imgs = [np.array(Image.open('tmp/img.png'))]
nms_score_thresh, nms_max_output_size = 0.4, 100

# Create model.
config = hparams_config.get_efficientdet_config('efficientdet-d0')
config.is_training_bn = False
config.image_size = '1920x1280'
config.nms_configs.score_thresh = nms_score_thresh
config.nms_configs.max_output_size = nms_max_output_size
model = efficientdet_keras.EfficientDetModel(config=config)
model.build((1, 1280, 1920, 3))
model.load_weights('tmp/efficientdet-d0/model')
boxes, scores, classes, valid_len = model(imgs)
model.summary()

# Visualize results.
for i, img in enumerate(imgs):
  img = inference.visualize_image(img,
                                  boxes[i].numpy(),
                                  classes[i].numpy().astype(np.int),
                                  scores[i].numpy(),
                                  min_score_thresh=nms_score_thresh,
                                  max_boxes_to_draw=nms_max_output_size)
  output_image_path = os.path.join('tmp/', str(i) + '.jpg')
  Image.fromarray(img).save(output_image_path)
  print('writing annotated image to %s', output_image_path)
