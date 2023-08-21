import argparse
import os
import openai
import time
import concurrent.futures
from tqdm import tqdm

openai.api_key = os.environ["OPENAI_API_KEY"]
COMPLETIONS_MODEL = "gpt-4"

def translatefr2eng(query: str):
    retries = 0
    max_retries = 3
    retry_timeout = 30
    promptfr = """If you are given text that is entirely or partially written in French, you provide a translation into English of the text. When translating, you never give additional commentary or explanations; you only give the literal translation of the text and nothing else. Your responses never contain the text "Translation:"."""
    while retries < max_retries:
        try:
            response = openai.ChatCompletion.create(
                model = COMPLETIONS_MODEL,
                messages=[
                    {"role": "system", "content": promptfr},
                    {"role": "user", "content": f"Translate the following French text into English: '{query}'"}],
                temperature=.3,
            )
            return response["choices"][0]["message"]["content"].strip(" \n")

        except openai.error.RateLimitError as e:
            print("Rate limited. Retrying in 30 seconds.")
            retries += 1
            if retries < max_retries:
                time.sleep(retry_timeout)
        except openai.error.OpenAIError as e:
            print(f"Error: {e}")
            retries += 1
            if retries < max_retries:
                time.sleep(retry_timeout)


def translateeng2fr(query: str):
    retries = 0
    max_retries = 3
    retry_timeout = 30
    prompteng = """If you are given text that is entirely or partially written in English, you provide a translation into French of the text. When translating, you never give additional commentary or explanations; you only give the literal translation of the text and nothing else. Your responses never contain the text "Translation:"."""
    while retries < max_retries:
        try:
            response = openai.ChatCompletion.create(
                model=COMPLETIONS_MODEL,
                messages=[
                    {"role": "system", "content": prompteng},
                    {"role": "user", "content": f"Translate the following English text into French: '{query}'"}],
                temperature=.3,
            )
            return response["choices"][0]["message"]["content"].strip(" \n")

        except openai.error.RateLimitError as e:
            print("Rate limited. Retrying in 30 seconds.")
            retries += 1
            if retries < max_retries:
                time.sleep(retry_timeout)
        except openai.error.OpenAIError as e:
            print(f"Error: {e}")
            retries += 1
            if retries < max_retries:
                time.sleep(retry_timeout)

def translate_file(input_file_path: str, translation_function):
    with open(input_file_path, 'r') as file:
        file_name = input_file_path.split('/')[-1].split('.')[0]
        file_trans = "/path/to/your/output/directory/" + file_name + "_tr.txt"
        queries = file.read().split('\n')

    with open(file_trans, 'w') as file, \
            concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor, \
            tqdm(total=len(queries)) as progress:
        future_to_query = {executor.submit(translation_function, query): query for query in queries}
        for future in concurrent.futures.as_completed(future_to_query):
            query = future_to_query[future]
            answer = future.result()
            file.write(f"{answer}\n")
            progress.update(1)
            print(f"Q: {query}\nA: {answer}\n")

def main():
    parser = argparse.ArgumentParser(description='Translate a text file from French to English or English to French.')
    parser.add_argument('input_file', type=str, help='Path to the input file to be translated')
    parser.add_argument('--fr2eng', action='store_true', help='Translate from French to English')
    parser.add_argument('--eng2fr', action='store_true', help='Translate from English to French')

    args = parser.parse_args()

    if args.fr2eng:
        translation_function = translatefr2eng
    elif args.eng2fr:
        translation_function = translateeng2fr
    else:
        print("Please specify either --fr2eng or --eng2fr for translation direction")
        exit(1)

    translate_file(args.input_file, translation_function)

if __name__ == "__main__":
    main()
