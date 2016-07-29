# django-corenlp
Django wrapper around Stanford's CoreNLP service that exposes document functionality seemlessly to you.

# Requirements
* Uses the [stanza](https://github.com/stanfordnlp/stanza) library to represent CoreNLP objects and to use the
CoreNLP server.

# Using `git subtree`

If you would like to develop this project within your existing project (which is highly likely), the recommendation is to use the `git subtree` method.
You can get started by running the following commands (happily stolen from the [stanza](https://github.com/stanfordnlp/stanza) project):

    # Add your fork of django-corenlp as a remote repo
    git remote add corenlp git@github.com:<your-user-name>/django-corenlp.git
    # Import the contents of the repo as a subtree
    git subtree add --prefix third-party/corenlp corenlp master --squash
    # Put a symlink to the actual module somewhere where your code needs it
    ln -s third-party/corenlp corenlp
    # Add aliases for the two things you'll need to do with the subtree
    git alias corenlp-update subtree pull --prefix third-party/corenlp corenlp master --squash
    git alias corenlp-push subtree push --prefix third-party/corenlp corenlp master

