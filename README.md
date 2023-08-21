# Text File Translation

This script translates a text file from French to English or English to French using OpenAI's GPT-4 language model.

## Prerequisites

- You need to have an OpenAI API key to use this script.
- Install the necessary libraries using the following command:

```
pip install openai
```

## How to use

1. Set an environment variable called `OPENAI_API_KEY` with your OpenAI API key.

```
export OPENAI_API_KEY=<your_api_key>
```

2. Run the script using the following command format.

```
python text_file_translation.py <input_file> --fr2eng/--eng2fr
```

Replace `<input_file>` with the path to the file you want to translate and use the `--fr2eng` flag to translate from French to English and the `--eng2fr` flag to translate from English to French.

### Example

Example command to translate a file called `example.txt` from French to English:

```
python text_file_translation.py example.txt --fr2eng
```

## Output

The output file will be placed in the `/path/to/your/output/directory/` folder by default. The file name will have the format `<input_file_name>_tr.txt`, and it will contain one translated line for each line in the input file.

## Note

If you reach the rate limits for the OpenAI API, the script will retry the translation after 30 seconds, up to a maximum of 3 retries per line.