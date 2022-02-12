from core.finance.context import Context

if __name__ == '__main__':
    ticks = ["GE", "T", "JNJ", "CVX"]
    no_cache = False

    history_repository = Context().get_history_repository()
    ticker_repository = Context().get_ticker_repository()
    for tick in ticks:
        if no_cache or not history_repository.is_history_exist(tick, True):
            if not history_repository.download_daily(tick):
                continue
        if no_cache or not history_repository.is_history_exist(tick):
            history_repository.build_monthly_data(tick)