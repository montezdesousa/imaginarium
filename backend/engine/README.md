# Establishing a connection with Google Cloud database requires the following environment variables (`DB_ADDRESS` must be whitelisted in Google Cloud):
    - `DB_USER`
    - `DB_PASS`
    - `DB_ADDRESS`
    - `DB_PORT`
    - `DB_NAME`

# To extract the URLs from the Arquivo.pt API run (this might take a while):
```zsh
    python -m engine.extract_features
```

# To train the knn with extracted features run:
```zsh
    python -m engine.train_knn
```