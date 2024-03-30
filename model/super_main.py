import pandas as pd
import cv2
import face_recognition
import numpy as np
from numpy import dot
from numpy.linalg import norm
from ast import literal_eval
from PIL import Image
import os

# Функция для преобразования строки в массив NumPy
def string_to_array(s):

    if s[7:-2]!= "" and type(s)==str:
        return np.array(literal_eval(s[7:-2]))
    else:
         return np.nan


# Загрузка данных блогеров
data_blog = pd.read_csv("../data/face_enc_blogers.csv", converters={'encodings': string_to_array})
# Загрузка данных актеров сша
data_us = pd.read_csv("../data/us_face_enc.csv", converters={'encodings': string_to_array})
# Загрузка данных актеров ссср
data_sssr = pd.read_csv("../data/face_enc_ussr.csv", converters={'encodings': string_to_array})
# --------------------------------------------------------------------------
# -------------------------------------------------------------------------
# ЧТЕНИЕ ИЗОБРАЖЕНИЯ,ЗДЕСЬ ДОЛЖНО БЫТЬ ЧТО-ТО СВЯЗЯННОЕ С ТГ БОТОМ
image = cv2.imread("../../3_cropped.jpg")
# --------------------------------------------------------------------------
# -------------------------------------------------------------------------
rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
#переменные в которых будем хранить данные о лучшем совпадении
index_max=None#уникальный индекс максимального
cos_val=0#максимальное значение косинусной меры,по которой происходит оценка
prefix=None# указывает на то из какого датафрейма взято наибольшее совпадение
# Определение расположения лиц
box = face_recognition.face_locations(rgb, model='hog')

# Получение кодировок лиц
encoding = face_recognition.face_encodings(rgb)[0]  # предполагается, что изображение содержит одно лицо

# Сравнение кодировок лиц
for i in range(data_blog.shape[0]):

    # Получение кодировки лица текущего блогера
    blogger_encoding = data_blog.iloc[i]["encodings"]
    if np.isnan(blogger_encoding).any():
        continue
    # Проверка, что blogger_encoding является массивом
    # if isinstance(blogger_encoding, np.ndarray) :
        # Вычисление сходства между кодировками
    similarity = dot(encoding, blogger_encoding) / (norm(encoding) * norm(blogger_encoding))
    if similarity > cos_val:
        cos_val=similarity
        index_max=data_blog.iloc[i]["names"]
        prefix="bloger"
for i in range(data_us.shape[0]):

    # Получение кодировки лица текущего блогера
    us_encoding = data_us.iloc[i]["encodings"]
    if np.isnan(us_encoding).any():
        continue
    # Проверка, что us_encoding является массивом
    # if isinstance(us_encoding, np.ndarray) :
        # Вычисление сходства между кодировками
    similarity = dot(encoding, us_encoding) / (norm(encoding) * norm(us_encoding))
    if similarity > cos_val:
        cos_val=similarity
        index_max=data_us.iloc[i]["names"]
        prefix="usa"

for i in range(data_sssr.shape[0]):

    # Получение кодировки лица текущего блогера
    sssr_encoding = data_sssr.iloc[i]["encodings"]
    if np.isnan(sssr_encoding).any():
        continue
    # Проверка, что us_encoding является массивом
    # if isinstance(us_encoding, np.ndarray) :
    # Вычисление сходства между кодировками
    similarity = dot(encoding, sssr_encoding) / (norm(encoding) * norm(sssr_encoding))
    if similarity > cos_val:
        cos_val = similarity
        index_max = data_sssr.iloc[i]["names"]
        prefix = "sssr"

if prefix=="sssr":
    res_data=pd.read_csv("../data/ussr_russia.csv", sep=";")
    image_path = "../data/new_datasets_ussr"
if prefix=="usa":
    res_data=pd.read_csv("../data/usa.csv", sep=";")
    image_path = "../data/new_dataset_american"
else:
    res_data=pd.read_csv("../data/bloggers.csv", sep=";")
    image_path = "../data/new_dataset_blogers"
inform=res_data[res_data["id"]==index_max][["name","link","specialization","films_years","description"]]
print(inform)
# Путь к изображению
image_path+='\\'+str(index_max)
files = os.listdir(image_path)
image_path = os.path.join(image_path,files[0])
image = Image.open(image_path)
image.show()
# Открытие изображения


# Отображение изображения

