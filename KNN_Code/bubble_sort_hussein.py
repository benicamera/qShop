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
