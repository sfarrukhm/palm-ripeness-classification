def count_images(path, title):
  df = pd.DataFrame(columns=[f"{title}_Class", "Count"])
  for folder in os.listdir(path):
    files = gb.glob(pathname= path + folder + "/*.jpg")
    df.loc[len(df.index)] = [folder, len(files)]
  return df
