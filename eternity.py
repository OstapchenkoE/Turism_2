import pandas as pd
import osmnx as ox

df_cut = pd.read_csv("data.csv", delimiter=",")

#df=df[['название.объекта','POINT_X','POINT_Y']]

russia_map = ox.load_graphml("piedmont.graphml")
