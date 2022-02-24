import sys
import random
import heapq
import numpy as np

DEBUG = True


def main():
    photo_c = int(sys.stdin.readline())

    tags_lib = {}
    last_tid = 0
    photos = {"V": [], "H": []}
    for i in range(photo_c):
        orientation, _, *tags = sys.stdin.readline().strip().split(" ")
        ntags = []
        for tag in tags:
            tid = 0
            if tag not in tags_lib:
                last_tid += 1
                tags_lib[tag] = last_tid
                tid = last_tid
            else:
                tid = tags_lib[tag]
            ntags.append(tid)
        photos[orientation].append(Photo(i, orientation, ntags))
    # if DEBUG:
    #     print(f"Count:{photo_c}")
    #     for photo in photos["V"]:
    #         print(photo)
    #     for photo in photos["H"]:
    #         print(photo)
    photos["V"].sort(key=lambda x: len(x.tags))
    slides = []

    v_size = len(photos["V"])
    # kalo photos["V"] ganjil maka -> buang paling kecil -> for loop selanjutnya ga mikirin itu soal nya
    if v_size % 2 == 1:
        photos["V"] = photos["V"][1:]

    count = 0
    for i in range(v_size // 2):
        slides.append(Slide(count, [photos["V"][i], photos["V"][v_size - 1 - i]]))
        count += 1
    for i in photos["H"]:
        slides.append(Slide(count, [i]))
        count += 1

    slideshow = [0]
    i = 0
    slides[0].taken = True
    while len(slideshow) < len(slides):
        best = (-1, -1)  # score, id
        for j in range(len(slides)):
            if i == j:
                continue
            if slides[j].taken:
                continue
            print(slides[i].tags)
            score = min(len(slides[i].tags - slides[j].tags),
                        len(slides[i].tags.intersection(slides[j].tags)),
                        len(slides[j].tags - slides[i].tags))

        # score += min(len(np.setdiff1d(slides[i].tags, slides[j].tags)), len(np.intersect1d(slides[i].tags, slides[j].tags)), len(np.setdiff1d(slides[j].tags, slides[i].tags)))
            if score > best[0]:
                best = (score, j)
        if best[1] == -1:
            break
        slideshow.append(best[1])
        slides[best[1]].taken = True
        i = best[1]
        if DEBUG:
            # if 0 == len(slideshow) % (len(slides) // 10000000):
            print(f"{len(slideshow) / len(slides) * 100:.3f}%")

    print("SOLUTION")
    print(f"{len(slideshow)}", file=sys.stderr)
    for sidx in slideshow:
        print(f"{' '.join([str(p.id) for p in slides[sidx].photos])}", file=sys.stderr)

    print("SCORE")
    score = 0
    for i in range(len(slideshow) - 1):
        j = i + 1
        score += min(len(np.setdiff1d(slides[slideshow[i]].tags, slides[slideshow[j]].tags)), len(np.intersect1d(slides[slideshow[i]].tags, slides[slideshow[j]].tags)), len(np.setdiff1d(slides[slideshow[j]].tags, slides[slideshow[i]].tags)))
    print(f"{score:,}")


# pairwise = {} # [i][j] : (Rj, IJ, RJ)
# for i, s1 in enumerate(slideshow):
#     pairwise[s1.id] = {}
#     # pairwise_weight[s1.id] = {}
#     for s2 in slides:
#         # pairwise[s1.id][s2.id] = ((s1, s2), 1 / (1 + min(len(s1.tags.difference(s2.tags)), len(s1.tags.intersection(s2.tags)), len(s2.tags.difference(s1.tags)))))
#         # if DEBUG:
#         #     print(f"{s1.id} {s2.id}\t-> {pairwise[s1.id][s2.id]}")
#     if DEBUG:
#         if len(slides) // 20000 and not i % (len(slides) // 20000):
#             print(f"{i / len(slides) * 100:.3f}%")

# pairwise_ks = list(pairwise.values())
# pairwise_ks.sort(key=lambda pair: min(len(pair[1]), len(pair[2]), len(pair[3])))
# if DEBUG:
#     for i in pairwise_ks:
#         print(i)

# largest cost path
# slideshow = []
# q = [(0, slides[0])]
# while len(q):
#     _, current = heapq.heappop(q)
#     if current.taken:
#         continue
#     current.taken = True
#     slideshow.append(current)
#     for adj in slides:
#         if adj.taken or adj.id == current.id:
#             continue
#         heapq.heappush(q, (1 / (1 + min(len(current.tags.difference(adj.tags)), len(current.tags.intersection(adj.tags)), len(adj.tags.difference(current.tags)))), adj))
#     print(f"{len(slideshow)}\t{len(q):,}")

# for slide in slideshow:
#     print(slide)


class Photo:
    def __init__(self, _id, orientation, tags):
        self.id = _id
        self.orientation = orientation
        self.tags = set(tags)

    def __str__(self):
        return f"id:{self.id} o:{self.orientation} t:{self.tags}"

    def __repr__(self):
        return f"id:{self.id} o:{self.orientation} t:{self.tags}"


class Slide:
    def __init__(self, _id, photos):
        self.id = _id
        self.photos = photos
        self.tags = photos[0].tags if len(photos) == 1 else photos[0].tags.union(photos[1].tags)
        self.taken = False

    def __str__(self):
        return f"id:{self.id} p:{self.photos} t:{self.tags}"

    def __lt__(self, other):
        return self


if __name__ == "__main__":
    main()
