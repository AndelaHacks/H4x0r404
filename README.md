# An Algo For Realtime Fake News Flaging
![Verified Post](images/bbc.png)


We'll make use of the word2vec algorithm. 
Essentially, the goal is to train a neural network with a single hidden layer; instead of using the model to make predictions (as is typically done in machine learning tasks), we will make use of the weights of the neurons in the single hidden layer to understand the inter-relationship among the words in the texts we're analyzing.
## Preprocessing Data
Before we can start with the word2vec model, we need to pre-process our text data. We will use the same pre-processing function that we used in a previous post about text-mining. We remove numbers and punctuation, stopwords (words which occur frequently but which convey very little meaning, e.g. "the"), and stem the words (remove the endings to group together words with the same root form).
### By :
1. 👩‍💻 Brendah Malakwen
2. 👨‍💻 Gatare Libère
3. 👩‍💻 Forum K. Patel
4. 👨‍💻 Phil Matunda
