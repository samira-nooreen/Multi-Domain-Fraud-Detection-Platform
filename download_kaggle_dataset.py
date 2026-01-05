import kagglehub, os
path = kagglehub.dataset_download('bhavikjikadara/fake-news-detection')
print('Dataset downloaded to:', path)
for root, dirs, files in os.walk(path):
    for f in files:
        print(os.path.join(root, f))
