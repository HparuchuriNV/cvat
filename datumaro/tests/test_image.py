from itertools import product
import numpy as np
import os.path as osp

from unittest import TestCase

import datumaro.util.image as image_module
from datumaro.util.test_utils import TestDir


class ImageTest(TestCase):
    def setUp(self):
        self.default_backend = image_module._IMAGE_BACKEND

    def tearDown(self):
        image_module._IMAGE_BACKEND = self.default_backend

    def test_save_and_load_backends(self):
        backends = image_module._IMAGE_BACKENDS
        for save_backend, load_backend, c in product(backends, backends, [1, 3]):
            with TestDir() as test_dir:
                if c == 1:
                    src_image = np.random.randint(0, 255 + 1, (2, 4))
                else:
                    src_image = np.random.randint(0, 255 + 1, (2, 4, c))
                path = osp.join(test_dir, 'img.png') # lossless

                image_module._IMAGE_BACKEND = save_backend
                image_module.save_image(path, src_image)

                image_module._IMAGE_BACKEND = load_backend
                dst_image = image_module.load_image(path)

                self.assertTrue(np.array_equal(src_image, dst_image),
                    'save: %s, load: %s' % (save_backend, load_backend))

    def test_encode_and_decode_backends(self):
        backends = image_module._IMAGE_BACKENDS
        for save_backend, load_backend, c in product(backends, backends, [1, 3]):
            if c == 1:
                src_image = np.random.randint(0, 255 + 1, (2, 4))
            else:
                src_image = np.random.randint(0, 255 + 1, (2, 4, c))

            image_module._IMAGE_BACKEND = save_backend
            buffer = image_module.encode_image(src_image, '.png') # lossless

            image_module._IMAGE_BACKEND = load_backend
            dst_image = image_module.decode_image(buffer)

            self.assertTrue(np.array_equal(src_image, dst_image),
                'save: %s, load: %s' % (save_backend, load_backend))