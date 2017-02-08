#!/bin/bash
# Conda packages & nltk downloading for humanities connector
${CONDA_DIR}/bin/conda install --quiet --yes \
            gensim=0.12.4 \
            nltk=3.2.1

# We put NLTK data under /opt/conda, 
# and then set the NLTK_DATA
# environment variable appropriately. See
# http://www.nltk.org/data.html#command-line-installation
# for more info.
mkdir ${CONDA_DIR}/nltk

# MODEL_____________________  TERMS____
# averaged_perceptron_tagger: 17sp 16fa
#                    cmudict:      16fa
#          maxent_ne_chunker: 17sp 16fa
#                      punkt: 17sp 16fa
#                  stopwords: 17sp
#                    wordnet: 17sp 16fa
#                      words: 17sp 16fa
${CONDA_DIR}/bin/python -m nltk.downloader -d ${CONDA_DIR}/nltk \
    averaged_perceptron_tagger \
    cmudict \
    maxent_ne_chunker \
    punkt \
    stopwords \
    wordnet \
    words \
    ;
