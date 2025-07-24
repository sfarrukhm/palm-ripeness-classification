import pandas as pd
import os
import glob as gb
import matplotlib.pyplot as plt

def count_images(path, title):
  df = pd.DataFrame(columns=[f"{title}_Class", "Count"])
  for folder in os.listdir(path):
    files = gb.glob(pathname= path + folder + "/*.jpg")
    df.loc[len(df.index)] = [folder, len(files)]
  return df

import os
import glob as gb
import matplotlib.pyplot as plt
import pandas as pd
from tqdm import tqdm

def get_image_size(path, is_pred=False):
    """
    Arguments:
        path: where images are stored
        is_pred: if True, look in root only
    """
    size = []

    if is_pred:
        folders = [""]
    else:
        folders = os.listdir(path)

    for folder in tqdm(folders):
        for img in gb.glob(os.path.join(path, folder, "*.jpg")):
            image = plt.imread(img)
            size.append(image.shape)
    
    return pd.Series(size).value_counts()


import matplotlib.pyplot as plt
import torch

def visualize_image_samples(data, title, figsize=(16, 6), rows_cols=(3, 10), is_pred=False):
    """
    Arguments:
        data: torch dataset or tensor
        title: plot title
        figsize: figure size
        rows_cols: tuple indicating grid size
        is_pred: if True, assumes data has no labels
    """

    plt.figure(figsize=figsize)
    rows, cols = rows_cols
    plt.suptitle(title, fontsize=16, fontweight='bold')

    for i in range(1, rows * cols + 1):
        plt.subplot(rows, cols, i)
        random_idx = int(torch.randint(0, len(data), size=[1]).item())

        if is_pred:
            image = data[random_idx]
        else:
            image, label = data[random_idx]
            plt.title(class_names[label].title(), fontdict={"color": "blue", "fontsize": 12})

        plt.imshow(image.permute(1, 2, 0))  # Convert from CHW to HWC
        plt.axis('off')

    plt.tight_layout()
    plt.show()
