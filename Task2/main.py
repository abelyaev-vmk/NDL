import cv2
import numpy as np
import os
import os.path as osp
from kivy.app import App
from kivy.graphics import Line, Color, Point
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.textinput import TextInput
from segment import GraphCut


class ButtonsWidget(GridLayout):

    def __init__(self, image_widget=None):
        super(ButtonsWidget, self).__init__()

        self.rows = 2
        self.path_input = TextInput(text='coffeecup.jpg')
        self.open_button = Button(text='Open', on_press=self.__open)
        self.save_button = Button(text='Save', on_press=self.__save)
        self.set_rect_button = Button(text='Set new rectangle', on_press=self.__set_rect)
        self.fgd_mask_button = Button(text='Add foreground mask', on_press=self.__set_mask(True))
        self.bgd_mask_button = Button(text='Add background mask', on_press=self.__set_mask(False))
        self.clear_canvas_button = Button(text='Clear objects', on_press=self.__clear_canvas)
        self.segment_button = Button(text='Segment image', on_press=self.__segment)
        self.round_label = Label(text='N rounds')
        self.round_input = TextInput(text='1')

        self.io_grid_layout = GridLayout()
        self.io_grid_layout.rows = 1
        self.io_grid_layout.add_widget(self.open_button)
        self.io_grid_layout.add_widget(self.save_button)

        self.segment_round_grid_layout = GridLayout()
        self.segment_round_grid_layout.rows = 1
        self.segment_round_grid_layout.add_widget(self.round_label)
        self.segment_round_grid_layout.add_widget(self.round_input)

        for w in (self.path_input, self.fgd_mask_button, self.set_rect_button, self.segment_button, self.io_grid_layout,
                  self.bgd_mask_button, self.clear_canvas_button, self.segment_round_grid_layout):
            self.add_widget(w)
        self.children[-1].size_hint = 1.2, 1

        self.__init_params(image_widget)

    def __init_params(self, image_widget):
        assert image_widget is not None, "No input image provided"
        self.image_widget = image_widget
        self.segmented_img = np.zeros((1, 1))
        self.user_rectangle = (0, 0, 1, 1)
        self.user_mask = np.zeros((1, 1))
        self.last_img_path = ''
        self.gc = GraphCut()

    def __open(self, _):
        self.image_widget.source = self.path_input.text
        self.gc = GraphCut()

    def __save(self, _):
        dir_name = osp.dirname(osp.abspath(self.path_input.text))
        im_name = self.path_input.text.split('/')[-1].split('.jpg')[0]
        count = len([0 for path in os.listdir(dir_name) if path[:len(im_name)] == im_name])
        self.last_img_path = "%s_segmented%04d.jpg" % (im_name, count)
        cv2.imwrite(self.last_img_path, self.segmented_img)

    def __clear_canvas(self, _):
        self.image_widget.clear()

    def __set_rect(self, _):
        self.__clear_canvas(_)
        self.image_widget.draw_rectangle = True

    def __set_mask(self, foreground=True):
        def set_mask(_):
            self.image_widget.draw_mask = True
            self.image_widget.foreground_mask = foreground
        return set_mask

    def __to_cv_coordinates(self, x, y, img):
        im_h, im_w = map(float, img.shape[:2])
        wg_w, wg_h = map(float, self.image_widget.size)
        im_prop, wg_prop = im_h / im_w, wg_h / wg_w
        prop = .5 * (wg_prop - im_prop)
        x_wg = max(0, x if prop > 0 else x - (wg_w - wg_h / im_prop) / 2)
        y_wg = max(0, y if prop < 0 else y - (wg_h - wg_w * im_prop) / 2)
        wg_w = wg_w if prop > 0 else wg_h / im_prop
        wg_h = wg_h if prop < 0 else wg_w * im_prop
        return min(x_wg * im_w / wg_w, im_w), min(im_h * (1. - y_wg / wg_h), im_h)

    def __segment(self, _):
        try:
            img = cv2.imread(self.image_widget.source)
            print 'Segmentation starts'
            if self.image_widget.rectangle:
                x1, x2, y1, y2 = map(float, self.image_widget.rectangle)
                x1_cv, y1_cv = self.__to_cv_coordinates(x1, y1, img)
                x2_cv, y2_cv = self.__to_cv_coordinates(x2, y2, img)
                rect = tuple(map(int, (min(x1_cv, x2_cv), min(y1_cv, y2_cv),
                                       max(x1_cv, x2_cv), max(y1_cv, y2_cv))))
                self.segmented_img = self.gc.segment(img, rect, None, int(self.round_input.text))
            elif self.image_widget.mask:
                mask = np.zeros(img.shape[:2], dtype=np.uint8)
                for x, y, fgd in self.image_widget.mask:
                    x_cv, y_cv = map(int, self.__to_cv_coordinates(x, y, img))
                    mask[max(0, y_cv - 3): min(img.shape[0], y_cv + 3),
                         max(0, x_cv - 3): min(img.shape[1], x_cv + 3)] = 1 if fgd else -1
                self.segmented_img = self.gc.segment(img, None, mask, int(self.round_input.text))
            else:
                raise Exception("Need rectangle or mask to work!")
            print "Segmentation done"
            self.__save(_)
            self.image_widget.update(self.last_img_path)
        except Exception as e:
            print "Exception handled in buttonswidget.segment!", e


class ImageWidget(Image):
    def __init__(self):
        super(ImageWidget, self).__init__()
        self.current_touch = None
        self.canvas_objects = []

        self.rectangle = None
        self.draw_rectangle = False

        self.mask = []
        self.foreground_mask = False
        self.draw_mask = False

    def clear(self):
        for line in self.canvas_objects:
            self.canvas.remove(line)
        self.canvas_objects = []
        self.rectangle = None
        self.mask = []

    def on_touch_move(self, touch):
        if not self.collide_point(touch.x, touch.y):
            return
        if self.draw_rectangle:
            self.clear()
            with self.canvas:
                x1, x2, y1, y2 = touch.opos[0], touch.pos[0], touch.opos[1], touch.pos[1]
                self.rectangle = x1, x2, y1, y2
                Color(1, 0, 0)
                self.canvas_objects.append(Line(points=[x1, y1] + [x2, y1] + [x2, y2] + [x1, y2] + [x1, y1], width=2))
        elif self.draw_mask:
            with self.canvas:
                x, y = touch.pos[:2]
                self.mask.append((x, y, int(self.foreground_mask)))
                Color(0, int(self.foreground_mask), int(not self.foreground_mask))
                self.canvas_objects.append(Point(points=((x, y)), pointsize=2))

    def on_touch_up(self, touch):
        if not self.collide_point(touch.x, touch.y):
            return
        self.draw_rectangle = False
        self.draw_mask = False

    def update(self, path=''):
        self.clear()
        self.source = path


class MainWidget(BoxLayout):
    def __init__(self):
        super(MainWidget, self).__init__()
        self.orientation = 'vertical'
        image_widget = ImageWidget()
        buttons_widget = ButtonsWidget(image_widget=image_widget)
        self.add_widget(buttons_widget)
        self.add_widget(image_widget)
        self.children[1].size_hint = 1, .2


class MainGUI(App):
    def build(self):
        return MainWidget()


if __name__ == '__main__':
    MainGUI().run()
