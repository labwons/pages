try:
    from ..portfolio.portfolio import individualReport
except ImportError:
    from dev.portfolio.portfolio import individualReport



individualReport()