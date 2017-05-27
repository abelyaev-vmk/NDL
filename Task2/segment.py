import numpy as np
import cv2


class GraphCut:
    def __init__(self):
        self.last_bgd_model = None
        self.last_fgd_model = None
        self.last_mask = None
        self.image = None

    def segment(self, img, rectangle=None, user_mask=None, n_round=1):
        """
        Segment an image with GrabCut
        :param img: BGR image
        :param rectangle: Object's bounding box
        :param user_mask: User's mask
        :param n_round: Number of rounds for grabCut
        :return: BGR image
        """
        if self.image is None:
            self.image = img
        mask = self.last_mask if self.last_mask is not None else np.zeros(self.image.shape[:2], dtype=np.uint8)
        if user_mask is not None:
            mask[user_mask == -1] = 0
            mask[user_mask == 1] = 1
        bgd_model = self.last_bgd_model if self.last_bgd_model is not None else np.zeros((1, 65), dtype=np.float64)
        fgd_model = self.last_fgd_model if self.last_fgd_model is not None else np.zeros((1, 65), dtype=np.float64)
        mode = cv2.GC_INIT_WITH_RECT if rectangle is not None else cv2.GC_INIT_WITH_MASK
        self.last_mask, self.last_bgd_model, self.last_fgd_model = \
            cv2.grabCut(self.image, mask, rectangle, bgd_model, fgd_model, n_round, mode)
        mask = np.where((self.last_mask == 0) | (self.last_mask == 2), 0, 1).astype('uint8')
        out_img = self.image * mask[:, :, np.newaxis]
        return out_img


if __name__ == '__main__':
    img = cv2.imread("coffeecup.jpg")
    gcs = GraphCut()
    cv2.imwrite("segmented.jpg", gcs.segment(img, (100, 500, 1500, 1500), n_round=3))
