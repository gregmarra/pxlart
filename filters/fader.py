import time

class FaderFilter(object):
  def __init__(self, length, time_decay=1):
    self.excitements = [0 for a in range(length)]
    self.last_time = time.time()
    self.time_decay = time_decay

  def stimulate(self, stimuli):
    new_excitements = []
    decay = self.decay()
    
    for stimulus, excitement in zip(stimuli, self.excitements):
      new_excitement = max(stimulus, excitement * decay)
      new_excitements.append(new_excitement)

    self.excitements = new_excitements

  def decay(self):
    ellapsed_time = (time.time() - self.last_time)
    self.last_time = time.time()
    return max(0, 1 - (ellapsed_time / self.time_decay))
