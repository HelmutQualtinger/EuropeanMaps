import pycountry
import plotly.express as px

print("Länder und ISO 3166-1 Alpha-3 Codes, die typischerweise von Plotly Express (px.choropleth) erkannt werden:")
print("----------------------------------------------------------------------------------------------------")
print("Hinweis: Plotly verwendet für 'locationmode=\"ISO-3\"' diese Standard-Codes.")
print("         Die Erkennung von 'locationmode=\"country names\"' basiert auf englischen Namen,")
print("         kann aber weniger zuverlässig sein als die Verwendung von ISO-3 Codes.")
print("         Diese Liste wird mit der Bibliothek 'pycountry' generiert, die den ISO-Standard abbildet.")
print("----------------------------------------------------------------------------------------------------")

count = 0
# Iteriere durch alle Länder in der pycountry-Datenbank
for country in pycountry.countries:
    # pycountry stellt sicher, dass wir standardisierte Codes und Namen haben.
    # Plotly orientiert sich stark an diesen Standards.
    try:
        iso_code = country.alpha_3
        name = country.name
        print(f"Code: {iso_code} - Name: {name}")
        count += 1
    except AttributeError:
        # Einige Einträge in pycountry haben möglicherweise keinen alpha_3 Code (sehr selten für Länder)
        # oder keinen Standardnamen, obwohl das unwahrscheinlich ist.
        try:
            print(f"Code: ??? - Name: {country.name} (Konnte keinen ISO Alpha-3 Code finden)")
        except AttributeError:
             print("Konnte einen Eintrag nicht verarbeiten.")

print("----------------------------------------------------------------------------------------------------")
print(f"Insgesamt {count} Länder/Territorien mit ISO Alpha-3 Codes gefunden.")
print("\nEmpfehlung für px.choropleth:")
print("Verwenden Sie die 'Code' Spalte (ISO Alpha-3) für den 'locations' Parameter")
print("und setzen Sie 'locationmode=\"ISO-3\"'.")
print("\nBeispiel:")
print("import plotly.express as px")
print("fig = px.choropleth(data_frame=my_dataframe,")
print("                    locations='iso_alpha_column',  # Spalte mit z.B. 'DEU', 'USA', 'BRA'")
print("                    locationmode='ISO-3',")
print("                    color='value_column',")
print("                    hover_name='country_name_column',")
print("                    color_continuous_scale=px.colors.sequential.Plasma,")
print("                    title='Meine Choropleth Karte')")
print("fig.show()")

# Optional: Prüfen, ob pycountry installiert ist
try:
    import pycountry
except ImportError:
    print("\n\nFEHLER: Die Bibliothek 'pycountry' wurde nicht gefunden.")
    print("Bitte installieren Sie sie mit: pip install pycountry")
    print("Führen Sie das Skript danach erneut aus.")