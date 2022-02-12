from core.finance.usecase import CoefficientUsecase
from core.finance.repository import HistoryRepository, TickerRepository, CoefficientRepository
from core.finance.api import HistoryApi, TickerAPI


class Context:
    def __init__(self):
        self.ticker_api = None
        self.history_api = None
        self.history_repository = None
        self.ticker_repository = None
        self.coefficient_repository = None
        self.coefficient_usecase = None

    def get_coefficient_usecase(self):
        if self.coefficient_usecase:
            return self.coefficient_usecase
        self.coefficient_usecase = CoefficientUsecase(self.get_history_repository(),
                                                      self.get_ticker_repository(),
                                                      self.get_coefficient_repository())
        return self.coefficient_usecase

    def get_coefficient_repository(self):
        if self.coefficient_repository:
            return self.coefficient_repository
        self.coefficient_repository = CoefficientRepository()
        return self.coefficient_repository

    def get_history_repository(self):
        if self.history_repository:
            return self.history_repository
        self.history_repository = HistoryRepository(self.get_history_api())
        return self.history_repository

    def get_ticker_repository(self):
        if self.ticker_repository:
            return self.ticker_repository
        self.ticker_repository = TickerRepository(self.get_ticker_api())
        return self.ticker_repository

    def get_history_api(self):
        if self.history_api:
            return self.history_api
        self.history_api = HistoryApi()
        return self.history_api

    def get_ticker_api(self):
        if self.ticker_api:
            return self.ticker_api
        self.ticker_api = TickerAPI()
        return self.ticker_api
