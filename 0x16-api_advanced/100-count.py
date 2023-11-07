import praw

def count_words(subreddit, word_list, after=None, counts=None):
    # Initialize PRAW (Reddit API) client
    reddit = praw.Reddit(client_id='YOUR_CLIENT_ID',
                         client_secret='YOUR_CLIENT_SECRET',
                         user_agent='YOUR_USER_AGENT')

    # Create a dictionary to store word counts
    if counts is None:
        counts = {}

    # Base case: no more keywords to search for
    if not word_list:
        # Sort the counts by count (descending) and word (ascending)
        sorted_counts = sorted(counts.items(), key=lambda x: (-x[1], x[0]))

        # Print the sorted counts
        for word, count in sorted_counts:
            print(f"{word.lower()}: {count}")
        return

    # Get the next batch of hot articles in the subreddit
    subreddit_obj = reddit.subreddit(subreddit)
    hot_articles = subreddit_obj.hot(limit=10, params={"after": after})

    # Initialize counts for this keyword
    word = word_list[0].lower()
    if word not in counts:
        counts[word] = 0

    # Search for the keyword in each article title
    for submission in hot_articles:
        title = submission.title.lower()
        if word in title:
            counts[word] += title.count(word)

    # Recursively call count_words with the rest of the word list
    count_words(subreddit, word_list[1:], submission.name, counts)

if __name__ == "__main__":
    import sys

    if len(sys.argv) < 3:
        print("Usage: {} <subreddit> <list of keywords>".format(sys.argv[0]))
    else:
        subreddit = sys.argv[1]
        word_list = sys.argv[2].split()
        count_words(subreddit, word_list)
