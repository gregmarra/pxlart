class SixtyToSixtyFourHelper(object):
  @classmethod
  def transform(cls, desired):
    actual = []
    counter = 0
    for x in desired:
      actual.append(x)
      counter += 1
      if counter % 60 == 0:
        actual.append(x)
        actual.append(x)
        actual.append(x)
        actual.append(x)
    return actual