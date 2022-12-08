## Training FAQ

Welcome to Derkling training! The Derklings use real neural networks, which means that training is somewhat unpredictable. Most of the time they train just fine, but sometimes they get stuck with one behavior, and sometimes they even deteriorate! This guide is here to help you when those things happen.

### Q: How do I get started?

A: First of all, make sure you set some bounties! Without bounties, the Derklings don't know what you want them to train for. Bounties can both be positive and negative; use negative bounties for behaviours you want them to _avoid_, such as jumping off a cliff.

### Q: Training doesn't seem to be improving. What's wrong?

A: First of all, training takes time. Sometimes tens of rounds, sometimes even hundreds. Usually you'll be able to tell from their behavior and the graphs if they are improving or not. If they are improving, then you may just have to wait longer. Use the turbo mode to speed things up!

Sometimes they are not improving, or even deteriorating as well. This may be for a number of reasons. The challenge may be too great (one Derkling vs. four crabs for instance). Sometimes they reach a "local optimum"; i.e. they get stuck with a behaviour and fail to make progress from that. If that happens, you may want to reset your Derklings to eggs and start over again.

### Q: How do the Derklings brains work?

A: The Derklings employ so called ["Recurrent Neural Networks"](http://karpathy.github.io/2015/05/21/rnn-effectiveness/), which are a type of neural network that also has memory. The inputs to the networks are a number of "senses", and the outputs their actions. You can actually see these by enabling "Advanced training" from settings and then clicking the senses and decision buttons in training. The brains have around 3,000 "parameters" and 32 memory slots.

### Q: How are the Derklings trained?

A: The Derklings are trained with what's called a [Genetic Algorithm](https://en.wikipedia.org/wiki/Genetic_algorithm). Basically, run each round in 128 parallel arenas. The parameters of the brains of the Derklings in each arena are slighty tweaked, so they exhibit slightly different behiors. We then take the Derklings with the most gold and copy them to all remaining arenas, and start over again. With time, these random mutations together with selection "trains" the Derklings to perform all kinds of complex behaviors to try to win the game.

### Q: Can I read more about this stuff anywhere?

A: Yes! This all is inspired by the [OpenAI Five DOTA bot](https://openai.com/blog/openai-five/) and the [Uber AI's Deep Neuroevolution](https://eng.uber.com/deep-neuroevolution/) work, which are both great places to start reading about training neural network agents.
