from csp.variables import Unassigned


class Constraint(object):
    def __init__(self, func, assigned=True):
        self._func = func
        self._assigned = assigned

    def __call__(self, variables, domains, assignments, forwardcheck=False, _unassigned=Unassigned,):
        parms = [assignments.get(x, _unassigned) for x in variables]
        missing = parms.count(_unassigned)
        if missing:
            return (self._assigned or self._func(variables, *parms)) and (
                not forwardcheck or
                self.forward_check(variables, domains, assignments)
            )
        return self._func(variables, *parms)

    def forward_check(self, variables, domains, assignments, _unassigned=Unassigned):
        unassigned_variable = _unassigned
        for variable in variables:
            if variable not in assignments:
                if unassigned_variable is _unassigned:
                    unassigned_variable = variable
                else:
                    break
        else:
            if unassigned_variable is not _unassigned:
                # Remove from the unassigned variable domain's all
                # values which break our variable's constraints.
                domain = domains[unassigned_variable]
                if domain:
                    for value in domain[:]:
                        assignments[unassigned_variable] = value
                        if not self(variables, domains, assignments, forwardcheck=False):
                            domain.hide_value(value)
                    del assignments[unassigned_variable]
                if not domain:
                    return False
        return True
