class FaderFilter(object):
  def __init__(self, clock, length):
    self.clock = clock
    self.excitements = [0 for a in range(length)]

  def stimulate(self, stimuli):
    new_excitements = []
    for stimulus, excitement in zip(stimuli, self.excitements):
      if stimulus < excitement:
        new_excitement = excitement * 0.9
      else:
        new_excitement = stimulus

      new_excitements.append(new_excitement)

    self.excitements = new_excitements
