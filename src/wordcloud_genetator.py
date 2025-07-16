from wordcloud import WordCloud
import matplotlib.pyplot as plt

def generate_wordcloud(words, output_path):
    wc = WordCloud(
        width=300,
        height=150,
        background_color="black",
        colormap="Set2"
    ).generate(" ".join(words))

    plt.figure(figsize=(3, 1.5))
    plt.imshow(wc, interpolation='bilinear')
    plt.axis("off")
    plt.tight_layout(pad=0)
    plt.savefig(output_path, format="png", bbox_inches="tight")
    plt.close()