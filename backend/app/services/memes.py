import random

MEMES = [
    {
        "id": "meme-1",
        "title": "HODL mode activated",
        "source": "Crypto Meme Library",
        "image": "https://i.imgflip.com/4/1bij.jpg",
    },
    {
        "id": "meme-2",
        "title": "When BTC moves 2% and everyone becomes an analyst",
        "source": "Crypto Meme Library",
        "image": "https://i.imgflip.com/4/1g8my4.jpg",
    },
    {
        "id": "meme-3",
        "title": "Portfolio is down, confidence is still up",
        "source": "Crypto Meme Library",
        "image": "https://i.imgflip.com/4/26am.jpg",
    },
    {
        "id": "meme-4",
        "title": "Trying to explain crypto risk management",
        "source": "Crypto Meme Library",
        "image": "https://i.imgflip.com/4/2fm6x.jpg",
    },
    {
        "id": "meme-5",
        "title": "Buy the dip, they said",
        "source": "Crypto Meme Library",
        "image": "https://i.imgflip.com/4/9ehk.jpg",
    },
    {
        "id": "meme-6",
        "title": "Me refreshing CoinGecko every 12 seconds",
        "source": "Crypto Meme Library",
        "image": "https://i.imgflip.com/4/1otk96.jpg",
    },
    {
        "id": "meme-7",
        "title": "When your watchlist is green for once",
        "source": "Crypto Meme Library",
        "image": "https://i.imgflip.com/4/1ur9b0.jpg",
    },
    {
        "id": "meme-8",
        "title": "Day trader after one correct prediction",
        "source": "Crypto Meme Library",
        "image": "https://i.imgflip.com/4/30b1gx.jpg",
    },
    {
        "id": "meme-9",
        "title": "Paper hands leaving before the pump",
        "source": "Crypto Meme Library",
        "image": "https://i.imgflip.com/4/1c1uej.jpg",
    },
    {
        "id": "meme-10",
        "title": "Diamond hands during market volatility",
        "source": "Crypto Meme Library",
        "image": "https://i.imgflip.com/4/43a45p.png",
    },
]


def get_random_meme():
    return random.choice(MEMES)