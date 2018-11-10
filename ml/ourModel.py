from ml import util
import random
import tensorflow as tf
import time

def loadML():
    # Set file names
    file_train_instances = "ml/train_stances.csv"
    file_train_bodies = "ml/train_bodies.csv"
    file_test_instances = "ml/test_stances_unlabeled.csv"
    file_test_bodies = "ml/test_bodies.csv"

    file_predictions = 'ml/ML_predictions.csv'


    # Initialise hyperparameters
    r = random.Random()
    lim_unigram = 5000
    target_size = 4
    hidden_size = 100
    train_keep_prob = 0.6
    l2_alpha = 0.00001
    learn_rate = 0.01
    clip_ratio = 5
    batch_size_train = 500
    epochs = 90


    # Load data sets
    raw_train = util.FNCData(file_train_instances, file_train_bodies)
    raw_test = util.FNCData(file_test_instances, file_test_bodies)
    # n_train = len(raw_train.instances)


    # TODO OH DUDE JUST LET THIS THING DO IT'S SHIT IN THE INITILIZATION!!! Use the test and train sets provided then just use the vectors created!

    # Process data sets - THIS TAKES 17 SECONDS!
    train_set, train_stances, bow_vectorizer, tfreq_vectorizer, tfidf_vectorizer = util.pipeline_train(raw_train, raw_test, lim_unigram=lim_unigram)
    # feature_size = len(train_set[0])
    # fix feature_size at 10001
    feature_size = 10001

    # Define model

    # Create placeholders
    features_pl = tf.placeholder(tf.float32, [None, feature_size], 'features')
    stances_pl = tf.placeholder(tf.int64, [None], 'stances')
    keep_prob_pl = tf.placeholder(tf.float32)

    # Infer batch size
    batch_size = tf.shape(features_pl)[0]

    # Define multi-layer perceptron
    hidden_layer = tf.nn.dropout(tf.nn.relu(tf.contrib.layers.linear(features_pl, hidden_size)), keep_prob=keep_prob_pl)
    logits_flat = tf.nn.dropout(tf.contrib.layers.linear(hidden_layer, target_size), keep_prob=keep_prob_pl)
    logits = tf.reshape(logits_flat, [batch_size, target_size])

    # Define L2 loss
    tf_vars = tf.trainable_variables()
    l2_loss = tf.add_n([tf.nn.l2_loss(v) for v in tf_vars if 'bias' not in v.name]) * l2_alpha

    # Define overall loss
    loss = tf.reduce_sum(tf.nn.sparse_softmax_cross_entropy_with_logits(logits, stances_pl) + l2_loss)

    # Define prediction
    softmaxed_logits = tf.nn.softmax(logits)
    predict = tf.arg_max(softmaxed_logits, 1)
    sess = tf.Session()
    util.load_model(sess)
    return sess, keep_prob_pl, predict, features_pl, bow_vectorizer, tfreq_vectorizer, tfidf_vectorizer

def runModel(sess, keep_prob_pl, predict, features_pl, bow_vectorizer, tfreq_vectorizer, tfidf_vectorizer):
    start_time = time.time()
    print("Now running predictions...")
    # THIS is the info from Henry
    userClaims = "ml/claims.csv"
    userBodies = "ml/bodies.csv"
    # parse that info
    raw_test = util.FNCData(userClaims, userBodies)
    # need more stuff for this
    test_set = util.pipeline_test(raw_test, bow_vectorizer, tfreq_vectorizer, tfidf_vectorizer)
    # idk what this does really
    test_feed_dict = {features_pl: test_set, keep_prob_pl: 1.0}
    # run predictions
    test_pred = sess.run(predict, feed_dict=test_feed_dict)
    # timing
    print("ML 'runModel': --- %s seconds ---" % (time.time() - start_time))
    print("Preditions complete.")
    return test_pred
