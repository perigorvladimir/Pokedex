import os
import cv2
import numpy

#parametros globais
raiz_dataSet = './images/images/'

def get_folders(data_base):
  data_folders = []
  for name in os.listdir(data_base):
    if(os.path.isdir(data_base + name)):

      data_folders.append(name)
  #print(data_folders)
  return data_folders

def gamma(im, par):
	invGamma = 1.0 / par[0]
	table = numpy.array([((i / 255.0) ** invGamma) * 255
		for i in numpy.arange(0, 256)]).astype("uint8")
	return cv2.LUT(im, table)

def equalize(im):
  return cv2.equalizeHist(im)

def median(im, par):
  im = cv2.medianBlur(im,par[0])
  return im
pokemons_saturados = []
valor_corte = 50

kernelMedian = numpy.array([[5,10,5],
                           [10,1,10],
                           [5,10,5]])/61

# Coloca pokemons ja saturados na lista
for caminho, subpasta, arquivos in os.walk(raiz_dataSet):
  for arquivo in arquivos:
    #filtro para pixel ser muito afetado por vizinhos (objetivo reduzir brilho de alguma areas)
    imagem_filtrada = cv2.filter2D(cv2.imread(raiz_dataSet + str(arquivo)), -1, kernelMedian)
    #converte para hsv
    pokemon_hsv = cv2.cvtColor(imagem_filtrada, cv2.COLOR_BGR2HSV)
    #satura
    pokemon_hsv[:, :, 1] = numpy.clip(pokemon_hsv[:, :, 1] * 3.5, 0, 255)
    #diminui brilho
    pokemon_hsv[:, :, 2] = numpy.clip(pokemon_hsv[:, :, 2] * 0.8, 0, 255)
    #volta para rgb
    imagem_rgb = cv2.cvtColor(pokemon_hsv, cv2.COLOR_HSV2BGR)
    # Converta a imagem resultante para escala de cinza
    imagem_resultado_gray = cv2.cvtColor(imagem_rgb, cv2.COLOR_BGR2GRAY)
    # equaliza
    imagem_equalizada = cv2.equalizeHist(imagem_resultado_gray)
    #volta para rgb
    imagem_rgb_equalizada = cv2.merge([imagem_rgb[:, :, 0], imagem_rgb[:, :, 1], imagem_equalizada])
    #coloca gama
    imagem_resultado = gamma(imagem_rgb_equalizada, [1])
    pokemons_saturados.append(imagem_resultado)
  
cv2.imshow('primeira imagem saturada', cv2.resize((pokemons_saturados[162]), (500,500)))
cv2.imshow('primeira imagem normal', cv2.resize(cv2.imread(raiz_dataSet + "cacnea.png"), (500,500)))
cv2.imshow('primeira imagem gamma', cv2.resize(gamma(cv2.filter2D(cv2.imread(raiz_dataSet + "arbok.png"), -1, kernelMedian), [0.4]), (500,500)))
cv2.waitKey(0)

