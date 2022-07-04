import sys
import time

from rx.subject import Subject
try:
    from PyQt5.QtWidgets import QApplication, QWidget
except ImportError:
    raise ImportError(
        'PyQt5 is needed for this program to run. Make sure to install it.')


class Window(QWidget):

    def __init__(self):
        QWidget.__init__(self)
        self.setWindowTitle("Detecting mouse clicks")
        self.resize(500, 500)

        self.mouseclick = Subject()

    def mousePressEvent(self, event):
        self.mouseclick.on_next(event.button())


def main():
    print("Click anywhere on the window opened to test the program")
    app = QApplication(sys.argv)

    window = Window()
    window.show()

    # Time-out period set up to 500 milliseconds
    period = 0.5
    buf = []

    def on_next(info):
        buf.append(time.time())
        if len(buf) >= 2:
            if buf[1] - buf[0] < period:
                if info == 1:
                    print("Left Double click")
                elif info == 2:
                    print("Right Double click")
                buf.clear()
            elif buf[1] - buf[0] > period:
                if info == 1:
                    print("Left click")
                elif info == 2:
                    print("Right click")
                buf.clear()

    window.mouseclick.subscribe(on_next, on_error=print)

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
