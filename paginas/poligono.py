import folium
import streamlit as st
import geopandas as gpd
import pandas as pd
from streamlit_folium import st_folium
from utils import pesquisar, to_dict, refinar_material, refinar_imaterial

mapinha = folium.Map(tiles="Esri WorldImagery", control_scale=True)

# sitios - cinza
# imaterial - roxo
# tombados - verde
# valorados - azul

base_sitios = "http://portal.iphan.gov.br/geoserver/SICG/ows?service=WFS&version=1.0.0&request=GetFeature&typeName=SICG%3Asitios&maxFeatures=2147483647&outputFormat=application%2Fjson"
base_imaterial_pol = "https://raw.githubusercontent.com/alexandrecgn/buscador_patrimonio/refs/heads/main/bens/imaterial_pol.geojson"
base_imaterial_pt = "https://raw.githubusercontent.com/alexandrecgn/buscador_patrimonio/refs/heads/main/bens/imaterial_pt.geojson"
base_tombados = "https://raw.githubusercontent.com/alexandrecgn/buscador_patrimonio/refs/heads/main/bens/tombados.geojson"
base_valorados = "https://raw.githubusercontent.com/alexandrecgn/buscador_patrimonio/refs/heads/main/bens/valorados.geojson"


st.title("Buscador do Patrimônio")

st.write("----")

st.write(
    """
    ## Busca por polígono

    Na seção abaixo, faça o upload de um POLÍGONO georreferenciado para definir a área onde será feita a busca por Bens Culturais acautelados em âmbito federal e, em seguida, clique em **Pesquisar** para exibir os resultados.
    """
)

st.info("Formatos de arquivo suportados: KML (Google Earth), Geopackage, GeoJSON")

with st.form("busca", border=False):
    area = st.file_uploader("Selecionar área", type=["kml", "gpkg", "geojson"])
    enviado = st.form_submit_button("Pesquisar")
    
    if enviado:
        tooltip = folium.Tooltip(text="Área da busca")
        folium.GeoJson(
            gpd.read_file(area),
            name="Polígono de busca",
            style_function=lambda cor: {"color": "red"},
            tooltip=tooltip,
            ).add_to(mapinha)

        with st.status(
            "Pesquisando Bens Culturais na área inserida",
            expanded=True,
            ) as status:
            sitios = pesquisar(area, base_sitios)
            imaterial_pol = pesquisar(area, base_imaterial_pol)
            imaterial_pt = pesquisar(area, base_imaterial_pt)
            tombados = pesquisar(area, base_tombados)
            valorados = pesquisar(area, base_valorados)

            sit_dict = to_dict(sitios)
            imapol_dict = to_dict(imaterial_pol)
            imapt_dict = to_dict(imaterial_pt)
            tom_dict = to_dict(tombados)
            val_dict = to_dict(valorados)

            tab_sit = refinar_material(sit_dict)

            tab_imtpol = refinar_imaterial(imapol_dict)
            tab_imtpt = refinar_imaterial(imapt_dict)
            impol = pd.DataFrame(tab_imtpol)
            impt = pd.DataFrame(tab_imtpt)
            tab_im_tot = pd.concat([impol, impt])
            
            tab_tmb = refinar_material(tom_dict)
            
            tab_val = refinar_material(val_dict)
            
            status.update(label="Pesquisa Concluída", state="complete")

        tab1, tab2, tab3, tab4 = st.tabs([
            "Patrimônio Arqueológico",
            "Patrimônio Imaterial",
            "Patrimônio Tombado",
            "Patrimônio Ferroviário",
            ])

        with tab1:
            st.header("Sítios Arqueológicos Cadastrados")
            
            icon = folium.Icon(color="lightgray")

            popup = folium.GeoJsonPopup(
                fields=["identificacao_bem"],
                aliases=["Sítio arqueológico"],
                )

            if tab_sit.empty:
                st.write("Não foi identificado Patrimônio Arqueológico na área de busca")
            if not tab_sit.empty:
                st.dataframe(tab_sit, use_container_width=True)
                folium.GeoJson(
                    sitios,
                    name="Bens Arqueológicos",
                    marker=folium.Marker(icon=icon),
                    zoom_on_click=True,
                    popup=popup,
                    ).add_to(mapinha)
        
        with tab2:
            st.header("Bens Imateriais Registrados")
            
            icon = folium.Icon(color="purple")

            popup = folium.GeoJsonPopup(
                fields=["titulo"],
                aliases=["Bem Registrado"],
            )

            tooltip = folium.GeoJsonTooltip(
                fields=["titulo"],
                aliases=["Bem Registrado"],
            )

            if tab_imtpol.empty and tab_imtpt.empty:
                st.write("Não foi identificado Patrimônio Imaterial na área de busca")
            elif tab_imtpol.empty and not tab_imtpt.empty:
                st.dataframe(tab_imtpt, use_container_width=True)
                folium.GeoJson(
                    imaterial_pt,
                    name="Bens Registrados (pontos)",
                    marker=folium.Marker(icon=icon),
                    zoom_on_click=True,
                    popup=popup,
                    ).add_to(mapinha)
            elif tab_imtpt.empty and not tab_imtpol.empty:
                st.dataframe(tab_imtpol, use_container_width=True)
                folium.GeoJson(
                    imaterial_pol,
                    name="Bens Registrados (polígonos)",
                    style_function=lambda cor: {"color": "purple"},
                    zoom_on_click=True,
                    tooltip=tooltip,
                    ).add_to(mapinha)
            elif not tab_imtpt.empty and not tab_imtpol.empty:
                st.dataframe(tab_im_tot, use_container_width=True)
                folium.GeoJson(
                    imaterial_pol,
                    name="Bens Registrados (polígonos)",
                    style_function=lambda cor: {"color": "purple"},
                    zoom_on_click=True,
                    tooltip=tooltip,
                    ).add_to(mapinha)
                folium.GeoJson(
                    imaterial_pt,
                    name="Bens Registrados (pontos)",
                    marker=folium.Marker(icon=icon),
                    zoom_on_click=True,
                    popup=popup,
                    ).add_to(mapinha)
        
        with tab3:
            st.header("Bens Materiais Tombados")

            icon = folium.Icon(color="green")

            popup = folium.GeoJsonPopup(
                fields=["identificacao_bem"],
                aliases=["Bem Tombado"],
                )

            if tab_tmb.empty:
                st.write("Não foi identificado Patrimônio Tombado na área de busca")
            if not tab_tmb.empty:
                st.dataframe(tab_tmb, use_container_width=True)
                folium.GeoJson(
                    tombados,
                    name="Bens Tombados",
                    marker=folium.Marker(icon=icon),
                    zoom_on_click=True,
                    popup=popup,
                    ).add_to(mapinha)
        
        with tab4:
            st.header("Bens Materiais Valorados")

            icon = folium.Icon(color="blue")

            popup = folium.GeoJsonPopup(
                fields=["identificacao_bem"],
                aliases=["Bem Valorado"],
                )

            if tab_val.empty:
                st.write("Não foi identificado Patrimônio Ferroviário na área de busca")
            if not tab_val.empty:
                st.dataframe(tab_val, use_container_width=True)
                folium.GeoJson(
                    valorados,
                    name="Bens Valorados",
                    marker=folium.Marker(icon=icon),
                    zoom_on_click=True,
                    popup=popup,
                    ).add_to(mapinha)

        folium.LayerControl().add_to(mapinha)
        st_folium(mapinha)


st.write("----")

st.error("**Disclaimer:** Este projeto não possui nenhum vínculo com o Instituto do Patrimôno Histórico e Artístico Nacional - IPHAN ou qualquer outro órgão/instuição.")