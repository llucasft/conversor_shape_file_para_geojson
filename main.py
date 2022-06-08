import shapefile
import json
import argparse
import zipfile
import os
import shutil

#Configuração do argparse
parser = argparse.ArgumentParser(description='Conversor de shapefile para Geojson')
parser.add_argument('--source', type=str, help='Caminho do shapefile')
parser.add_argument('--target', type=str, help='GeoJson de saída')
args = parser.parse_args()


#Descompactando o arquivo .zip onde estão os dados que irei usar
zip_file = zipfile.ZipFile('BR_UF_2021.zip', 'r')
zip_file.extractall('temporario')
zip_file.close()
caminho = os.listdir('temporario')


#Uma função para extrair os dados do diretório temporario
def extrair():
    for arq in caminho:
        if arq.endswith('.shp'):
            shp_caminho = os.path.join('temporario', arq)
            shape = shapefile.Reader(shp_caminho)
            break
    return shape


feature_collection = {
  "type": "FeatureCollection",
  "features": [
      {
      "type": "Feature",
      "properties": {},
      "geometry": {
          "type": "Polygon",
          "coordinates" : [
                            ] 
      }
    }]
}


#Extraindo os dados do diretório temporário e armazenando os dados shp na variável shape
shape = extrair()


#Uma função para ler o arquivo geojson
def ler_geojson():
    for feature in shape.shapeRecords():
        data = feature.shape.__geo_interface__
        feature_collection["features"].append(
            {"type":"Feature",
            "properties":{},
            "geometry":data})
    return data


#Passando os dados do arquivo shp para string
data = ler_geojson()


#Uma função para transformar o shapefile em geojson
def shp_para_geojson(data):
    data = json.dumps(feature_collection)
    with open(args.target, mode="w") as arquivo_data:
        arquivo_data.write(data) 


#Transformando as informações string da variável data para um arquivo geojson
shp_para_geojson(data)


shape.close()
shutil.rmtree("temporario")
