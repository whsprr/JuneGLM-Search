import re
import requests
import subprocess
import random
import datetime
import os
from urllib.parse import urlparse
from shutil import copyfile
import wikipedia
from collections import Counter


def process_text_operations(file_path, chunk_size, user_phrase):
    def preprocess_text(text):
        return text

    def process_text_in_chunks(file_path, chunk_size, n):
        ngram_dict = {}
        with open(file_path, 'r') as file:
            while True:
                chunk = file.read(chunk_size)
                if not chunk:
                    break

                chunk = preprocess_text(chunk)
                words = chunk.split()
                for i in range(len(words) - n):
                    context = tuple(words[i:i + n])
                    next_word = words[i + n]

                    if context in ngram_dict:
                        ngram_dict[context].append(next_word)
                    else:
                        ngram_dict[context] = [next_word]

        return ngram_dict

    def find_word_occurrences_in_chunks(file_path, phrase, chunk_size):
        occurrences = []
        with open(file_path, 'r') as file:
            while True:
                chunk = file.read(chunk_size)
                if not chunk:
                    break

                chunk = preprocess_text(chunk)
                words = chunk.split()
                input_words = phrase.split()

                for i in range(len(words) - 1):
                    if words[i].lower() == input_words[0].lower():
                        if words[i + 1].lower().startswith(input_words[1].lower()):
                            occurrences.append(words[i + 1])

        return occurrences

    def generate_sentence_with_correction(ngram_dict, input_context, corrected_word):
        sentence = list(input_context[:-1])  # Exclude the incomplete part of the phrase
        sentence.append(corrected_word)  # Append the corrected word
        sentence.extend(predict_next_word(ngram_dict, sentence))  # Generate sentence
        return ' '.join(sentence)

    def predict_next_word(ngram_dict, context, max_words=100):
       predicted_words = []
       current_context = tuple(context)  # Convert context to a tuple

       for _ in range(max_words):
           if current_context in ngram_dict:
               possible_next_words = ngram_dict[current_context]
               if len(possible_next_words) == 1 and possible_next_words[0] == '.':
                   predicted_words.append('.')
                   break  # Stop if the only predicted word is a full stop
               next_word = random.choice(possible_next_words)
               predicted_words.append(next_word)
               if next_word == '.':
                   break  # Stop if the predicted word is a full stop
               current_context = tuple(list(current_context[1:]) + [next_word])
           else:
               break

       return predicted_words
    default_n = 2  # Default n-gram size if the input is shorter
    ngram_dictionary = process_text_in_chunks(file_path, chunk_size, default_n)

    word_occurrences = find_word_occurrences_in_chunks(file_path, user_phrase, chunk_size)

    if len(word_occurrences) > 0:
        most_common_word = Counter(word_occurrences).most_common(1)[0][0]
        print(f"The most common word following the first word in the phrase is: {most_common_word}")

        input_context = user_phrase.split()
        input_context[-1] = most_common_word

        corrected_sentence = generate_sentence_with_correction(ngram_dictionary, input_context, most_common_word)
        print(f"Generated sentence starting from '{' '.join(input_context)}': \n {corrected_sentence}")
    else:
        print(f"No words following the first word in the phrase were found in the text.")


def search(query):
  url = f"https://api.duckduckgo.com/?q={query}&format=json"
  response = requests.get(url)

  if response.status_code == 200:
      data = response.json()
      if 'RelatedTopics' in data:
          related_topics = data['RelatedTopics']
          for topic in related_topics:
              if 'Text' in topic and 'FirstURL' in topic:
                  print(f"{topic['Text']}\nURL: {topic['FirstURL']}\n")
      else:
          print("No results found.")
  else:
      print("Failed to fetch results.")

def weather_command(zip_code):
    return lol

def calculate_command(expression):
    # Use Python's eval function to calculate the expression
    result = eval(expression)
    return result

def flip_coin():
    return random.choice(['Heads', 'Tails'])

def roll_dice(sides):
    return random.randint(1, sides)

def google_search(query):
    search_results = googlesearch.search(query, num=1, stop=1)
    return search_results[0]

def fetch_wikipedia_summary(topic):
    try:
        summary = wikipedia.summary(topic, sentences=2)
        return summary
    except wikipedia.exceptions.DisambiguationError as e:
        return f"Multiple results found. Please specify: {', '.join(e.options)}"
    except wikipedia.exceptions.PageError:
        return f"Sorry, no information found for '{topic}'"

def download_file(url, file_name=None):
    try:
        response = requests.get(url)
        if file_name:
            with open(file_name, 'wb') as file:
                file.write(response.content)
                return f"Downloaded {url} as {file_name}"
        else:
            parsed_url = urlparse(url)
            file_name = os.path.basename(parsed_url.path)
            with open(file_name, 'wb') as file:
                file.write(response.content)
                return f"Downloaded {url} as {file_name}"
    except requests.exceptions.RequestException as e:
        return f"Error downloading file: {e}"

def copy_file(source_file, destination_file):
  try:
      shutil.copy(source_file, destination_file)
      return f"File copied from {source_file} to {destination_file} successfully."
  except FileNotFoundError:
      return "File not found. Please check the file paths."
  except PermissionError:
      return "Permission denied. Please ensure you have necessary permissions."
  except Exception as e:
      return f"An error occurred: {e}"

def rename_file(old_name, new_name):
  try:
      os.rename(old_name, new_name)
      return f"File {old_name} renamed to {new_name} successfully."
  except FileNotFoundError:
      return "File not found. Please check the file paths."
  except PermissionError:
      return "Permission denied. Please ensure you have necessary permissions."
  except Exception as e:
      return f"An error occurred: {e}"

def process_command(user_input):
    weather_pattern = r'weather for (\d+)'
    calculate_pattern = r'calculate (.*)'
    google_pattern = r'google "(.*)"'
    wiki_pattern = r'wikipedia (.*)'
    download_pattern = r'download (.*)'
    hello_pattern = r'hello'
    how_pattern = r'how are you'
    i_pattern = r'i feel (.*)'
    search_pattern = r'search (.*)'
    gen_pattern = r'generate (.*)'
    coin_pattern = r'flip a coin'
    copy_pattern = r'copy (.*) to (.*)'
    rename_pattern = r'rename (.*) to (.*)'

    if re.match(weather_pattern, user_input):
        match = re.match(weather_pattern, user_input)
        zip_code = match.group(1)
        return weather_command(zip_code)

    elif re.match(calculate_pattern, user_input):
        match = re.match(calculate_pattern, user_input)
        expression = match.group(1)
        return calculate_command(expression)

    elif re.match(hello_pattern, user_input):
      hello = "Hello!"
      return hello

    elif re.match(how_pattern, user_input):
      expression = "I feel as a great as a search tool can be! Which is good by the way."
      return expression

    elif re.match(i_pattern, user_input):
      match = re.match(i_pattern, user_input)
      expression = match.group(1)
      output = "It's ok to feel ", + expression
      return output

    elif re.match(rename_pattern, user_input):
      match = re.match(rename_pattern, user_input)
      old_name = match.group(1)
      new_name = match.group(2)
      return rename_file(old_name, new_name)

    elif re.match(copy_pattern, user_input):
      match = re.match(copy_pattern, user_input)
      source_file = match.group(1)
      destination_file = match.group(2)
      return copy_file(source_file, destination_file)

    elif re.match(coin_pattern, user_input):
        match = re.match(coin_pattern, user_input)
        return flip_coin()

    elif re.match(google_pattern, user_input):
        match = re.match(google_pattern, user_input)
        query = match.group(1)
        return google_search(query)

    elif re.match(wiki_pattern, user_input):
        match = re.match(wiki_pattern, user_input)
        topic = match.group(1)
        return fetch_wikipedia_summary(topic)

    elif re.match(download_pattern, user_input):
        match = re.match(download_pattern, user_input)
        url = match.group(1)
        return download_file(url)
      
    elif re.match(search_pattern, user_input):
      match = re.match(search_pattern, user_input)
      url = match.group(1)
      return search(url)
      
    elif re.match(gen_pattern, user_input):
      match = re.match(gen_pattern, user_input)
      file_path = "sample_text.txt"
      chunk_size = 10000
      user_phrase = match.group(1)
      return process_text_operations(file_path, chunk_size, user_phrase)

    # Add other conditions for different commands

    else:
        return "Hmm, I don't understand?"

def main():
    while True:
        user_input = input("./june ")

        if user_input.lower() == 'exit':
            break

        result = process_command(user_input)
        print('')
        print(result)
        print('')

if __name__ == "__main__":
    main()
