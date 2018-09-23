import logging


logging.basicConfig(
    format="%(asctime)s [%(filename)-s:%(lineno)s] [%(levelname)-5.5s] %(message)s",
    level=logging.DEBUG,
)

log = logging.getLogger('root')
