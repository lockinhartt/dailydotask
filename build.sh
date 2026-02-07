#!/usr/bin/env bash
set -o errexit

pip install -r requirements.txt

python manage.py collectstatic --no-input
python manage.py migrate

# Download TextBlob/NLTK corpora to a specific directory
mkdir -p nltk_data
python -m textblob.download_corpora
python -c "import nltk; nltk.download('punkt', download_dir='nltk_data'); nltk.download('punkt_tab', download_dir='nltk_data'); nltk.download('averaged_perceptron_tagger_eng', download_dir='nltk_data'); nltk.download('brown', download_dir='nltk_data'); nltk.download('wordnet', download_dir='nltk_data')"
