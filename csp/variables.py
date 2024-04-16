class Variable(object):
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return self.name

Unassigned = Variable("Unassigned")

class Domain(list):
    def __init__(self, set):
        list.__init__(self, set)
        self._hidden = []
        self._states = []

    def reset_state(self):
        self.extend(self._hidden)
        del self._hidden[:]
        del self._states[:]

    def push_state(self):
        self._states.append(len(self))

    def pop_state(self):
        diff = self._states.pop() - len(self)
        if diff:
            self.extend(self._hidden[-diff:])
            del self._hidden[-diff:]

    def hide_value(self, value):
        list.remove(self, value)
        self._hidden.append(value)
