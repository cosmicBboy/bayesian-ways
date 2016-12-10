"""This file contains code for use with "Think Bayes",
by Allen B. Downey, available from greenteapress.com

Copyright 2012 Allen B. Downey
License: GNU GPLv3 http://www.gnu.org/licenses/gpl.html
"""

from thinkbayes import Pmf
import random


class Cookie(Pmf):
    """A map from string bowl ID to probablity."""

    def __init__(self, hypos):
        """Initialize self.

        hypos: sequence of string bowl IDs
        """
        Pmf.__init__(self)
        for hypo in hypos:
            self.Set(hypo, 1)
        self.Normalize()
        self._mixes = {
            "Bowl 1": Bowl(30, 10),
            "Bowl 2": Bowl(20, 20)
        }

    @property
    def mixes(self):
        return {k: v.mix for k, v in self._mixes.items()}

    def Update(self, data):
        """Updates the PMF with new data.

        data: string cookie type
        """
        hypos = self.Values()
        for hypo in hypos:
            like = self.Likelihood(data, hypo)
            self.Mult(hypo, like)
        # pick a bowl at random to pull a cookie out and modify the mixture
        # of the bowls
        choice = random.randint(*range(len(hypos)))
        print("Picking {} from {}".format(data, hypos[choice]))
        self.UpdateMix(data, hypos[choice])
        self.Normalize()

    def Likelihood(self, data, hypo):
        """The likelihood of the data under the hypothesis.

        data: string cookie type
        hypo: string bowl ID
        """
        mix = self.mixes[hypo]
        like = mix[data]
        return like

    def UpdateMix(self, data, hypo):
        mix = self._mixes[hypo]
        mix.decrement(data)


class Bowl(object):

    def __init__(self, num_vanilla, num_chocolate):
        self._mix = {
            "vanilla": num_vanilla,
            "chocolate": num_chocolate
        }

    def decrement(self, cookie):
        self._mix[cookie] -= 1

    @property
    def mix(self):
        total = sum(self._mix.values())
        return {k: float(v) / total for k, v in self._mix.items()}


def main():
    hypos = ['Bowl 1', 'Bowl 2']

    pmf = Cookie(hypos)

    dataset = ["vanilla", "chocolate", "vanilla"]
    for d in dataset:
        print "Data: {}".format(d)
        pmf.Update(d)
        for hypo, prob in pmf.Items():
            print hypo, prob
        print(pmf.mixes)
        print ""

if __name__ == '__main__':
    main()
