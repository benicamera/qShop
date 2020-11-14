from time import time


def bubblesort(liste, items):

    h = len(liste)

    for j in range(0, h):
        for i in range(0, h - j):
            if i + 1 < h:
                if liste[i] > liste[i + 1]:
                    merke1 = liste[i + 1]
                    merke2 = liste[i]
                    liste[i] = liste[i + 1]
                    liste[i + 1] = merke2

                    merke_items = items[i]
                    items[i] = items[i + 1]
                    items[i + 1] = merke_items


def get_time():
    sec = time()  # Sekunden seit 1.1.1970
    min = sec/60
    std = min/60
    tag = std/24
    jahr = 365
    tageminus = tag - (50 * jahr + 12)

    tageminus = int(tageminus)

    return tageminus


if __name__ == "__main__":
    print(get_time())
