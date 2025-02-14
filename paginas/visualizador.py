import folium
import streamlit as st
# from streamlit_folium import st_folium


mapinha = folium.Map(tiles="Esri WorldImagery", control_scale=True)

# sitios - cinza
# imaterial - roxo
# tombados - verde
# valorados - azul

# base_sitios = "http://portal.iphan.gov.br/geoserver/SICG/ows?service=WFS&version=1.0.0&request=GetFeature&typeName=SICG%3Asitios&maxFeatures=2147483647&outputFormat=application%2Fjson"
# base_imaterial_pol = "https://raw.githubusercontent.com/alexandrecgn/buscador_patrimonio/refs/heads/main/bens/imaterial_pol.geojson"
# base_imaterial_pt = "https://raw.githubusercontent.com/alexandrecgn/buscador_patrimonio/refs/heads/main/bens/imaterial_pt.geojson"
# base_tombados = "https://raw.githubusercontent.com/alexandrecgn/buscador_patrimonio/refs/heads/main/bens/tombados.geojson"
# base_valorados = "https://raw.githubusercontent.com/alexandrecgn/buscador_patrimonio/refs/heads/main/bens/valorados.geojson"

st.title("Buscador do Patrimônio")
st.write("---")


st.write("## Visualizador dos Bens Culturais")


# # Icone e popup dos bens arqueológicos
# icon_sitio = folium.Icon(color="lightgray")

# popup_sitio = folium.GeoJsonPopup(
#     fields=["identificacao_bem"],
#     aliases=["Sítio arqueológico"],
#     )


#  # Icone, popup e tooltip dos bens registrados
# icon_imaterial = folium.Icon(color="purple")

# popup_imaterial = folium.GeoJsonPopup(
#     fields=["titulo"],
#     aliases=["Bem Registrado"],
# )

# tooltip_imaterial = folium.GeoJsonTooltip(
#     fields=["titulo"],
#     aliases=["Bem Registrado"],
# )


# # Icone e popup dos bens tombados
# icon_tombado = folium.Icon(color="green")

# popup_tombado = folium.GeoJsonPopup(
#     fields=["identificacao_bem"],
#     aliases=["Bem Tombado"],
#     )


# # Icone e popup dos bens valorados
# icon_valorado = folium.Icon(color="blue")

# popup_valorado = folium.GeoJsonPopup(
#     fields=["identificacao_bem"],
#     aliases=["Bem Valorado"],
#     )


# # Adicionando os bens arqueológicos ao mapa
# sitios = folium.GeoJson(
#     data=base_sitios,
#     name="Bens Arqueológicos",
#     marker=folium.Marker(icon=icon_sitio),
#     zoom_on_click=True,popup=popup_sitio,
#     show=False,
# )


# # Adicionando os bens registrados ao mapa
# imaterial_pol = folium.GeoJson(
#     data=base_imaterial_pol,
#     name="Bens Registrados (polígonos)",
#     style_function=lambda cor: {"color": "purple"},
#     zoom_on_click=True,
#     tooltip=tooltip_imaterial,
#     show=False,
# )

# imaterial_pt = folium.GeoJson(
#     data=base_imaterial_pt,
#     name="Bens Registrados (pontos)",
#     marker=folium.Marker(icon=icon_imaterial),
#     zoom_on_click=True,
#     popup=popup_imaterial,
#     show=False,
# )


# # Adicionando os bens tombados ao mapa
# tombados = folium.GeoJson(
#     data=base_tombados,
#     name="Bens Tombados",
#     marker=folium.Marker(icon=icon_tombado),
#     zoom_on_click=True,
#     popup=popup_tombado,
#     show=False,
# )


# # Adicionando os bens valorados ao mapa
# valorados = folium.GeoJson(
#     base_valorados,
#     name="Bens Valorados",
#     marker=folium.Marker(icon=icon_valorado),
#     zoom_on_click=True,
#     popup=popup_valorado,
#     show=False,
# )


# sitios.add_to(mapinha)
# imaterial_pol.add_to(mapinha)
# imaterial_pt.add_to(mapinha)
# tombados.add_to(mapinha)
# valorados.add_to(mapinha)

# folium.LayerControl().add_to(mapinha)
# st_folium(mapinha)

st.warning("*O visualizador de bens estará disponível em breve.*", icon="🛠️")