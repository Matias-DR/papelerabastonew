from gui import Main
import sys


if __name__ == '__main__':
    try:
        location = (int(sys.argv[-2])-2, int(sys.argv[-1])-30)
    except:
        location = (160, 10)
    Main(location).run()
