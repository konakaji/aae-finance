from core.finance.repository import HistoryRepository, TickerRepository, CoefficientRepository
from core.finance.entity import History
import numpy as np, math


class CoefficientUsecase:
    def __init__(self, history_repository: HistoryRepository,
                 ticker_repository: TickerRepository, coefficient_repository: CoefficientRepository):
        self.history_repository = history_repository
        self.ticker_repository = ticker_repository
        self.coefficient_repository = coefficient_repository

    def build(self, ticks, span, slide):
        all_ticks, dates = self.get_ticks()
        self.coefficient_repository.save_dates(dates)
        self.coefficient_repository.save_tickers(ticks)
        from_index = 0
        coefficients = []
        while from_index + span < len(dates):
            coefficient = self._do_build(ticks, span, from_index)
            coefficients.append(coefficient)
            from_index = from_index + slide
        return coefficients

    def _do_build(self, ticks, span, from_index):
        dimension = len(ticks)
        result = np.zeros((dimension, span - 1))
        for id, tick in enumerate(ticks):
            histories = self.history_repository.find_history_by_tick_and_span(tick, span, from_index)
            n = len(ticks)
            self.fill(result, id, n, histories)
        self.coefficient_repository.save(result, span, from_index)
        return result

    def load(self, span, date_from_index, ticks):
        return self.coefficient_repository.load(span, date_from_index, ticks)

    def get_ticks(self):
        results = []
        size = 0
        for tick in self.ticker_repository.find_all_ticks():
            histories = self.history_repository.find_history_by_tick(tick)
            if len(histories) == 0:
                print("insufficient data:" + tick)
                continue
            results.append(tick)
            dates = []
            for h in histories:
                dates.append(h.date)
        return results, dates

    def fill(self, result, id, n, histories):
        rs = self.compute_rs(histories)
        t = len(rs)
        m = np.mean(rs)
        sigma = np.std(rs)
        for j, r in enumerate(rs):
            result[id][j] = (r - m) / (sigma * math.sqrt(n * t))

    def compute_rs(self, histories: [History]):
        previous = None
        results = []
        for h in histories:
            if previous is None:
                previous = h.open_price
                continue
            result = math.log(h.open_price) - math.log(previous)
            results.append(result)
            previous = h.open_price
        return results
