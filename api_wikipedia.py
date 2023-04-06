import wikipedia
import nltk
import json
from nltk.metrics.distance import jaro_winkler_similarity
import warnings
warnings.filterwarnings("ignore", category=UserWarning, module='wikipedia')

#wikipedia.set_lang("pt")
nltk.download('punkt')

# Find the best match using the Jaro-Winkler similarity algorithm
def find_best_match(input_str, options_list):
    best_match = None
    best_score = 0
    for option in options_list:
        score = jaro_winkler_similarity(input_str.lower(), option.lower())
        if score > best_score:
            best_score = score
            best_match = option
    return best_match


def get_wiki_info(topic):
    results = wikipedia.search(topic)
    # Comente o resto da função e descomente a linha abaixo para testar
    #return json.dumps(results)
#'''
    # Pega o texto do resumo da página da Wikipedia
    #summary = wikipedia.summary(topic, sentences=2)
    best_match = find_best_match(topic, results)
    summary = wikipedia.summary(find_best_match(topic, results), sentences=5)

    # Pega os links relacionados à página da Wikipedia
    related_links = wikipedia.page(topic).links

    # Cria um dicionário com as informações obtidas
    wiki_info = {
        "best_match": best_match,
        "summary": summary,
        "results": results
    }

    # Converte o dicionário para um objeto JSON e retorna
    return json.dumps(wiki_info)
#'''
def main():
    # Pergunta ao usuário o tópico que deseja pesquisar
    topic = input("Qual tópico você deseja pesquisar na Wikipedia? ")

    # Obtém as informações da Wikipedia e imprime como JSON
    try:
        wiki_info = get_wiki_info(topic)
        results = json.loads(wiki_info)
        print(f"O melhor resultado que encontramos foi: {results.get('best_match')}\n")
        print(f"{results.get('summary')}\n")
        print(f"Outros resultados: {results.get('results')}")
    except wikipedia.exceptions.DisambiguationError as e:
        print("The search term 'brazilian' is ambiguous. Please choose one of the following options:")
        for option in e.options:
            print("- " + option)

if __name__ == '__main__':
    main()