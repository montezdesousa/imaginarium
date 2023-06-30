# Imaginarium

Imaginarium is a reverse image search engine. Wut? It is basically a cheap version of Google Lens.

The engine receives an image hosted on the web and searches similar images on the archive database.

Well, actually it's only on a subset, 43k images were loaded in the model.

To do this it uses a pre-trained neural network and applies K-Nearest Neighbors algorithm to find the most similar images.

This work has been submitted for the annual contest of [Arquivo.pt](https://arquivo.pt), the Portuguese web archive, which awards original works based on the data they preserve. This archive is a search engine for web pages of the past and the idea was to extend it with reverse image search.

The project was awarded an honorable mention by [Aveiro Media Competence Center](https://a-mcc.eu/pt).

Check the other winning projects [here](https://sobre.arquivo.pt/pt/conheca-os-vencedores-do-premio-arquivo-pt-2023).

# How it works?

You paste any image hyperlink.

The engine extracts the image features.

It returns the most similar images in the database.

No metadata was provided to the model, so results can be funny :)

This is a video with some examples:

[![imaginarium](https://img.youtube.com/vi/dwebaxpzBGo/0.jpg)](https://www.youtube.com/watch?v=dwebaxpzBGo)
