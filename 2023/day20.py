import collections
import math


def first(modules, broadcaster):
    signals = {True: 0, False: 0}
    for _ in range(1000):
        queue = collections.deque([(Module('button'), broadcaster, False)])
        while queue:
            src, dst, signal = queue.popleft()
            signals[signal] += 1
            next_signals = dst._receive_signal(src, signal)
            for next_signal in next_signals:
                queue.append(next_signal)
    return signals[False] * signals[True]


def second(modules, broadcaster):
    idx = 0
    sent = False
    while not sent:
        queue = collections.deque([(Module('button'), broadcaster, False)])
        idx += 1
        while queue:
            src, dst, signal = queue.popleft()
            if src.name in ['vv', 'nt', 'vn', 'zq'] and not signal and isinstance(dst, ConModule):
                print(f"{src.name} sent low to {dst.name} on {idx}")
            next_signals = dst._receive_signal(src, signal)
            for next_signal in next_signals:
                queue.append(next_signal)
    return idx



class Module:
    def __init__(self, name, successors=None):
        if successors is None:
            successors = []
        self.name = name
        self.successors: list[Module] = successors

    def _receive_signal(self, src, signal):
        # print(f"{src.name} -{'high' if signal else 'low'}-> {self.name}")
        signal_to_send = self._process_signal(src, signal)
        if signal_to_send is None:
            return []
        return [(self, successor, signal_to_send) for successor in self.successors]

    def _process_signal(self, src, signal):
        pass

    def add_successor(self, successor):
        assert isinstance(successor, Module)
        self.successors.append(successor)

    def add_processor(self, processor):
        pass

    def __eq__(self, other):
        if isinstance(other, Module):
            return self.name == other.name
        if isinstance(other, str):
            return self.name == other
        return False

    def __hash__(self):
        return hash(self.name)

    def __repr__(self):
        return f"<{self.__class__.__name__}: {self.name}>"


class Broadcaster(Module):
    def _process_signal(self, src, signal):
        return signal

    def __hash__(self):
        return hash(self.name)


class FFModule(Module):
    def __init__(self, *args):
        super().__init__(*args)
        self.state = False

    def __eq__(self, other):
        if isinstance(other, FFModule):
            return self.name == other.name and self.state == other.state
        if isinstance(other, str):
            return f"%{self.name}" == other or self.name == other
        return False

    def _process_signal(self, src, signal):
        if not signal:
            self.state = not self.state
            return self.state
        return None

    def __hash__(self):
        return hash(self.name)


class ConModule(Module):
    def __init__(self, *args):
        super().__init__(*args)
        self.received = {}

    def add_processor(self, processor):
        self.received[processor] = False

    def _process_signal(self, src, signal):
        self.received[src] = signal
        return not all(self.received.values())

    def __eq__(self, other):
        if isinstance(other, ConModule):
            return self.received == other.received
        if isinstance(other, str):
            return f"&{self.name}" == other or self.name == other
        return False

    def __hash__(self):
        return hash(self.name)


def solve(filename, solve_func):
    with open(f"data/{filename}", 'r') as input_file:
        puzzle_input = [line.replace('\n', '') for line in input_file.readlines()]
    modules = []
    for module in puzzle_input:
        name, _ = module.split(' -> ')
        if name == 'broadcaster':
            modules.append(Broadcaster('broadcaster'))
        elif name[0] == '%':
            modules.append(FFModule(name[1:]))
        elif name[0] == '&':
            modules.append(ConModule(name[1:]))
        else:
            raise NameError("Unknown module")
    for module in puzzle_input:
        name, successors = module.split(' -> ')
        src = modules[modules.index(name)]
        successors = successors.split(', ')
        for successor in successors:
            if successor not in modules:
                modules.append(Module(successor))
            dst = modules[modules.index(successor)]
            src.add_successor(dst)
            dst.add_processor(src)
    return solve_func(modules, modules[modules.index('broadcaster')])


if __name__ == '__main__':
    print(solve("day20.txt", first))
    # print(solve("day20.txt", second))
    print(math.lcm(3733, 3797, 3877, 3917))
