import streamlit as st
import requests

QDRANT_URL = "http://qdrant:6333/collections/air_quality/points/scroll"

st.title("Inteligentny Monitoring Jakości Powietrza")

r = requests.post(QDRANT_URL, json={"limit": 100})
pts = r.json().get("result", {}).get("points", [])

st.write("Ostatnie odczyty:")
for p in pts:
    st.write(p["payload"])

st.header("Wyszukaj podobne warunki")
pm25 = st.slider("PM2.5", 0, 100, 20)
pm10 = st.slider("PM10", 0, 100, 20)
co2 = st.slider("CO2", 0, 2000, 400)
temp = st.slider("Temp [°C]", -20, 40, 20)
humidity = st.slider("Wilgotność [%]", 0, 100, 50)

if st.button("Szukaj podobnych"):
    vec = [pm25, pm10, co2, temp, humidity]
    search_url = "http://qdrant:6333/collections/air_quality/points/search"
    resp = requests.post(search_url, json={"vector": vec, "limit": 5})
    res = resp.json()
    st.write(res)
