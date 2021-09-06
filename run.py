import cv2 #подключение библиотеки "cv2"

from config import CASCADES # импорт каскадов


def is_user_wants_quit(): # функция для выхода
    return cv2.waitKey(1) & 0xFF == ord('q') #проверка нажатия клавиши "q"


def show_frame(frame): # показать кадр
    cv2.imshow('Video', frame)


def draw_sqare(frame, color): # нарисовать рамку по координатам
        cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)


def get_cascades(): # генератор списка каскадов
    cascades = [
        (cv2.CascadeClassifier(cascade['path']), cascade['color'])
        for title, cascade in CASCADES.items()
        if cascade['draw']
    ]
    return cascades


if __name__ == "__main__":
    cascades = get_cascades() #запись каскадов в переменную
    video_capture = cv2.VideoCapture(0) #захват изображения
    while True: # выполнять цикл пока возможен захват изображения и пользователь не нажал кнопку для выхода
        if not video_capture.isOpened(): # проверка возможности захвата изображения
            print("Couldn't find your webcam... Sorry :c")
        _, webcam_frame = video_capture.read() # запись кадра в переменную
        gray_frame = cv2.cvtColor(webcam_frame, cv2.COLOR_BGR2GRAY) # преобразование кадра в Ч/Б
        for cascade, color in cascades: #поиск совпадений между каскадами и кадром с камеры с помощью вложенных циклов
            captures = [cascade.detectMultiScale(
                gray_frame,
                scaleFactor=1.1,
                minNeighbors=10,
                minSize=(30, 30)
            )]
            for capture in captures:
                for (x, y, w, h) in capture:
                    draw_sqare(webcam_frame, color) #на каждом анализируемом объекте рисуется рамка
        show_frame(webcam_frame) #отображение текущего кадра

        if is_user_wants_quit(): #проверка нажатия кнопки пользователем для выхода
            break
    video_capture.release() #вывод на экран
    cv2.destroyAllWindows() #закрыть окна
