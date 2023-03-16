cat << EOF
Usage: plantgardener_cli.py upload image [OPTIONS]

Options:
  -p, --path TEXT                [required]
  -ak, --server_access_key TEXT  [required]
  -sk, --server_secret_key TEXT  [required]
  -n, --name TEXT                [required]
  -w, --width INTEGER            [required]
  -m, --meta_path TEXT           Path to JSON file.
  --help                         Show this message and exit.)

EOF

python plantgardener_cli.py upload image \
    -p data/IMG_20221206_141113.jpg \
    -ak eb861e363ecf1563a824b290dd2e32b633d9d7b3 \
    -sk 0aba77815d86e9861597d6226b4c2f70493891db \
    -n TestPlant \
    -w 2 \
    -m data/metadata.json