import sys

debug = True

def main():
    _, count_l, count_d = sys.stdin.readline().strip().split(" ")
    count_l, count_d = int(count_l), int(count_d)
    if debug: print(f"L:{count_l} D:{count_d}")

    book_set = {}
    libraries = []

    score_b = sys.stdin.readline().strip().split(" ")
    for bid, score in enumerate(score_b):
        book_set[bid] = Book(bid, int(score))

    for lid in range(count_l):
        count_b, sud, bpd = sys.stdin.readline().strip().split(" ")
        count_b, sud, bpd = int(count_b), int(sud), int(bpd)
        books = []
        total_score = 0
        for bid in sys.stdin.readline().strip().split(" "):
            book = book_set[int(bid)]
            books.append(book)
            total_score += book.score
        books.sort(key=lambda b: b.score, reverse=True)
        library = Library(lid, books, bpd, sud)
        # SORTING KEY
        library.total_score = total_score
        libraries.append(library)

    libraries.sort(key=lambda l: (count_d - l.sud) * l.total_score / l.bpd, reverse=True)

    shipment = []
    signing = None
    for d in range(count_d):
        idle = True
        if (signing is None or signing.signedup >= 0) and len(shipment) < count_l:
            libraries.sort(key=lambda l: (count_d - d - l.sud) * l.total_score / l.bpd, reverse=True)
            for l in libraries:
                if l.signedup < 0:
                    signing = l
                    shipment.append(signing)
                    idle = False
                    break
        for l in libraries:
            if l.signedup >= 0 and len(l.sbooks) < len(l.books):
                if l.books[l.bidx].score <= 0:
                    l.bidx = 0
                    while l.bidx < len(l.books) - 1 and l.books[l.bidx].score <= 0:
                        l.bidx += 1
                l.books[l.bidx].score = 0
                l.sbooks.append(l.books[l.bidx])
                l.bidx = (l.bidx + 1) % len(l.books)
                idle = False
        if idle and signing.signedup >= 0:
            break
        signing.signedup += 1
        if debug:
            if count_d // 20 and not d % (count_d // 20):
                print(f"{d / count_d * 100:.0f}%")

    if debug: print("\nSOLUTION")
    print(len(shipment), file=sys.stderr)
    for l in shipment:
        print(f"{l.lid} {l.bidx}", file=sys.stderr)
        bids = []
        for book in l.sbooks:
            bids.append(str(book.bid))
        print(" ".join(bids), file=sys.stderr)

    print("\nSCORE")
    calc_score(shipment)


def calc_score(shipment, debug=False):
    score = 0
    books = set()
    for l in shipment:
        for book in l.sbooks:
            if book not in books:
                score += book.tscore
                books.add(book)
    print(f"{score:,}")
    print()


class Book:
    def __init__(self, bid, score, delivered=False):
        self.bid = bid
        self.score = score
        self.tscore = score
        self.delivered = delivered
    
    def __str__(self):
        return f"bid:{self.bid} score:{self.score}"
    
    def __repr__(self):
        return f"({self})"


class Library:
    def __init__(self, lid, books, bpd, sud):
        self.lid = lid
        self.books = books
        self.sbooks = []
        self.books_set = set(books)
        self.bpd = bpd
        self.sud = sud
        self.key = 0
        self.bidx = 0
        self.signedup = -sud
    
    def __str__(self):
        return f"lid:{self.lid} books:{self.books} bpd:{self.bpd} sud:{self.sud} key:{self.key}"


if __name__ == "__main__":
    main()
