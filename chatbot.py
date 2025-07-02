from rdflib import Graph, Namespace
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

# Ontologie
g = Graph()
g.parse("maïs_agadir_geolocal_turtle.ttl", format="ttl")
EX = Namespace("http://example.org/agroOntology#")

# Initialisation du modèle
model = SentenceTransformer('sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2')

# Intentions groupées par catégorie
intent_map = {
    "semis": [
        "connaître la période de semis du maïs à Agadir",
        "quelle est la période idéale pour semer le maïs à Agadir",
        "quand faut-il semer le maïs à Agadir",
        "quelle est la bonne saison pour planter du maïs",
        "quand semer le maïs dans la région d'Agadir",
        "à quel moment commence la saison de semis du maïs",
        "période recommandée pour la culture du maïs",
        "date de plantation du maïs à Agadir"
    ],
    "rendement": [
        "savoir le rendement du maïs local",
        "quel est le rendement moyen du maïs",
        "combien de tonnes par hectare donne le maïs",
        "productivité du maïs dans la région",
        "rendement du maïs par hectare",
        "quelle quantité produit le maïs local"
    ],
    "sol": [
        "connaître le type de sol pour le maïs",
        "quel type de sol est adapté au maïs",
        "le maïs pousse dans quel sol",
        "sol recommandé pour la culture du maïs",
        "de quel sol le maïs a-t-il besoin",
        "sol idéal pour le maïs"
    ],
    "climat": [
        "savoir le climat adapté au maïs",
        "quel climat est bon pour le maïs",
        "conditions climatiques pour cultiver le maïs",
        "quel est le meilleur climat pour le maïs",
        "le maïs a besoin de quel climat",
        "climat idéal pour le maïs"
    ]
}

# Liste plate des intentions et correspondance
flat_intents = []
intent_labels = []
for label, phrases in intent_map.items():
    for phrase in phrases:
        flat_intents.append(phrase)
        intent_labels.append(label)

# Embedding des intentions
intent_embeddings = model.encode(flat_intents)

# SPARQL semis
def get_semis_mais_agadir():
    query = """
    PREFIX : <http://example.org/agroOntology#>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>

    SELECT ?cultureLabel ?regionLabel ?debut ?fin
    WHERE {
      :MaïsLocal a :Maïs ;
                 rdfs:label ?cultureLabel ;
                 :aPourPériodeSemis ?periode ;
                 :cultivéDans ?region .

      ?periode :début ?debut ;
               :fin ?fin .

      ?region rdfs:label ?regionLabel .
    }
    """
    results = g.query(query)
    for row in results:
        return f"🌱 Période de semis du maïs local à {row.regionLabel} : du {row.debut} au {row.fin}"
    return "❌ Aucune information trouvée."

# Chatbot
def chatbot_respond(user_input):
    input_embedding = model.encode([user_input])
    similarities = cosine_similarity(input_embedding, intent_embeddings)[0]
    best_idx = np.argmax(similarities)
    best_intent = flat_intents[best_idx]
    best_label = intent_labels[best_idx]
    score = similarities[best_idx]

    print(f"🧠 Intention détectée : {best_intent} (similarité: {score:.2f})")

    if best_label == "semis":
        return get_semis_mais_agadir()
    elif best_label == "rendement":
        return "🌾 Le rendement moyen du maïs local est de 8.0 tonnes/hectare."
    elif best_label == "sol":
        return "🌍 Le maïs local nécessite un sol argileux et bien drainé."
    elif best_label == "climat":
        return "🌤️ Le climat adapté au maïs est chaud et modérément humide."
    else:
        return "❌ Désolé, je ne comprends pas encore cette question."

# Test
user_input = "Quand semer le maïs à Agadir cette année ?"
print("👤", user_input)
response = chatbot_respond(user_input)
print("🤖", response)
