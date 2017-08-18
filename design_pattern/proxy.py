# Proxy
# client - proxy(secretary) - real(boss)
# client - agent - actor

class Actor(object):
    def __init__(self,name):
        self.name = name
        self.isBusy = False
    def occupied(self):
        self.isBusy = True
        print self.name, "is occupied with current movie"
    def available(self):
        self.isBusy = False
        print self.name, "is free for the movie"
    def getStatus(self):
        return self.isBusy
    def setStatus(self,isBusy):
        self.isBusy = isBusy

class Agent(object):
    def __init__(self,actor):
        self.actor = actor
    def work(self):
        if self.actor.getStatus():
            self.actor.occupied()
        else:
            self.actor.available()

if __name__ == '__main__':
    james = Actor('James')
    r = Agent(james)
    r.work()
    james.setStatus(True)
    r.work()

